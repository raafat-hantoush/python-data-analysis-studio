'''
import modules
'''
import json; import os
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseRedirect
import numpy as np; import pandas as pd
import pickle

from  service.eda_plotting import plot_vizualisation
import service.experiments_controller as exp
from  service.experiments_controller import Experiment
from service.eda_stats import get_stats_html
from service.code_generation import load_generated_code_dict
from service.code_generation import generate_tree_view_json_data
from service.code_generation import export_experiment_to_notebook
import service.jupyter_kernel_executor as kernel
from service.file_explorer import get_project_files_directories_list
'''
helper function to get the data frame via jupyter kernel request
'''
def get_data_frame():
    df=pd.DataFrame({})
    try:
        frame_json=kernel.execute_code(["pd.DataFrame.to_json(df,orient='columns')"])
        frame_json= frame_json[0]      
        df=pd.read_json(frame_json[1:-1],orient='columns')
    except Exception as e:
        print("data frame to json exception: "+str(e))
    return df

'''
loading the data frame via ajax call when refressh data button is clicked
''' 
def load_data_frame(request):
    print("load data frame is invoked!")
    ##print(request.GET.get('data', ''))
    frame_html=""
    df=pd.DataFrame({})
    df_name=request.GET.get('data', '')
    if df_name in ["df","y","y_train","y_test"] :
        df_name=df_name
        #print(df_name)
    try:
        frame_json=kernel.execute_code(["pd.DataFrame.to_json(pd.DataFrame("+df_name+"),orient='columns')"])
        frame_json= frame_json[0]      
        df=pd.read_json(frame_json[1:-1],orient='columns')
        frame_html = pd.DataFrame.to_html(df, max_rows=20, max_cols=100, justify='justify-all',
                                          show_dimensions=True, bold_rows=False)
        frame_html = frame_html.replace('<table border="1" class="dataframe">', 
                                        '<table border="1" class="table table-sm table-responsive">')
    except Exception as e:
                print("data frame to json exception: "+str(e))
    return HttpResponse(json.dumps(frame_html), content_type='application/json')

'''
adding new step to the experiment via ajax call on jstree double click
'''
def add_new_step(request):
    try:
        print("add new step is invoked")
        current_experiment=""
        experiments=[]
        commands=[]
        steps,steps_desc,steps_codes = [],[],[]
        steps_out="";new_step=""
        filepath=request.GET['filepath']
        project_file=open(filepath, 'rb')
        print("loading the pickle file")
        if project_file: experiments,current_experiment,commands,settings,code_output_msg,generated_code_dict= pickle.load(project_file)  
        if experiments:
            steps,steps_desc,steps_codes=exp.get_experiment_info(experiments,current_experiment)
        if not commands: commands=[]
        if not generated_code_dict: 
            generated_code_dict=load_generated_code_dict()
    except FileNotFoundError: 
        print("new step project file not found")  
     
    new_step = request.GET['new_step']
    ##print(request.GET['filepath'])
    
    if new_step:
        ##print("step_selected is: "+ new_step)
        steps.append(new_step)
        
        if(new_step in generated_code_dict):
            new_step_generated_desc=generated_code_dict[new_step]["step_desc"]
            new_step_generated_code=generated_code_dict[new_step]["step_code"]
            steps_desc.append(new_step_generated_desc)
            steps_codes.append(new_step_generated_code)
        else:
            steps_desc.append("")
            steps_codes.append("")
                
        ## update the experiment steps
        exp.update_experiment_steps(experiments,current_experiment,steps,steps_desc,steps_codes)
        
        steps_out= zip(steps,steps_desc,steps_codes)
        print("saving to pickle file")
        pickle.dump([experiments,current_experiment,commands,settings,code_output_msg,generated_code_dict], open(filepath, 'wb'))
        rendered=render_to_string('py_ml_studio/steps_list.html', {'steps':steps_out}) 
        return HttpResponse(json.dumps(rendered), content_type='application/json')

'''
Creating new Project/ Open existing project from the  File menu
'''
def load_project(request,filepath):
    print("load_project is invoked!")
    #print("file path is "+ filepath)
    # get current directory
    path = os.getcwd()
    #print(os.listdir("/Users"))
    #print("Current Directory is ", path)   
    result=""
    df=pd.DataFrame()
    plot_type=""; plt_encoded=""
    stat_type=""
    current_experiment=""
    code_output_msg=[]
    experiments=[]
    steps,steps_desc,steps_codes = [],[],[]
    generated_code_dict={}
    commands=[]
    settings={}
    
    try: #load experiments 
        project_file=open(filepath, 'rb')
        print("loading the project pickle file")
        if project_file: experiments,current_experiment,commands,settings,code_output_msg,generated_code_dict= pickle.load(project_file)  
        if experiments:
            steps,steps_desc,steps_codes=exp.get_experiment_info(experiments,current_experiment)
            #print("steps_codes are: " ,steps_codes)
        if not commands: commands=[]
        if not code_output_msg: code_output_msg=[]
        if not settings: settings={}
        
        #if not generated_code_dict: ##UPDATE :load the source code every time
        generated_code_dict=load_generated_code_dict()
        
        if not current_experiment: 
            current_experiment=""
            '''
            generate the js tree nodes from the notebook source code template
            '''
            generate_tree_view_json_data(path+"/py_ml_studio/static/py_ml_studio/")
    
    except FileNotFoundError: 
        print("project file not found")

        ## if it is a new project then create experiment_0 by default.
        print("new experiment was pressed")
        experiment_id="experiment_"+str(len(experiments))
        print("current experiment is "+ experiment_id)
        current_experiment=experiment_id
        steps,steps_desc,steps_codes=[],[],[]
        commands.append(experiment_id)
        experiment=exp.Experiment(experiment_id)
        experiments.append(experiment)
        pickle.dump([experiments,current_experiment,commands,settings,code_output_msg,generated_code_dict],open(filepath, 'wb'))
            
    '''
    handling post requests
    '''
    if request.method == 'POST':
            
        delete_exp = request.POST.get('delete_experiment')
        if delete_exp: ## delete current experiment
            print("user requested to delete the current experiement "+current_experiment )
            experiments= exp.delete_experiment(experiments,current_experiment)
            if current_experiment in commands:
                commands.remove(current_experiment) ## delete the associated command.
    
            ## change the current experiment to the first experiement in the list after deleting the current one.
            if experiments:
                pickle.dump([experiments,experiments[0].id,commands,settings,code_output_msg,generated_code_dict], open(filepath, 'wb'))
            else:
                pickle.dump([[],"",commands,settings,code_output_msg,generated_code_dict], open(filepath, 'wb'))    
            return HttpResponseRedirect(request.path_info)
         
        '''
        getting plot type
        '''
        plot_type=request.POST.get('plot_type')
        
        '''
        getting stats type
        '''
        stat_type=request.POST.get('stat_type')
        #print(stat_type)
        
        '''
        experiments commands
        '''
        command_selected = request.POST.get('command_selected')
        
        if command_selected:
            if(command_selected=="new experiment"):
                print("new experiment was pressed")
                experiment_id="experiment_"+str(len(experiments))
                #print("current experiment is "+ experiment_id)
                current_experiment=experiment_id
                steps,steps_desc,steps_codes=[],[],[]
                commands.append(experiment_id)
                experiment=exp.Experiment(experiment_id)
                experiments.append(experiment)
                pickle.dump([experiments,current_experiment,commands,settings,code_output_msg,generated_code_dict],open(filepath, 'wb'))
            
            elif(command_selected=="copy current experiment"):
                if current_experiment:
                    print("copy current experiment was pressed")
                    experiment_id="experiment_"+str(len(experiments))
                    #print("current experiment is "+ experiment_id)
                    current_experiment=experiment_id
                    commands.append(experiment_id)
                    experiment=exp.Experiment(experiment_id)
                    experiment.steps=steps; experiment.steps_desc=steps_desc; experiment.steps_codes=steps_codes;
                    experiments.append(experiment)
                    pickle.dump([experiments,current_experiment,commands,
                                 settings,code_output_msg,generated_code_dict],open(filepath, 'wb'))
                    
            elif(command_selected.startswith("experiment_")):
                current_experiment=command_selected
                #print("specific "+ current_experiment+ " was pressed")
                steps,steps_desc,steps_codes=exp.get_experiment_info(experiments,current_experiment)
            else: pass
            
        ''' 
        save experiment steps
        '''    
        new_steps = request.POST.get('steps')
        if new_steps:
            if new_steps=="empty":
                print("the experiment has no steps to save!")
                steps=[];steps_desc=[];steps_codes=[]
            else:
                steps=new_steps.split(',')
                steps_desc=request.POST.get('steps_desc').split('%%%')
                steps_codes=request.POST.get('steps_codes').split('%%%')
        
        '''
        export experiment into notebook
        '''
        exported_steps = request.POST.get('exported_steps')
        if exported_steps:
            if exported_steps=="empty":
                print("the experiment has no steps to export!")
            else:
                #print("here exported steps " + exported_steps.split(',')[0])
                exported_steps=exported_steps.split(',')
                exported_steps_desc=request.POST.get('exported_steps_desc').split('%%%')
                exported_steps_codes=request.POST.get('exported_steps_codes').split('%%%')   
                filepath=request.POST.get('filepath')
                #print(filepath)
                experiment_name=request.POST.get('experiment_name')     
                
                export_experiment_to_notebook(exported_steps,exported_steps_desc,exported_steps_codes,
                                              filepath,experiment_name)     
        '''
        run commands 
        '''
        run_step = request.POST.get('run_step')
        if run_step:
            print("run_step is invoked!")
            try:
                result=kernel.execute_code([run_step])
                code_output_msg=result
                #print("codoutputmsg "+ str(len(code_output_msg)))
                pickle.dump([experiments,current_experiment,commands,settings,code_output_msg,generated_code_dict], 
                            open(filepath, 'wb'))
            except Exception as e:
                print("run step exception:"+str(e))
                code_output_msg=str(e)
            
            return HttpResponse(json.dumps("\n".join(code_output_msg)), content_type='application/json')    
        
        run_all_above=request.POST.get("run_all_steps_codes")
        if run_all_above:
            print("run all above steps codes " + run_all_above)
            try:
                result=kernel.execute_code(run_all_above.split("%%%"))
                #code_output_msg.extend(result)
                code_output_msg=result
                pickle.dump([experiments,current_experiment,commands,settings,code_output_msg,generated_code_dict], 
                            open(filepath, 'wb'))
            except Exception as e:
                print("run all above exception: "+str(e))
                code_output_msg=str(e)
            ##code_output_msg[::-1] for reversing the message output
            return HttpResponse(json.dumps("\n".join(code_output_msg)), content_type='application/json')    
            
    ## update the experiment steps    
    exp.update_experiment_steps(experiments,current_experiment,steps,steps_desc,steps_codes)
    
    ##load the data frame
    #df=get_data_frame()
    
    if stat_type!="" and stat_type is not None :
        df=get_data_frame()
        return HttpResponse(json.dumps(get_stats_html(df,stat_type)), content_type='application/json')
        #content["stats"]=get_stats_html(df,stat_type)
        
    if plot_type!="" and plot_type is not None:
        df=get_data_frame();
        plt_encoded=plot_vizualisation(df,plot_type);
        return HttpResponse(json.dumps(plt_encoded), content_type='application/json')
        #content["plt_encoded"]=plot_vizualisation(df,plot_type)

    '''
    convert dataframe to readable html content
    '''      
    #pd.DataFrame.to_html(df, max_rows=20, max_cols=100, justify='justify-all', show_dimensions=True, bold_rows=False)"])[0]
    frame_html = pd.DataFrame.to_html(df, max_rows=20, max_cols=100, justify='justify-all', show_dimensions=True, bold_rows=False)
    frame_html = frame_html.replace('<table border="1" class="dataframe">', '<table border="1" class="table table-sm table-responsive">')
    
    content = {}
    content['dataframe'] = frame_html   
    content['commands'] = commands
    content['steps'] = zip(steps,steps_desc,steps_codes)
    content['current_experiment'] = current_experiment
    content["code_output_msg"]="\n".join(code_output_msg[::-1])


    ## save it into the project file
    print("saving to the project pickle file")
    pickle.dump([experiments,current_experiment,commands,settings,code_output_msg,generated_code_dict], open(filepath, 'wb'))
    
    return render(request, 'py_ml_studio/index.html', context=content)

'''
reload the source code template from the settings menu
'''
def reload_source_code_jstree_nodes_template(request):
    print("reload_source_code_jstree_nodes_template is inoked!")
    path = os.getcwd()

    '''
    generate the js tree nodes from the notebook source code template
    '''
    generate_tree_view_json_data(path+"/py_ml_studio/static/py_ml_studio/")
    
    return HttpResponseRedirect("/mlstudio")

# Default View
def index(request):
    path=request.GET.get('dir', os.path.expanduser("~/Documents"))
    path=path.replace("\\","/")
    if path!="":
        files_list= get_project_files_directories_list(path)
        content={}
        content['current_directory'] = path
        content["files_list"]=files_list
        return render(request, 'py_ml_studio/home.html',context=content)
    else:
        return render(request, 'py_ml_studio/home.html')
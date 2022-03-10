from django.shortcuts import render
from django.http import HttpResponseRedirect
import numpy as np
import pandas as pd
import pickle
import time
'''
import modules
'''
from  service.eda_plotting import plot_vizualisation
import service.experiments_controller as exp
from  service.experiments_controller import Experiment
from service.eda_stats import get_stats_html
from service.code_generation import load_generated_code_dict
import service.jupyter_kernel_executor as kernel

# Create your views here.
def index(request):
    
    '''
    read dataframe from temp dictionary
    '''
    import os
 
    # get current directory
    path = os.getcwd()
    #print("Current Directory", path)
    ##df = pd.read_pickle(path+"/web_app/"+'temp/tmp.pkl')
    generated_code_dict=load_generated_code_dict()
    done=True;result=""
    toggle_code=None
    plot_type=""
    stat_type=""
    current_experiment=""
    code_output_msg=[]
    experiments=[]
    steps,steps_desc,steps_codes = [],[],[]
    new_step_generated_code,new_step_generated_desc="",""
    name = 'blub';df=pd.DataFrame();
    commands=["new_experiment"]
    settings={"toggle_code":False}
    ##load experiments 
    try:
        project_file=open(path+"/web_app/"+'temp/project.pickle', 'rb')
        print("loading the pickle file")
        if project_file: experiments,current_experiment,commands,settings,code_output_msg= pickle.load(project_file)  
        if experiments:  
            steps,steps_desc,steps_codes=exp.get_experiment_info(experiments,current_experiment)
            print("steps_codes are: " ,steps_codes)
        if not commands: commands=["new_experiment"]
        if not code_output_msg: code_output_msg=[]
        if not settings: settings={"toggle_code":False}
    except FileNotFoundError: print("project file not found")    

    '''
    manipulate dataframe
    '''
    if request.method == 'POST':
            
        delete_exp = request.POST.get('delete_experiment')
        if delete_exp: ## delete current experiment
            print("user requested to delete the current experiement "+current_experiment )
            experiments= exp.delete_experiment(experiments,current_experiment)
            if current_experiment in commands:
                commands.remove(current_experiment) ## delete the associated command.
            #print("experiments list after delete")
            #print(experiments)
            ## change the current experiment to the first experiement in the list after deleting the current one.
            if experiments:
                pickle.dump([experiments,experiments[0].id,commands,settings,code_output_msg], open(path+"/web_app/"+'temp/project.pickle', 'wb'))
            else:
                pickle.dump([[],"",commands,settings,code_output_msg], open(path+"/web_app/"+'temp/project.pickle', 'wb'))    
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
        toggling code
        '''
        toggle_code=request.POST.get('toggle_code')
        if toggle_code:
            old_val=settings.get("toggle_code")
            ##print("old val is "+ str(old_val))
            settings["toggle_code"]=not old_val
            toggle_code=not old_val
        
        '''
        experiments commands
        '''
        command_selected = request.POST.get('command_selected')
        if command_selected:
            if(command_selected=="new_experiment"):
                print("new experiment was pressed")
                experiment_id="experiment_"+str(len(experiments))
                print("current experiment is "+ experiment_id)
                current_experiment=experiment_id
                steps,steps_desc,steps_codes=[],[],[]
                commands.append(experiment_id)
                experiment=exp.Experiment(experiment_id)
                experiments.append(experiment)
                pickle.dump([experiments,current_experiment,commands,settings,code_output_msg],open(path+"/web_app/"+'temp/project.pickle', 'wb'))
            
            elif(command_selected.startswith("experiment_")):
                current_experiment=command_selected
                print("specific "+ current_experiment+ " was pressed")
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
                print("here new updated steps " + new_steps.split(',')[0])
                steps=new_steps.split(',')
                steps_desc=request.POST.get('steps_desc').split(',')
                steps_codes=request.POST.get('steps_codes').split(',')
        '''
        experiment step
        '''
        new_step = request.POST.get('new_step')
        if new_step:
            print("step_selected is: "+ new_step)

            steps.append(new_step)
            
            """ res = cmd_handler.input_command(new_step, {'filepath':path+"/web_app/"+'temp/work_file.csv'})
            if res:
                if 'dataframe' in res:
                    df = res['dataframe'] """
        
            if(new_step in generated_code_dict):
                new_step_generated_desc=generated_code_dict[new_step]["step_desc"]
                new_step_generated_code=generated_code_dict[new_step]["step_code"]
                #print(generated_code_dict[new_step]["code"])
                #print(generated_code_dict[new_step]["desc"])
                steps_desc.append(new_step_generated_desc)
                steps_codes.append(new_step_generated_code)
            else:
                steps_desc.append("")
                steps_codes.append("")
            
        '''
        run commands 
        '''
        res = request.POST.get('start')
        
        if res == 'run':
            """ cnt = df.shape[0]
            name = chr(np.random.randint(200))
            df[name] = np.random.randint(10, size=cnt) """
            
            try:
                done,result=kernel.execute_code([request.POST.get("step_code")])
                code_output_msg.extend(result)
            except Exception as e:
                print("run step exception:"+str(e))
                code_output_msg.append(str(e))
                
        if res == 'remove':
            try:
                kernel.execute_code(["df.drop(df.columns[-1], axis='columns', inplace=True)"])
            except Exception as e:
                print(str(e))
                code_output_msg.append(str(e))
        
        run_all_above=request.POST.get("run_all_steps_codes")
        
        if run_all_above:
            done=False
            print("run all above steps codes " + run_all_above)
            try:
                done,result=kernel.execute_code([run_all_above])
                code_output_msg.extend(result)
                print("just right after execute run all above")
                print("codoutputmsg "+ str(len(code_output_msg)))
                #time.sleep(2)
                #print("just right after sleep")
                
            except Exception as e:
                print("run all above exception: "+str(e))
                code_output_msg.append(str(e))
    
    ##print("steps_codes here : " ,steps_codes)
            
    ## update the experiment steps
    exp.update_experiment_steps(experiments,current_experiment,steps,steps_desc,steps_codes)
    print('steps:',steps)
    print('steps_desc:',steps_desc)
    print('steps_code:',steps_codes)
    print("commands:",commands)
    
    
    '''
    convert dataframe to readable html content
    '''
    content = {}
    try:
        if done:
            #pass
            done,frame_json=kernel.execute_code(["pd.DataFrame.to_json(df,orient='columns')"])
            frame_json= frame_json[0]          
            df=pd.read_json(frame_json[1:-1],orient='columns')
    except Exception as e:
                print("data frame to json exception: "+str(e))
                code_output_msg.append(str(e))
                
    #pd.DataFrame.to_html(df, max_rows=20, max_cols=100, justify='justify-all', show_dimensions=True, bold_rows=False)"])[0]
    frame_html = pd.DataFrame.to_html(df, max_rows=20, max_cols=100, justify='justify-all', show_dimensions=True, bold_rows=False)
    frame_html = frame_html.replace('<table border="1" class="dataframe">', '<table border="1" class="table table-sm table-responsive">')
    
    #content['attributes'] = []
    content['dataframe'] = frame_html
    
    if toggle_code is not None :
         content["toggle_code"]=toggle_code
         
    if stat_type!="" and stat_type is not None :
        content["stats"]=get_stats_html(df,stat_type)
        
    if plot_type!="" and plot_type is not None:
        content["plt_encoded"]=plot_vizualisation(df,plot_type)
        
    content['commands'] = commands
    
    #steps=["test this"]
    #steps_desc=["step des"]
    #steps_codes=[""]
    
    content['steps'] = zip(steps,steps_desc,steps_codes)
    content['current_experiment'] = current_experiment
    content["code_output_msg"]="\n".join(code_output_msg[::-1])
    ##content["new_step_generated_code"]=new_step_generated_code
    ##content["new_step_generated_desc"]=new_step_generated_desc

    ## save it into the project file
    print("saving to pickle file")
    pickle.dump([experiments,current_experiment,commands,settings,code_output_msg], open(path+"/web_app/"+'temp/project.pickle', 'wb'))
    
    '''
    save changed dataframe in temp dictionary
    '''
    #pd.to_pickle(df, path+"/web_app/"+'temp/tmp.pkl')
    print("just right before render")
    if done:
        return render(request, 'py_data_analysis_code_generator/index.html', context=content)
    else:
        pass
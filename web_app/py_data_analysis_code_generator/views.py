#from copyreg import pickle
from ast import Try
from cmath import exp
from distutils import command
from turtle import st
from django.shortcuts import render
from django.http import HttpResponseRedirect
import numpy as np
import pandas as pd
import pickle


'''
import modules
'''
from service.mods_panda import Commands
from  service.eda_plotting import plot_vizualisation
import service.experiments_controller as exp
from  service.experiments_controller import Experiment
from service.eda_stats import get_stats_html

cmd_handler = Commands()

# Create your views here.
def index(request):
    
    '''
    read dataframe from temp dictionary
    '''
    import os
 
    # get current directory
    path = os.getcwd()
    #print("Current Directory", path)
    df = pd.read_pickle(path+"/web_app/"+'temp/tmp.pkl')

    plot_type=""
    stat_type=""
    current_experiment=""
    code_exception_msg=""
    experiments=[]
    steps = []
    name = 'blub'
    commands=["new_experiment"]
    ##load experiments
    try:
        project_file=open(path+"/web_app/"+'temp/project.pickle', 'rb')
        if project_file: experiments,current_experiment,commands= pickle.load(project_file)  
        if experiments:  steps=exp.get_experiment_info(experiments,current_experiment)
        if not commands: commands=["new_experiment"]
    except FileNotFoundError: print("project file not found")    

    print(experiments)  
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
            print("experiments list after delete")
            print(experiments)
            ## change the current experiment to the first experiement in the list after deleting the current one.
            if experiments:
                pickle.dump([experiments,experiments[0].id,commands], open(path+"/web_app/"+'temp/project.pickle', 'wb'))
            else:
                pickle.dump([[],"",commands], open(path+"/web_app/"+'temp/project.pickle', 'wb'))    
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
        
        new_step = request.POST.get('new_step')
        if new_step:
            print("step_selected is: "+ new_step)
            if(new_step=="new_experiment"):
                print("new experiment was pressed")
                experiment_id="experiment_"+str(len(experiments))
                print("current experiment is "+ experiment_id)
                commands.append(experiment_id)
                experiment=exp.Experiment(experiment_id,[],[],[])
                experiments.append(experiment)
                pickle.dump([experiments,current_experiment,commands],open(path+"/web_app/"+'temp/project.pickle', 'wb'))
            
            elif(new_step.startswith("experiment_")):
                current_experiment=new_step
                print("specific "+ current_experiment+ " was pressed")
                steps=exp.get_experiment_info(experiments,current_experiment)
            else: ## all other commands
                steps.append(new_step)
                res = cmd_handler.input_command(new_step, {'filepath':path+"/web_app/"+'temp/work_file.csv'})
                if res:
                    if 'dataframe' in res:
                        df = res['dataframe']
        
        res = request.POST.get('start')
        
        if res == 'apply':
            cnt = df.shape[0]
            name = chr(np.random.randint(200))
            df[name] = np.random.randint(10, size=cnt)
            print(request.POST.get("step_cell_txtarea"))
            try:
                exec(request.POST.get("step_cell_txtarea"))
                
            except Exception as e:
                print(str(e))
                code_exception_msg=str(e)
                
        if res == 'remove':
            df.drop(df.columns[-1], axis='columns', inplace=True)
    
    ## update the experiment steps
    exp.update_experiment_steps(experiments,current_experiment,steps)
    print('steps:',steps)
    print("commands:",commands)
    #print(experiments)
    ## save it into the project file
    pickle.dump([experiments,current_experiment,commands], open(path+"/web_app/"+'temp/project.pickle', 'wb'))
    
    '''
    convert dataframe to readable html content
    '''

    content = {}
    frame_html = pd.DataFrame.to_html(df, max_rows=9, max_cols=10, justify='justify-all', show_dimensions=True, bold_rows=False)
    frame_html = frame_html.replace('<table border="1" class="dataframe">', '<table border="1" class="table table-sm">')
    
    content['attributes'] = []
    content['dataframe'] = frame_html
    if stat_type!="":
        content["stats"]=get_stats_html(df,stat_type)
    if plot_type!="":
        content["plt_encoded"]=plot_vizualisation(df,plot_type)
    content['commands'] = commands
    content['steps'] = steps
    content['current_experiment'] = current_experiment
    
    content["code_exception_msg"]=code_exception_msg
    #print(content)
    '''
    save changed dataframe in temp dictionary
    '''
    pd.to_pickle(df, path+"/web_app/"+'temp/tmp.pkl')

    return render(request, 'py_data_analysis_code_generator/index.html', context=content)   
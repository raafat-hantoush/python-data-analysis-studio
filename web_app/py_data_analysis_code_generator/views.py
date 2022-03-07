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
from io import StringIO
from contextlib import redirect_stdout

'''
import modules
'''
from service.mods_panda import Commands
from  service.eda_plotting import plot_vizualisation
import service.experiments_controller as exp
from  service.experiments_controller import Experiment
from service.eda_stats import get_stats_html
from service.feature_selection import feature_selection_code_dict
import service.jupyter_kernel_executor as kernel
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

    toggle_code=None
    plot_type=""
    stat_type=""
    current_experiment=""
    code_exception_msg=""
    experiments=[]
    steps = []
    new_step_generated_code=""
    name = 'blub'
    commands=["new_experiment"]
    settings={"toggle_code":False}
    ##load experiments
    try:
        project_file=open(path+"/web_app/"+'temp/project.pickle', 'rb')
        if project_file: experiments,current_experiment,commands,settings= pickle.load(project_file)  
        if experiments:  steps=exp.get_experiment_info(experiments,current_experiment)
        if not commands: commands=["new_experiment"]
        if not settings: settings={"toggle_code":False}
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
                pickle.dump([experiments,experiments[0].id,commands,settings], open(path+"/web_app/"+'temp/project.pickle', 'wb'))
            else:
                pickle.dump([[],"",commands,settings], open(path+"/web_app/"+'temp/project.pickle', 'wb'))    
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
                steps=[]
                commands.append(experiment_id)
                experiment=exp.Experiment(experiment_id)
                experiments.append(experiment)
                pickle.dump([experiments,current_experiment,commands,settings],open(path+"/web_app/"+'temp/project.pickle', 'wb'))
            
            elif(command_selected.startswith("experiment_")):
                current_experiment=command_selected
                print("specific "+ current_experiment+ " was pressed")
                steps=exp.get_experiment_info(experiments,current_experiment)
            else: pass
            
        '''
        experiment step
        '''
        new_step = request.POST.get('new_step')
        if new_step:
            print("step_selected is: "+ new_step)

            steps.append(new_step)
            res = cmd_handler.input_command(new_step, {'filepath':path+"/web_app/"+'temp/work_file.csv'})
            if res:
                if 'dataframe' in res:
                    df = res['dataframe']
        
        if(new_step in feature_selection_code_dict):
            new_step_generated_code=feature_selection_code_dict[new_step]["code"]
            ## populate the 
            print(feature_selection_code_dict[new_step]["code"])
        
        res = request.POST.get('start')
        
        if res == 'run':
            cnt = df.shape[0]
            name = chr(np.random.randint(200))
            df[name] = np.random.randint(10, size=cnt)
            print(request.POST.get("step_cell_txtarea"))
            try:
                
                code_exception_msg= "\n".join(kernel.execute_code([request.POST.get("step_cell_txtarea")]))
                """ print(exec(request.POST.get("step_cell_txtarea")))
                f = StringIO()
                with redirect_stdout(f):
                    print(exec(request.POST.get("step_cell_txtarea")))
                s = f.getvalue()
                print(s)
                code_exception_msg=str(s) """
                
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
    pickle.dump([experiments,current_experiment,commands,settings], open(path+"/web_app/"+'temp/project.pickle', 'wb'))
    
    '''
    convert dataframe to readable html content
    '''

    content = {}
    frame_html = pd.DataFrame.to_html(df, max_rows=7, max_cols=100, justify='justify-all', show_dimensions=True, bold_rows=False)
    frame_html = frame_html.replace('<table border="1" class="dataframe">', '<table border="1" class="table table-dark table-sm table-responsive">')
    
    content['attributes'] = []
    content['dataframe'] = frame_html
    
    if toggle_code is not None :
         content["toggle_code"]=toggle_code
         
    if stat_type!="" and stat_type is not None :
        content["stats"]=get_stats_html(df,stat_type)
        
    if plot_type!="" and plot_type is not None:
        content["plt_encoded"]=plot_vizualisation(df,plot_type)
        
    content['commands'] = commands
    content['steps'] = steps
    content['current_experiment'] = current_experiment
    
    content["code_exception_msg"]=code_exception_msg
    
    content["new_step_generated_code"]=new_step_generated_code
    #print(content)
    '''
    save changed dataframe in temp dictionary
    '''
    pd.to_pickle(df, path+"/web_app/"+'temp/tmp.pkl')

    return render(request, 'py_data_analysis_code_generator/index.html', context=content)
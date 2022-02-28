#from copyreg import pickle
from ast import Try
from cmath import exp
from distutils import command
from django.shortcuts import render
from django.http import HttpResponseRedirect
import numpy as np
import pandas as pd
import pickle


'''
import modules
'''
from service.mods_panda import Commands

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

    current_experiment="experiment_0"
    experiments=[]
    steps = []
    name = 'blub'
    commands=['set_data', 'reset', 'add', 'remove',"filling Missing values","new_experiment"]
    ##load experiments
    try:
        project_file=open(path+"/web_app/"+'temp/project.pickle', 'rb')
        if project_file: experiments,current_experiment,commands= pickle.load(project_file)  
        if experiments:  steps=get_experiment_info(experiments,current_experiment)
        if not commands: commands=['set_data', 'reset', 'add', 'remove',"filling Missing values","new_experiment"]
    except FileNotFoundError: print("project file not found")    

    print(experiments)  
    '''
    manipulate dataframe
    '''
    if request.method == 'POST':
        delete_exp = request.POST.get('delete_experiment')
        if delete_exp: ## delete current experiment
            print("user requested to delete the current experiement "+current_experiment )
            experiments= delete_experiment(experiments,current_experiment)
            if current_experiment in commands:
                commands.remove(current_experiment) ## delete the associated command.
            ## change the current experiment to the first experiement in the list after deleting the current one.
            if experiments:
                pickle.dump([experiments,experiments[0].id,commands], open(path+"/web_app/"+'temp/project.pickle', 'wb'))
            else:
                pickle.dump([[],"",commands], open(path+"/web_app/"+'temp/project.pickle', 'wb'))    
            return HttpResponseRedirect(request.path_info)
        
        new_step = request.POST.get('choice')
        if new_step:
            if(new_step=="new_experiment"):
                print("new experiment was pressed")
                experiment_id="experiment_"+str(len(experiments))
                print("current experiment is "+ experiment_id)
                commands.append(experiment_id)
                experiment=Experiment(experiment_id,[],[],[])
                experiments.append(experiment)
                pickle.dump([experiments,current_experiment,commands],open(path+"/web_app/"+'temp/project.pickle', 'wb'))
            
            elif(new_step.startswith("experiment_")):
                current_experiment=new_step
                print("specific "+ current_experiment+ " was pressed")
                steps=get_experiment_info(experiments,current_experiment)
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
            
        if res == 'remove':
            df.drop(df.columns[-1], axis='columns', inplace=True)
    
    ## update the experiment steps
    update_experiment_steps(experiments,current_experiment,steps)
    print('steps:',steps)
    print("commands:",commands)
    print(experiments)
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
    content['commands'] = commands
    content['steps'] = steps
    content['current_experiment'] = current_experiment
    #print(content)
    '''
    save changed dataframe in temp dictionary
    '''
    pd.to_pickle(df, path+"/web_app/"+'temp/tmp.pkl')

    return render(request, 'py_data_analysis_code_generator/index.html', context=content)   

def update_experiment_steps(experiments,experiment_id,steps):
    for ind,Experiment in enumerate(experiments):
        if(Experiment.id==experiment_id): 
            Experiment.steps=steps
            experiments[ind]=Experiment
     
def get_experiment_info(experiments,experiment_id):
    for Experiment in experiments:
        if(Experiment.id==experiment_id): 
            return Experiment.steps
    
    return []

def delete_experiment(experiments,experiment_id):
    for ind,Experiment in enumerate(experiments):
        if(Experiment.id==experiment_id): 
            del experiments[ind]
            return experiments
        else:
            return experiments  ## Experiment not found!

class Experiment:
    def __init__(self,id,steps=[],steps_codes=[],commands=[],description=[]):
        self.id = id   
        self.steps=steps
        self.steps_codes=steps_codes
        self.description=description
        self.commands=commands ## NOT used for noew
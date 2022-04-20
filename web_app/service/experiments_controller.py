
'''
This handler manipulate the experiments list 
experiments is a list of Expirement objects
''' 
def update_experiment_steps(experiments,experiment_id,steps,steps_desc,steps_codes):
    for ind,Experiment in enumerate(experiments):
        if(Experiment.id==experiment_id): 
            #print("found the experiment to be updated "+ Experiment.id )
            Experiment.steps=steps
            Experiment.steps_desc=steps_desc
            Experiment.steps_codes=steps_codes
            experiments[ind]=Experiment

def print_experiments(experiments):
    for exper in experiments:
        print(exper.id)
        for step in exper.steps:
            print(step)
            
def get_experiment_info(experiments,experiment_id):
    for Experiment in experiments:
        if(Experiment.id==experiment_id): 
            return Experiment.steps.copy(),Experiment.steps_desc.copy(),Experiment.steps_codes.copy()
    
    return [],[],[]

def delete_experiment(experiments,experiment_id):
    for ind,Experiment in enumerate(experiments):
        if(Experiment.id==experiment_id): 
            del experiments[ind]
            return experiments
    
    return experiments  ## Experiment not found!

'''
Experiment Class definition
'''
class Experiment:
    def __init__(self,id,steps=[],steps_desc=[],steps_codes=[],description=[]):
        self.id = id   
        self.steps=steps
        self.steps_desc=steps_desc
        self.steps_codes=steps_codes
        self.description=description

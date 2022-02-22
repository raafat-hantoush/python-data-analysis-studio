#from copyreg import pickle
from django.shortcuts import render
import numpy as np
import pandas as pd
import pickle


'''
import modules
'''
from service.mods_panda import Commands

#df = pd.read_csv('temp/work_file.csv')
#df = pd.DataFrame({"name":["Kike","Nelson","Rafa","Denny"],"Age":[19,18,22,31]})
#df.to_pickle('temp/tmp.pkl')


steps = []
name = 'blub'
cmd_handler = Commands()


#steps = pickle.load(open('temp/steps.p', 'rb'))

# Create your views here.
def index(request):
    
    '''
    read dataframe from temp dictionary
    '''
    df = pd.read_pickle('temp/tmp.pkl')

    '''
    manipulate dataframe
    '''
    if request.method == 'POST':
        new_button = request.POST.get('choice')
        if new_button:
            steps.append(new_button)
            res = cmd_handler.input_command(new_button, {'filepath':'temp/work_file.csv'})
            if res:
                if 'dataframe' in res:
                    df = res['dataframe']
            
        
        res = request.POST.get('start')
        
        if res == 'apply':
            #index = pd.DataFrame.
            cnt = df.shape[0]
            name = chr(np.random.randint(200))
            df[name] = np.random.randint(10, size=cnt)
            
        if res == 'remove':
            df.drop(df.columns[-1], axis='columns', inplace=True)
        
    
    #print(df)
    print('steps:',steps)
    pickle.dump(steps, open('temp/steps.p', 'wb'))
    
    '''
    convert dataframe to readable html content
    '''

    content = {}
    frame_html = pd.DataFrame.to_html(df, max_rows=9, max_cols=10, justify='justify-all', show_dimensions=True, bold_rows=False)
    frame_html = frame_html.replace('<table border="1" class="dataframe">', '<table border="1" class="table table-sm">')
    
    content['attributes'] = []
    content['dataframe'] = frame_html
    content['commands'] = ['set_data', 'reset', 'add', 'remove']
    content['steps'] = steps
    #print(content)
    '''
    save changed dataframe in temp dictionary
    '''
    pd.to_pickle(df, 'temp/tmp.pkl')

    return render(request, 'py_data_analysis_code_generator/index.html', context=content)    
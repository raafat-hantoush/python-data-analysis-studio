## Code generation
import json
import os
 
# get current directory
path = os.getcwd()
    
def read_notebook_file_cell_sources(file_path):
    cells_sources=[]
    with open(file_path) as f:
      data = json.load(f)

    for cell in data["cells"]:
        if len(cell["source"])!=0:
            cells_sources.append(cell["source"])
    return cells_sources

def parse_cells_sources(cells_sources):
    cells_code_dict={};step_id="";step_name="";step_type="";step_desc="";step_code=""
    for cell in cells_sources:
        ## handle step_name
        if len(cell)>4 :
            if len(cell[0])>9:
                ## handle step_id
                print(cell[0][9:-1])
                step_id=cell[0][9:-1]
            else: step_id=""
                
            if len(cell[1])>11:
                print(cell[1][11:-1])
                step_name=cell[1][11:-1]
            else: step_name=""
                
            #handle step_type
            if len(cell[2])>11:
                print(cell[2][11:-1])
                step_type=cell[2][11:-1]
            else: step_type=""

            #handle step_desc
            if len(cell[3])>11:
                print(cell[3][11:-1])
                step_desc=cell[3][11:-1]
            else: step_desc=""

            # handle step_code
            print("".join(cell[4:]))
            step_code="".join(cell[4:])
        else:
            step_id="";step_name="";step_type="";step_desc="";step_code=""

        if step_id!="" :
            cells_code_dict[step_id]={}
            cells_code_dict[step_id]["step_id"]=step_id
            cells_code_dict[step_id]["step_name"]=step_name
            cells_code_dict[step_id]["step_type"]=step_type
            cells_code_dict[step_id]["step_desc"]=step_desc
            cells_code_dict[step_id]["step_code"]=step_code

    return cells_code_dict

def load_generated_code_dict():
    cells_sources = read_notebook_file_cell_sources(path+"/service/code_generation_source_template.ipynb")
    generated_code_dict=parse_cells_sources(cells_sources)
    return generated_code_dict

'''
generated code dictionary
'''



""" generated_code_dict={
    "drop_cols":
        {
            "name":"drop columns",
            "type":"feature_selection",
            "code":"pd.DataFrame.drop(df,columns=[\"\"],inplace=True)",
            "desc":"drop one or more columns from teh data frame."
        },
    "lower_cols":
        {
            "name":"lower columns",
            "type":"data_cleaning",
            "code":"df.columns= df.columns.str.lower()",
            "desc":"make the data frame columns a lower case."
        },
    
    "reset":
        {
            "name":"reset",
            "type":"import/export",
            "code":"df=pd.read_csv(\"Documents/GitHub/general/work_file.csv\")",
            "desc":"reload the original data frame from the csv file."
        },
    
    "import_required_libs":
        {
            "name":"import_required_libs",
            "type":"import/export",
            "code":"import pandas as pd;\nimport numpy as np;\n\
            ## plotting libraries\nfrom matplotlib import pyplot as plt\nimport seaborn as sns",
            "desc":"import the required python libraries"
        },
    
    "export_data_tocsv":
        {
            "name":"export_data_tocsv",
            "type":"import/export",
            "code":"df.to_csv ('', index = None, header=True)",
            "desc":"export pandas data frame to csv file"
        }
}
 """
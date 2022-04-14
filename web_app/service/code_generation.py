## Code generation
import json
import os
import configparser
import nbformat as nbf
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
                #print(cell[0][9:-1])
                step_id=cell[0][9:-1]
            else: step_id=""
                
            if len(cell[1])>11:
                #print(cell[1][11:-1])
                step_name=cell[1][11:-1]
            else: step_name=""
                
            #handle step_type
            if len(cell[2])>11:
                #print(cell[2][11:-1])
                step_type=cell[2][11:-1]
            else: step_type=""

            #handle step_desc
            if len(cell[3])>11:
                #print(cell[3][11:-1])
                step_desc=cell[3][11:-1]
            else: step_desc=""

            # handle step_code
            #print("".join(cell[4:]))
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
    ## read the path from the config file 
    config = configparser.ConfigParser()
    config.read(path +'/config.txt')
    source_code_template_path=path + "/" + config['DEFAULT']['Source_Code_Template_Path']
    
    cells_sources = read_notebook_file_cell_sources(source_code_template_path)
    generated_code_dict=parse_cells_sources(cells_sources)
    return generated_code_dict

def generate_tree_view_json_data(filepath):
    generated_code_dict=load_generated_code_dict()

    steps_types=[]; step_type="";tree=[];tree_node={}
    for key in generated_code_dict:
        tree_node={}
        step_type=generated_code_dict[key]["step_type"]    
        tree_node["id"]= generated_code_dict[key]["step_id"]
        tree_node["parent"]= step_type
        tree_node["text"]= generated_code_dict[key]["step_name"]  
        tree.append(tree_node)
        if step_type not  in steps_types:
            steps_types.append(step_type)

    for node in steps_types:
        tree_node={}
        tree_node["id"]= node
        tree_node["parent"]= "#"
        tree_node["text"]= node.replace("_"," ").title()
        tree.append(tree_node)

    with open(filepath+'tree_view_nodes.json', 'w') as outfile:
        json.dump(tree, outfile)
    return

'''
export an experiment to a notebook file
'''
def export_experiment_to_notebook(steps_names,steps_desc,steps_codes,filepath,experiment_name):
    nb = nbf.v4.new_notebook()
    for step_name, step_desc, step_code in zip(steps_names,steps_desc,steps_codes):
        nb['cells'].append(nbf.v4.new_markdown_cell("## "+step_name));
        nb['cells'].append(nbf.v4.new_markdown_cell("<b>"+step_desc));
        nb['cells'].append(nbf.v4.new_code_cell(step_code));
    
    nbf.write(nb, filepath + "_"+experiment_name +'.ipynb')
    print("experiment is exported successfully!")
    return 1
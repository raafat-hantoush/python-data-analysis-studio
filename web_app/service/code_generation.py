## Code generation
'''
generated code dictionary
'''
generated_code_dict={
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

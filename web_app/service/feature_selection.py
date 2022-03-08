## Feature Selection
'''
- dropping column/columns
- dropping highly correlated columns 
- feature selection using p-value
- recursive feature elimination RFE
'''

'''
dropping column
'''
feature_selection_code_dict={
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
            "type":"data_cleaning",
            "code":"df=pd.read_csv(\"Documents/GitHub/general/work_file.csv\")",
            "desc":"reload the original data frame from the csv file."
        }
}

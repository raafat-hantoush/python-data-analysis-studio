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
            "code":"pd.DataFrame.drop(df,columns=[\"zone\"],inplace=True)"
        },
    "lower_cols":
        {
            "name":"lower columns",
            "type":"data_cleaning",
            "code":"df.columns= df.columns.str.lower()"
        }
}

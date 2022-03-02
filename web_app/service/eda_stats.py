import pandas as pd
import io
"""_summary_
get descriptive stats about data
"""
    
def get_numerical_data_stats(df):
    if not df.empty:
        df=df._get_numeric_data()
        return df.describe()  
    else: return pd.DataFrame()

def get_categorical_data_stats(df):
    if not df.empty:
        df=df.select_dtypes(include="object")
        ## getting df.info()
        #buf = io.StringIO()
        #df.info(buf=buf)
        #s = buf.getvalue()
        #return s
        temp=""
        for column in df.columns:
            temp+= "---------------------------------\n"
            temp+=(df[[column]].value_counts().to_string()) + "\n"
        return temp
    else: return pd.DataFrame()

def get_stats_html(df,stat_type="numericals"):
    if stat_type=="numericals":
        df=get_numerical_data_stats(df)
    elif stat_type=="categoricals":   
        return get_categorical_data_stats(df)
    else: return ""
    if not df.empty: ## df is not empty
        frame_html = pd.DataFrame.to_html(df, max_rows=9, max_cols=10, justify='justify-all', show_dimensions=True, bold_rows=False)
        frame_html = frame_html.replace('<table border="1" class="dataframe">', '<table border="1" class="table table-sm">')
        return frame_html
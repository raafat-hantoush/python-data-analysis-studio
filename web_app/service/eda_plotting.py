## for visualization
from matplotlib import pyplot as plt; import seaborn as sns
import base64; from io import BytesIO
import pandas as pd
import numpy as np

'''
encoding the plot figure to embed it into HTML
'''
def plot_vizualisation(df,plot_type="hist",figsize=(9,8)):
    tmpfile = BytesIO()
    if plot_type=="hist":
        fig = df.hist(figsize=figsize)[0][0].get_figure()
    elif plot_type=="pairplot":
        fig= sns.pairplot(df).fig
    elif plot_type=="corr_heatmap":
        fig=plot_corr_heatmap(df,figsize)
    elif plot_type=="boxplot":
        fig=plot_boxplot(df,figsize=(19,24))
    else: 
        fig=plt.figure()
    plt.close(fig)
    ## save the figre to binary file     
    fig.savefig(tmpfile, format='png')
    ## encoding it using base64
    plt_encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    return plt_encoded

def plot_corr_heatmap(df,figsize):
    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=figsize)
        ax = sns.heatmap(corr, mask=mask,cmap='coolwarm', vmin=-1,vmax=1,annot=True, square=True)
    return ax.get_figure()

def plot_boxplot(df,figsize=(20,24)):
    df=df._get_numeric_data()  ## get ONLY  numeric data 
    fig, ax = plt.subplots(nrows=4,ncols=int(len(df.columns)/4)+1,figsize=figsize)
    col_ind=0
    for x in range(0, ax.shape[0]):
        for y in range(0, ax.shape[1]):
            sns.boxplot(ax=ax[x,y],y=df.iloc[:,col_ind])
            if col_ind == df.shape[1]-1: break;
            col_ind += 1 
    return fig
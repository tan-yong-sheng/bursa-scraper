from tkinter import Toplevel
import matplotlib.pyplot as plt
import streamlit as st
import pandas
from typing import Optional
import streamlit.components.v1 as components
import seaborn
import mpld3

def plot_fig(df: pandas.core.frame.DataFrame, period:int, x: str,y : str, legend:Optional[str]=None, normalize:bool = False):  
    # clean data and remove abnormal values
    fig = plt.figure()
    df = df.dropna()
    X = df[y]
    Y = df[x]
    if normalize: 
        df = df[X.between(X.quantile(0.05), X.quantile(0.95)) & Y.between(Y.quantile(0.05), Y.quantile(0.95))]
    # plot scatterplot
    if legend:
        scatter = seaborn.scatterplot(x=x, y=y,hue=legend, data=df,legend=True)
    elif not legend:
        scatter = seaborn.scatterplot(x=x, y=y, data=df, legend=True)   
    # Put the legend out of the figure
    plt.legend(bbox_to_anchor=(0.8, 1), loc='upper left', borderaxespad=0)
    fig_html = mpld3.fig_to_html(fig)
    components.html(fig_html, height=600, width=1000)
    #return fig

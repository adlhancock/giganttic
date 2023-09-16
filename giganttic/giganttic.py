# -*- coding: utf-8 -*-
"""
giganttic.py

a matplotlib gantt chart tool using patches, 
specifically designed for large projects
"""

import matplotlib.pyplot as plt

#import giganttic.import_fns as gim
#from giganttic.data_fns import filter_data
#from giganttic.plotting_fns import gantt_chart

from . import import_fns as gim
from .data_fns import filter_data
from .plotting_fns import gantt_chart

import os


#%% all in one function

def giganttic(inputfile: str | list = 'Auto',
              outputfile: str = 'Auto',
              title: str = 'Auto',
              filter: str | None = None,
              **kwargs):
    
    """
    all in one 'giganttic' function which takes an input and output path
    to import a range of filetypes and generate a giganntic gantt chart.
    
    Parameters
    ----------
    inputfile: str
        file location or list. Filetypes are .csv, .xlsx, or ms project .xml
    outputfile: str, optional
        where to save the output image. Default is current directory 
        and the input filename with .png extension
    title: str, optional
        Graph Title.
        Default is input filename
    filter: list or None, optional
        list containing column name string and regex string to use as a filter. 
        Default is None
    **kwargs:
        keyword arguments to be passed to giganttic.gantt_chart
    
    Returns
    -------
    df: pandas.DataFrame
    
    ax: matplotlib.axes._axes.Axes
        
    fig: matplotlib.figure.Figure
    
    
    """
    
    # import the data
    if inputfile == 'Auto':
        inputfile = gim.choosefile()
        
    if type(inputfile) is list:
        df = gim.import_list(inputfile)
    elif inputfile.endswith('.csv'):
        df = gim.import_csv(inputfile,**kwargs)
    elif inputfile.endswith('.xlsx'):
        df = gim.import_excel(inputfile,**kwargs)
    elif inputfile.endswith('.xml'):
        df = gim.import_mpp_xml(inputfile,**kwargs)
    else:
        raise ValueError("input must be list or string with path to .csv, .xlsx, or mpp .xml file")

    # create a default string to use for naming
    if isinstance(inputfile, str):
        defaultstring = os.path.basename(inputfile).rsplit('.')[-2]
    if isinstance(inputfile, list):
        defaultstring = 'gantt-chart'
    

    if title == 'Auto'    :
        title = defaultstring

    #filter and manipulate the data
    if filter is not None:
        df = filter_data(df,filter[0],filter[1])
        
    # plot the gantt chart
    ax, fig = gantt_chart(df,title=title,**kwargs)
    #fig.show()
    
    # save the figure
    if outputfile is not None:
        if outputfile == 'Auto':
            outputfile = '{}.png'.format(defaultstring)
        plt.savefig(outputfile)

    return df, ax, fig



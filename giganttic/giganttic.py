# -*- coding: utf-8 -*-
"""
giganttic.py

a matplotlib gantt chart tool using patches, 
specifically designed for large projects
"""

import matplotlib.pyplot as plt

from giganttic.import_fns import import_list, import_csv, import_excel
from giganttic.data_fns import filter_data
from giganttic.plotting_fns import gantt_chart


#%% all in one function

def giganttic(inputfile,outputfile,title,filter=None,**kwargs):
    """
    all in one giganttic fn
    """
    
    # import the data
    if type(inputfile) is list:
        df = import_list(inputfile)
    elif inputfile.endswith('.csv'):
        df = import_csv(inputfile,**kwargs)
    elif inputfile.endswith('xlsx'):
        df = import_excel(inputfile,**kwargs)
    else:
        raise ValueError("input must be list or string with path to .csv or .xlsx file")

    #filter and manipulate the data
    if filter is not None:
        df = filter_data(df,filter[0],filter[1])
        
    # plot the gantt chart
    ax, fig = gantt_chart(df,title=title,**kwargs)
    fig.show()
    
    # save the figure
    plt.savefig(outputfile)

    return df, fig
    


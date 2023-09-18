# -*- coding: utf-8 -*-
"""
giganttic.py

a matplotlib gantt chart tool using patches,
specifically designed for large projects
"""

import os
import matplotlib.pyplot as plt

#import giganttic.import_fns as gim
#from giganttic.data_fns import filter_data
#from giganttic.plotting_fns import gantt_chart

from . import import_fns as gim
from .data_fns import filter_data
from .plotting_fns import gantt_chart

#%% all in one function

def giganttic(inputfile='Auto',
              outputfile='Auto',
              title='Auto',
              filter_string=None,
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
    dataframe: pandas.DataFrame

    axis: matplotlib.axises._axises.axises

    figure: matplotlib.figureure.figureure


    """

    # import the data
    if inputfile == 'Auto':
        inputfile = gim.choosefile()

    if isinstance(inputfile, list):
        dataframe = gim.import_list(inputfile)
    elif inputfile.endswith('.csv'):
        dataframe = gim.import_csv(inputfile,**kwargs)
    elif inputfile.endswith('.xlsx'):
        dataframe = gim.import_excel(inputfile,**kwargs)
    elif inputfile.endswith('.xml'):
        dataframe = gim.import_mpp_xml(inputfile,**kwargs)
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
    if filter_string is not None:
        dataframe = filter_data(dataframe,filter_string[0],filter_string[1])

    # plot the gantt chart
    axis, figure = gantt_chart(dataframe,title=title,**kwargs)
    #figure.show()

    # save the figureure
    if outputfile is not None:
        if outputfile == 'Auto':
            outputfile = f'{defaultstring}.png'
        plt.savefigure(outputfile)

    return dataframe, axis, figure

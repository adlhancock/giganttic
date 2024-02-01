# -*- coding: utf-8 -*-
"""
giganttic.py

a matplotlib gantt chart tool using patches,
specifically designed for large projects
"""

import os
import matplotlib.pyplot as plt

import giganttic as gt

#%% all in one function

def giganttic(input_data='Auto',
              output_file='Auto',
              title='Auto',
              filter_string=None,
              plot_type='matplotlib',
              **kwargs):

    """
    all in one 'giganttic' function which takes an input and output path
    to import a range of filetypes and generate a giganntic gantt chart.

    Parameters
    ----------
    inputfile: str
        file location or list. Filetypes are .csv, .xlsx, or ms project .xml
    output_file: str, optional
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

    def import_data(input_data,**kwargs):
        # import the data

        # import a list
        if isinstance(input_data, list):
            dataframe = gt.import_list(input_data)
            inputfile = 'na'
        elif isinstance(input_data, str):
            inputfile = input_data
        else:
            raise ValueError("input must be list or string with path to file")

        if input_data == 'Auto':
            inputfile = gt.choosefile()
            input_data = inputfile
            print(f'DEBUG: {inputfile}')

        # import a file
        if inputfile == 'na':
            pass
        elif inputfile.endswith('.csv'):
            dataframe = gt.import_csv(inputfile,
                                       headers=kwargs.get('headers',True),
                                       columns=kwargs.get('columns',None))
        elif inputfile.endswith('.xlsx'):
            dataframe = gt.import_excel(inputfile,sheet = kwargs.get('sheet',0))
        elif inputfile.endswith('.xml'):
            dataframe = gt.import_mpp_xml(inputfile)
        else:
            raise ValueError(f"inputfile must be .csv, .xlsx, or mpp .xml file not {inputfile}")

        return dataframe

    def make_default_string(inputfile,title):
        # create a default string to use for naming
        if isinstance(inputfile, str) and os.path.exists(inputfile):
            defaultstring = os.path.basename(inputfile).rsplit('.')[-2]
        elif isinstance(inputfile, list):
            defaultstring = 'list_data'
        else:
            defaultstring = "Gantt Chart"

        if title == 'Auto'    :
            title = defaultstring
        return defaultstring

    def manage_data(dataframe,**kwargs):
        #filter and manipulate the data
        if filter_string is not None:
            dataframe = gt.filter_data(dataframe,filter_string[0],filter_string[1])

        # flatten milestones if requested
        if kwargs.get('flatten_milestones',False) is True:
            dataframe = gt.flatten_milestones(dataframe)
        return dataframe

    def save_files(fig,output_file=None):
        # save the figureure
        if output_file is not None:
            if output_file == 'Auto':
                output_file = f'{defaultstring}.png'
            plt.savefig(output_file)
        return output_file

    dataframe = import_data(input_data, **kwargs)
    defaultstring = make_default_string(input_data, title)
    dataframe = manage_data(dataframe, **kwargs)

    if plot_type == 'matplotlib':
        plotting_function = gt.gantt_chart
    elif plot_type == 'plotly':
        plotting_function = gt.plotly_gantt
    else:
        raise ValueError('plot_type must be "matplotlib" or "plotly"')

    axis, figure = plotting_function(dataframe,title=title,**kwargs)
    output_file = save_files(figure,output_file)

    output = dict(
        data = dataframe,
        axis = axis,
        figure = figure,
        output_file = output_file)

    if kwargs.get('show_figure',False) is True:
        figure.show()

    return output

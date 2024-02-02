# -*- coding: utf-8 -*-
"""
export functions for giganttic
Created on Mon Sep 25 14:40:53 2023

@author: dhancock
"""

import os
from matplotlib import pyplot as plt


def save_figures(df, ax, fig, title, outputdir, maxlines=60):
    """ Splits up an existing gantt chart into separate images,
    with a maximum number of rows given by maxlines and saves them.

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    ax : TYPE
        DESCRIPTION.
    fig : TYPE
        DESCRIPTION.
    title : TYPE
        DESCRIPTION.
    outputdir : TYPE
        DESCRIPTION.
    maxlines : TYPE, optional
        DESCRIPTION. The default is 60.

    Returns
    -------
    None.

    """

    ylocs = df.yvalue.unique().tolist()
    number_of_rows = len(ylocs)
    number_of_figures = round(len(ylocs)/maxlines)

    print(f'total number of rows: {number_of_rows}')
    print(f'number of figures: {number_of_figures}')

    if outputdir.endswith('/'):
        outputdir = outputdir[:-1]
        print('stripped trailing / from outputdir')
    if os.path.exists(outputdir) is False:
        os.mkdir(outputdir)
        print(f'created new directory: {outputdir}')

    # resize and set layout
    plt.rcParams.update({'font.size': 10})
    fig.set_dpi(60)
    width = 15  # inches
    fig.set_size_inches(width, width*2**0.5)
    plt.tight_layout(pad=1.1)

    # set the y axis limits to chunks of the whole and save individual files
    start, stop = 0, 0

    figure_files = []
    while stop < len(ylocs):
        stop = start + maxlines
        if stop > len(ylocs):
            stop = len(ylocs)
            if stop - start < 5:
                start = stop - 10
        ymin = ylocs[start]
        ymax = ylocs[stop-1]

        # ax.set_ylim((stop+1, start-1))
        ax.set_ylim((ymax+1, ymin-1))
        ax.set_title(f'{title} (rows {start}-{stop})')
        figure_filename = f'{outputdir}/{title} - {start}-{stop}.png'
        fig.savefig(figure_filename, dpi=300)
        figure_files.append(figure_filename)
        print(f'Plotted lines {start} to {stop}')
        start += maxlines

    return figure_files

# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 13:47:35 2023

@author: dhancock
"""

from matplotlib import pyplot as plt
from .mpl_gantt import gantt_chart
from .data_modify import filter_data


def plot_by_column(df, column, plot_function=gantt_chart, **kwargs):
    """ plot a different figure for each value in a given column """
    # plot_function = kwargs.get('plot_function',gt.gantt_chart)
    if 'title' in kwargs:
        title = kwargs.pop('title')
    else:
        title = f'{column}'
    df_filtered = df.copy()

    # print(f"plotting separate {column}s\n".upper())

    groups = df_filtered[column].unique().tolist()
    df_groups = {}
    figure_details = {}
    for group in groups:
        df_group = filter_data(df_filtered, column, group).copy()

        if len(df_group) > 0:
            subtitle = group
            graphtitle = '{} - {}'.format(subtitle, title)
            ax, fig = plot_function(df_group,
                                    f'{subtitle}\n{title}',
                                    **kwargs
                                    )
            df_groups[group] = df_group
            figure_details[group] = dict(
                axis=ax,
                figure=fig,
                title=graphtitle,
                data=df_group)
            plt.close()

    return figure_details


def get_fontsize(row_count,
                 fontsizes=list(zip((5, 10, 20, 50, 100, 500, 1000),
                                    (12, 10, 9, 8, 7, 6, 5))
                                )
                 ):
    """ returns a font size based on a number of rows"""

    fontsize = 12
    for rows, size in fontsizes:
        # print(f'DEBUG: row_count = {row_count}, rows = {rows}, size = {size}')
        if row_count > rows:
            fontsize = size
    # print(f'DEBUG: fontsize = {fontsize:<3} for {row_count:>5} rows')
    return fontsize

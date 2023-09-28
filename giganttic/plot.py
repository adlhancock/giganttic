# -*- coding: utf-8 -*-
""" giganttic.plot
plotting functions for giganttic

Created on Fri May  5 08:32:23 2023

@author: dhancock
"""

from itertools import cycle
from datetime import datetime as dt

#import pandas as pd
from matplotlib import colors, colormaps
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle, Patch

from .figure_sizes import get_figure_sizes

#%% Setup figure
def setup_figure(df,
                 title="Gantt Chart",
                 **kwargs
                 ):
    """ sets up the figure.

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    dates : list | None, optional
        DESCRIPTION. The default is None.
    yvalues : list | None, optional
        DESCRIPTION. The default is None.
    title : TYPE, optional
        DESCRIPTION. The default is "Gantt Chart".
    fontsize : int | float, optional
        DESCRIPTION. The default is None.
    figsize : list | int | float | None, optional
        DESCRIPTION. The default is None.
    dpi : int, optional
        DESCRIPTION. The default is None.
    figratio : str, optional
        DESCRIPTION. The default is 'print'.
    **kwargs : TYPE
        DESCRIPTION.

    Raises
    ------
    AssertionError
        DESCRIPTION.

    Returns
    -------
    ax : TYPE
        DESCRIPTION.
    fig : TYPE
        DESCRIPTION.

    """
    # get any kwargs values
    dates = kwargs.get('dates',None)
    yvalues=kwargs.get('yvalues',None)
    max_label_length = kwargs.get('max_label_length',100)
    
    # set the date range
    if dates is None:
        dates = (min(df.start[df.start.notna()]), max(df.end[df.end.notna()]))
    if dates[0] == dates[1]:
        dates = [dt(2022, 1, 1), dt(2050, 1, 1)]


    # set up figure
    if yvalues is None:
        df['yvalue'] = df.get('yvalue',list(range(len(df))))
        df['ylabel'] = df.get('ylabel',df.name)
        maxlength = max_label_length
        df.ylabel = df.ylabel.map(
            lambda x: str(x)[:maxlength-5]+'...' if len(str(x)) > maxlength else str(x))
        yvalues = [df.yvalue.tolist(), df.ylabel.tolist()]
    
    

    dimensions = get_figure_dimensions(df)
    # print(f'DEBUG: {dimensions}')
    plt.rcParams['font.size'] = dimensions['font_size']
    plt.rcParams['figure.dpi'] = dimensions['dpi']
    plt.rcParams['figure.figsize'] = [dimensions['width'],dimensions['height']]

    fig = plt.figure(
        figsize=[dimensions['width'],dimensions['height']],
        dpi=dimensions['dpi'],
        num=title,
        )

    ax = fig.add_subplot(111)
    ax.set_title(title)

    # assign date locator / formatter to the x-axis to get proper labels
    locator = mdates.AutoDateLocator(minticks=3)
    formatter = mdates.AutoDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    # set yaxis labels
    ax.set_yticks(yvalues[0], yvalues[1])
    ax.tick_params('y', length=0)

    # set x and y limits
    if dates is None:
        dates = [dt.now(), dt(2050, 1, 1)]
    xlimits = (mdates.date2num(d) for d in dates)
    plt.xlim(xlimits)

    if yvalues is None:
        ylimits = (dimensions['rows'], -1)
    else:
        ylimits = (max(yvalues[0])+1, min(yvalues[0])-1)
    plt.ylim(ylimits)

    plt.grid(linestyle="--", color="#eeeeee", zorder=0)
    
    # set tight layout, if requested
    if kwargs.get('tight_layout',True) is True:
        plt.tight_layout()

    return ax, fig

def get_figure_dimensions(df,
                          **kwargs):
    """ works out figure size, dpi, and font size from number of rows
    
    Parameters
    ----------
    df

    Returns
    -------
    dimensions

    """
    yvalues = kwargs.get('yvalues',None)
    
    # work out how many rows are in the figure
    if 'yvalue' in df.columns:
        rows = len(df.yvalue.unique())
        #print('DEBUG: rows set by df.yvalue')
    elif yvalues is not None:
        rows = len(set(yvalues[0]))
    else:
        rows = len(df)

    # set figure ratio
    figure_ratio = kwargs.get('figure_ratio','print')
    if figure_ratio == 'screen':
        ratio = 1.78 # assuming widescreen
    elif figure_ratio == 'print':
        ratio = 1.414 # A4 ratio is sqrt 2
    elif isinstance(figure_ratio, (float, int)):
        ratio = figure_ratio
    else:
        raise AssertionError('figure ratio must be "screen", "print", or float')

    figure_sizes = get_figure_sizes(rows, ratio, short_side=10)
    
    figure_size = kwargs.get('figure_size',None)

    if isinstance(figure_size,list):
        figure_width, figure_height = figure_size
        figure_size = 'manual'
    else:
        # use the max_row values in the figure_sizes dict to set figure_size
        size_names = list(figure_sizes.keys())
        size_names.remove('default')
        max_row_values = [figure_sizes[size_name]['max_rows']
                          for size_name in size_names]
        size_dictionary = dict(zip(max_row_values,size_names))
        for max_size in sorted(max_row_values,reverse=True):
            if rows < max_size:
                figure_size = size_dictionary[max_size]

    # apply the figure dimensions
    figure_dimensions = figure_sizes.get(figure_size,
                                         figure_sizes['default'])

    #print(f'DEBUG:{rows:<5} {figure_size:<10} {figure_dimensions}')
    
    dimensions = {'size':figure_size,
                  'rows':rows,
                  'height':figure_dimensions.get('figure_height'),
                  'width':figure_dimensions.get('figure_width'),
                  'font_size':kwargs.get('font_size',figure_dimensions.get('font_size')),
                  'dpi':kwargs.get('figure_dpi',figure_dimensions.get('figure_dpi'))}

    return dimensions

#%% get colors
def get_colors(df,
               fillcolumn=None,
               bordercolumn=None,
               customcolour_column='name',
               cmap_fill=colormaps['viridis'],
               cmap_border=colormaps['tab10'],
               customcolours:dict=None,
               default_fill="#002F56",
               default_border=None,
               recolour=True,
               **kwargs
               ):
    """
    gets colours for the dataframe

    Parameters
    ----------

    df
        dataframe
    fillcolumn
        which column is used to set the fill colour
    bordercolumn
        which column is used to set the border colour
    cmap_fill
        The default is matplotlib.colormaps['viridis']
    default_fill
        event fill if cannot be found
    default_border : TYPE, optional
        event border colour
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    fillcolour

    bordercolour

    df

    cmaps: dict
        keys are 'fill' and 'border'

    """

    # set the colourmaps
    if isinstance(cmap_fill, list):
        cmap_fill = colors.ListedColormap(cmap_fill, 'cmap')

    if cmap_border is not None:
        if isinstance(cmap_border, list):
            cmap_border = colors.ListedColormap(cmap_border, 'cmap_border')
    else:
        cmap_border = cmap_fill

    if recolour is True:
        df['fillcolour'] = None
        df['bordercolour'] = None
        df['customcolour'] = None

    #set the fill colour
    if fillcolumn is not None:
        fillvalues = df[fillcolumn].unique().tolist()
        if len(fillvalues) < len(cmap_fill.colors)*0.5 or len(cmap_fill.colors) > 30:
            #fillcolor = cmap(fillvalues.index(fillvalue)/len(fillvalues))
            df.fillcolour = df[fillcolumn].map(
                lambda x: cmap_fill(fillvalues.index(x)/len(fillvalues)))
        else:
            iterator = cycle(cmap_fill.colors)
            fillcolours = [next(iterator) for x in range(len(fillvalues))]
            #fillcolor = fillcolours[fillvalues.index(fillvalue)]
            df.fillcolour = df[fillcolumn].map(
                lambda x: fillcolours[fillvalues.index(x)])
    else:
        df.fillcolour = default_fill

    #set the border colour
    if bordercolumn is not None:
        bordervalues = df[bordercolumn].unique().tolist()
        df.bordercolour = df[bordercolumn].map(
            lambda x: cmap_border(bordervalues.index(x)/len(bordervalues)))
    else:
        df.bordercolor = default_border

    # populate any custom colours
    if customcolours is not None:
        for row, event in df.iterrows():
            for item in customcolours:  
                if item in str(event[customcolour_column]): # uses a very simple string search
                    event.fillcolour = customcolours[item]
                    event.customcolour = customcolours[item]

    
    cmaps = {'fill':cmap_fill,'border':cmap_border,'custom':customcolours}

    return df, cmaps

#%% add milestone labels
def add_milestone_labels(df):
    """
    add milestone labels to the middle of any bars that are milestones (shrug).
    Feature included because of the need to understand some poorly planned data.

    Parameters
    ----------
    df: pandas.DataFrame

    Returns
    -------
    df

    """
    zorder = len(df)+10
    for row, event in df.iterrows():
        if event.end != event.start:
            label_text = str(event.milestone)
            xval = event.start + (event.end-event.start)/2
            yval = row
            if label_text not in (None, 'nan', 'None',''):
                plt.text(
                    xval, yval,
                    f'{label_text:>5}',
                    zorder=zorder,
                    c='white',
                    va='center',
                    ha='center')

    return df


#%% plot event
def plot_event(event,
               ax,
               **kwargs):
    """
    plots a single event.
    if it's a milestone (zero-length event) try to add a label

    Parameters
    ----------
    
    event: single-row of a dataframe. Must have start, end, yvalue

    fill_colour: str

    border_colour: str

    ax: matplotlib.axes._axes.Axes

    """
    
    start = mdates.date2num(event.start)
    end = mdates.date2num(event.end)
    width = end - start
    x = start
    y = event.yvalue
    height = 0.7
    anchor = (x, y-height/2)
    fill_colour = event.get('fillcolour',kwargs.get('fill_colour','#aaaaaa'))
    border_colour = event.get('bordercolour',kwargs.get('border_colour',None))

    # plot as a zero length milestone
    milestone_size = plt.rcParams['font.size']*0.5
    if width == 0:
        ax.plot(x, y,
                marker="D",
                color=fill_colour,
                markersize=milestone_size
                )

        # create a "dummy" rectangle, to avoid errors
        shape = Rectangle(
            anchor,
            width=0,
            height=0)

        # add a text label if possible
        label_text = str(event.get('milestone',None))
        if label_text not in (None,'None','nan'): plt.text(x, y, f'{label_text:>6}')

    # plot as a bar
    else:
        shape = Rectangle(
            anchor,
            width,
            height,
        )
        shape.set_color(fill_colour)
        if border_colour is not None:
            shape.set_edgecolor(border_colour)
        shape.set_zorder(10)
        
    ax.add_patch(shape)


#%% plot connections
def plot_connections(df,
                     ax,
                     line_colour="grey",
                     **kwargs):
    """
    Add connection arrows.

    Parameters
    ----------
    df : DataFrame

    ax : axis

    line_colour : str, optional
        The default is "grey".
    **kwargs :


    Returns
    -------
    df : dataframe

    ax : matplotlib.axes._axes.Axes

    """
    assert 'predecessors' in df.columns, 'no predecessors defined in df'

    # some default variables
    arrow_style = kwargs.get('arrow_style','->')
    line_colour_error = kwargs.get('line_colour_error','red')
    line_style = '-'
    line_style_error = ':'
    line_radius = kwargs.get('line_radius',8)

    assert 'predecessors' in df.columns, 'no predecessors defined in dataframe'
    df.predecessors = df.predecessors.str.split(',')
    df.loc[df.predecessors.map(
        lambda x: x ==['']), 'predecessors'] = float('nan')

    for row, event in df.loc[df.predecessors.notna()].iterrows():
        x_end = float(mdates.date2num(event.start))
        y_end = float(event.yvalue)

        for predecessor in event.predecessors:

            predecessor_row = df[df.id == predecessor]
            x_start = float(mdates.date2num(predecessor_row.end))
            y_start = float(predecessor_row.yvalue)
            #print(f'DEBUG:\n\t x = {x_start},{x_end}\n\t y = {y_start},{y_end}')
            if y_start != y_end:
                if x_end < x_start:
                    connection_line_colour = line_colour_error
                    connection_line_style = line_style_error
                else:
                    connection_line_colour = line_colour
                    connection_line_style = line_style
                if x_end == x_start:
                    connection_style = "arc3,rad=0"
                else:
                    connection_style = f"angle,angleA=-90,angleB=180,rad={line_radius}"
                ax.annotate("",
                            xy=[x_end, y_end], xycoords='data',
                            xytext=[x_start, y_start], textcoords='data',
                            arrowprops={'arrowstyle':arrow_style,
                                        'linestyle':connection_line_style,
                                        'color':connection_line_colour,
                                        'shrinkA':8,
                                        'shrinkB':8,
                                        'connectionstyle':connection_style},
                            zorder=100
                            )

    return df, ax

#%% create legend
def add_legend(ax,
                  fig,
                  df,
                  cmaps,
                  **kwargs
                  ):

    """ add a legend

    Parameters
    ----------
    ax: matplotlib.axes._axes.Axes

    fig: matplotlib.figure.Figure

    df: pandas.DataFrame

    legend_sections: list, optional
        Default is ['fill', 'border', 'customcolours']

    Returns
    -------
    ax:

    fig:

    """
    fillcolumn=kwargs.get('fillcolumn',None)
    bordercolumn=kwargs.get('bordercolumn',None)
    customcolours=kwargs.get('customcolours',None)
    customcolour_column=kwargs.get('customcolour_column',None)

    # choose which bits of the legend to include
    legend_sections = kwargs.get('legend_sections',
                                 ['fill', 'border', 'customcolours'])

    patches = []
    # draw the fill column section of the legend
    if fillcolumn is not None and 'fill' in legend_sections:
        fill_title_patch = Patch(
            color='white', label=f'{fillcolumn}:'.upper()
            )
        patches.append(fill_title_patch)
        fill_labels = df[fillcolumn].unique().tolist()
        for n, i in enumerate(fill_labels):
            fillcolour = df.loc[
                df[fillcolumn]==i,'fillcolour'].unique().tolist()
            assert(len(fillcolour) == 1 ), 'inconsistent colours for legend'
            fillcolour = fillcolour[0]
            #print(fillcolour)
            patch = Patch(color=fillcolour, edgecolor=None, label=i)
            patches.append(patch)

    # draw the border colour section of the legend
    if bordercolumn is not None and 'border' in legend_sections:
        border_title_patch = Patch(
            color='white', label=f'{bordercolumn}:'.upper()
            )
        patches.append(border_title_patch)
        border_labels = df[bordercolumn].unique().tolist()
        for i in border_labels:
            bordercolour = df.loc[
                df[bordercolumn]==i,'bordercolour'].unique().tolist()
            assert(len(bordercolour) == 1), 'inconsistent border colours for legend'
            bordercolour = bordercolour[0]
            #print(bordercolour)

            patch = Patch(facecolor='white', edgecolor=bordercolour, label=i)
            patches.append(patch)

    # draw the custom colours section of the legend
    if customcolours is not None and 'customcolours' in legend_sections:
        customcolour_legend_title = kwargs.get(
            'customcolour_legend_title',customcolour_column)
        customcolours_title_patch = Patch(
            color="white",
            label=f"{customcolour_legend_title}:".upper()
            )
        patches.append(customcolours_title_patch)
        for c in customcolours:
            patch = Patch(color=customcolours[c], label=c)
            patches.append(patch)

    if len(patches) != 0:
        plt.rcParams['legend.framealpha'] = 0.5
        ax.legend(handles=patches, framealpha=0.5,fontsize='small')
    else:
        print("no legend items generated")


#%% add nowline
def add_nowline(df,ax,**kwargs):
    nowline_colour = kwargs.get('nowline_colour','#7a9aeb')
    xs = [mdates.date2num(dt.now())]*2
    ys = [max(df.yvalue)+1, min(df.yvalue)-1]
    ax.plot(xs, ys, color=nowline_colour, linestyle='--')


#%% gantt chart main function
def gantt_chart(df,
                # figure setup
                title="Gantt Chart",

                # features
                legend=False,
                nowline=True,
                connections=False,
                # kwargs                
                **kwargs):
    """ the main gantt chart function.

    Parameters
    ----------
    df : DataFrame

    Returns
    -------
    ax : ax

    fig : matplotlib.figure.Figure
    """
    
    assertion_error = 'dataframe must have "name", "start", and "end" columns as a minimum'
    assert all(x in df.columns for x in ['name', 'start', 'end']), assertion_error



    ax, fig = setup_figure(df,
                           title=title,
                           **kwargs)

    # get the colours
    df, cmaps = get_colors(df, **kwargs)

    # reset the index
    df = df.reset_index(drop=True)

    # iterate through events
    for row, event in df.iterrows():
        # create and add the shape
        plot_event(event, ax)
        

    # add a "now" line
    if nowline is True:
        add_nowline(df,ax)

    # add connection arrows
    if connections is True:
        plot_connections(df, ax, **kwargs)


    # add a legend
    if legend is True:
        add_legend(ax, fig, df,
                   cmaps,
                   **kwargs)

    return ax, fig



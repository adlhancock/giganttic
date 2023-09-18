# -*- coding: utf-8 -*-
"""
plotting functions for giganttic

Created on Fri May  5 08:32:23 2023

@author: dhancock
"""
import os
from itertools import cycle
from datetime import datetime as dt

import pandas as pd
from matplotlib import colors, colormaps
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle, Patch


#%% Setup figure
def setup_figure(df,
                 dates=None,
                 yvalues=None,
                 title="Gantt Chart",
                 fontsize=None,
                 figsize=None,
                 dpi: int=None,
                 figratio: str='print',
                 #**kwargs
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

    # resize and rescale dependent on number of rows
    if 'yvalue' in df.columns:
        rows = len(df.yvalue.unique())
        #print('DEBUG: rows set by df.yvalue')
    elif yvalues is not None:
        rows = len(set(yvalues[0]))
    else:
        rows = len(df)

    if isinstance(figsize, (float,int)):
        s = figsize
    else:
        s = 10 # size of figure short side, in inches

    if figratio == 'screen':
        ratio = 1.78
    elif figratio == 'print':
        ratio = 1.5 # A4 ratio is sqrt 2, but using adjustment ratio to fix odd distortion
    elif isinstance(figratio, (float, int)):
        ratio = figratio
    else:
        raise AssertionError('figratio must be "screen", "print", or float')


    if rows > 200:
        print(f'WARNING: trying to display {rows} rows. Very Unlikely to be legible!')
        fontsize = 3
        figuresize = [s, rows/2]
        figuredpi = 50
    if rows > 120:
        print(f'WARNING: trying to display {rows} rows. Unlikely to be legible!')
        fontsize = 8
        figuresize = [s, rows/1.5]
        figuredpi = 60
    elif rows > 65:
        print(f'WARNING: trying to display {rows} rows!')
        fontsize = 6
        figuresize = [s, rows/1.5]
        figuredpi = 60
    elif rows > 40:
        fontsize = 8
        figuresize = [s, s*ratio] # A4 portrait ratio
        figuredpi = 70
    elif rows > 10:
        fontsize = 10
        figuresize = [s*ratio, s] # A4 landscape ratio
        figuredpi = 100
    else:
        fontsize = 10
        figuresize = [s*2, rows] # thin landscape ratio
        figuredpi = 100

    if figsize is not None:
        print(f'manually setting figure size to {figsize}')
        figuresize = figsize
    if dpi is not None:
        print(f'manually setting figure dpi to {dpi}')
        figuredpi = dpi
    if fontsize is not None:
        plt.rcParams['font.size'] = fontsize


    plt.rcParams['font.size'] = fontsize
    plt.rcParams['figure.dpi'] = figuredpi
    plt.rcParams['figure.figsize'] = figuresize

    fig = plt.figure(
        figsize=figuresize,
        dpi=figuredpi,
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
        ylimits = (rows, -1)
    else:
        ylimits = (max(yvalues[0])+1, min(yvalues[0])-1)
    plt.ylim(ylimits)

    plt.grid(linestyle="--", color="#eeeeee", zorder=0)

    return ax, fig

#%% get colors
def get_colors(df,
               fillcolumn,
               bordercolumn,
               cmap=colormaps['viridis'],
               cmap_border=colormaps['tab10'],
               default_fill="#002F56",
               default_border=None,
               recolour=True,
               **kwargs):
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
    cmap
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
    if isinstance(cmap, list):
        cmap = colors.ListedColormap(cmap, 'cmap')

    if cmap_border is not None:
        if isinstance(cmap_border, list):
            cmap_border = colors.ListedColormap(cmap_border, 'cmap_border')
    else:
        cmap_border = cmap

    if recolour is True:
        df['fillcolour'] = None
        df['bordercolour'] = None



    #set the fill colour
    if fillcolumn is not None:

        #fillvalue = event[fillcolumn]
        fillvalues = df[fillcolumn].unique().tolist()
        if len(fillvalues) < len(cmap.colors)*0.5 or len(cmap.colors) > 30:
            #fillcolor = cmap(fillvalues.index(fillvalue)/len(fillvalues))
            df.fillcolour = df[fillcolumn].map(
                lambda x: cmap(fillvalues.index(x)/len(fillvalues)))
        else:
            iterator = cycle(cmap.colors)
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


    #df['bordercolour'] = df[bordercolumn].map(lambda x: allcolours[bordervalues.index(x)])
    cmaps = {'fill':cmap,'border':cmap_border}

    return df, cmaps

#%% add milestone labels
def add_milestone_labels(df):
    """
    add milestone labels to the middle of any bars that are milestones (shrug)

    Parameters
    ----------
    df: pandas.DataFrame

    Returns
    -------
    None

    """
    zorder = len(df)+10
    for row, event in df.iterrows():
        if event.end != event.start:
            label_text = str(event.milestone)
            xval = event.start + (event.end-event.start)/2
            yval = row
            plt.text(
                xval, yval,
                f'{label_text}',
                zorder=zorder,
                c='white',
                va='center',
                ha='center')

    return df


#%% plot event
def plot_event(yvalue,
               event,
               fill_colour="#aaaaaa",
               border_colour=None,
               ax=None,
               **kwargs):
    """
    plots a single event.
    if it's a milestone (zero-length event) try to add a label

    Parameters
    ----------
    yvalue: float

    event: single-row of a dataframe

    fill_colour: str

    border_colour: str

    ax: matplotlib.axes._axes.Axes

    **kwargs


    Returns
    -------
    shape: matplotlib.patches.Rectangle
        may be invisible, if a milestone, which will just be ploted
        using ax.plot using a "D" marker


    """
    start = mdates.date2num(event["start"])
    end = mdates.date2num(event["end"])
    width = end - start
    x = start
    y = yvalue
    height = 0.7
    anchor = (x, y-height/2)

    # plot as a zero length milestone
    if width == 0:
        ax.plot(x, y,
                marker="D",
                color=fill_colour,
                markersize=plt.rcParams['font.size']*0.5
                )

        # create a "dummy" rectangle, to avoid errors
        shape = Rectangle(
            anchor,
            width=0,
            height=0)

        # add a text label if possible
        try:
            if pd.notna(event.milestone):
                try:
                    label_text = str(event.milestone)
                    mslabel = f'  {label_text}'
                except:
                    mslabel = '  ??'
                plt.text(x, y, mslabel)
        except:
            pass

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
    return shape

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
        x_end = mdates.date2num(event.start)
        y_end = event.yvalue

        for predecessor in event.predecessors:

            predecessor_row = df[df.id == predecessor]
            x_start = mdates.date2num(predecessor_row.end)
            y_start = predecessor_row.yvalue
            #print(x_start, y_start)
            if x_end < x_start:
                line_colour = line_colour_error
                line_style = line_style_error
            if x_end == x_start:
                connection_style = "arc3, rad=0"
            else:
                connection_style = f"angle,angleA=-90,angleB=180,rad={line_radius}"
            ax.annotate("",
                        xy=[x_end, y_end], xycoords='data',
                        xytext=[x_start, y_start], textcoords='data',
                        arrowprops={'arrowstyle':arrow_style,
                                    'linestyle':line_style,
                                    'color':line_colour,
                                    'shrinkA':8,
                                    'shrinkB':8,
                                    'connectionstyle':connection_style},
                        zorder=100
                        )

    return df, ax

#%% create legend
def create_legend(ax,
                  fig,
                  df,
                  cmaps,
                  fillcolumn=None,
                  bordercolumn=None,
                  customcolours=None,
                  customcolour_field=None,
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

    **kwargs


    Returns
    -------

    ax:

    fig:

    """
    
    '''
    cmap = cmaps['fill']
    if 'border' in cmaps:
        cmap_border = cmaps['border']
    else:
        cmap_border = None
    if isinstance(cmap, list):
        cmap = colors.ListedColormap(cmap, 'cmap')

    if cmap_border is not None:
        if isinstance(cmap_border, list):
           cmap_border = colors.ListedColormap(cmap_border, 'cmap_border')
    else:
        cmap_border = cmap
    '''

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
        for n, i in enumerate(border_labels):
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
            'customcolour_legend_title',customcolour_field)
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
        ax.legend(handles=patches, framealpha=0.5)
    else:
        print("no legend items generated")
    return ax


#%% gantt chart main function
def gantt_chart(df,
                title="Gantt Chart",
                fillcolumn=None,
                bordercolumn=None,
                customcolours=None,
                customcolour_field='name',
                yvalues=None,
                dates=None,
                legend=False,
                nowline=True,
                nowline_colour='#7a9aeb',
                connections=True,
                tight=True,
                max_label_length=100,
                **kwargs):
    """ the main gantt chart function.

    Parameters
    ----------
    df : DataFrame

    title : str, optional
        The default is "Gantt Chart".
    fillcolumn : str, optional
        The default is None.
    bordercolumn : str, optional
        The default is None.
    customcolours : dict, optional
        The default is None.
    customcolour_field : str, optional
        The default is 'name'.
    yvalues : list, optional
        Format [[ylocations], [ylabels]].  The default is None.
    dates : list, optional
        Format [start_date, end_date]
        The default is None.
    legend : TYPE, optional
        add a legend.
        The default is False.
    nowline : TYPE, optional
        add a vertical line at today's date
        The default is True.
    nowline_colour : TYPE, optional
        The default is '#7a9aeb'.
    connections : TYPE, optional
        add connection arrows for dependencies
        The default is False.
    tight : TYPE, optional
        apply tight_layout. The default is True.
    max_label_length : TYPE, optional
        clip long labels with '...'
        The default is 100.
    **kwargs : TYPE


    Returns
    -------
    ax : ax

    fig : matplotlib.figure.Figure


    """
    assertion_error = 'dataframe must have "name", "start", and "end" columns as a minimum'
    assert all(x in df.columns for x in ['name', 'start', 'end']), assertion_error

    # set the date range
    if dates is None:
        dates = (min(df.start[df.start.notna()]), max(df.end[df.end.notna()]))
    if dates[0] == dates[1]:
        dates = [dt(2022, 1, 1), dt(2050, 1, 1)]


    # set up figure
    if yvalues is None:
        maxlength = max_label_length
        ylocs = list(range(len(df)))
        ylabels = df.name.map(
            lambda x: str(x)[:maxlength-5]+'...' if len(str(x)) > maxlength else str(x))
        yvalues = [ylocs, ylabels]

    else:
        ylocs, ylabels = yvalues

    df['yvalue'] = ylocs

    ax, fig = setup_figure(df,
                           dates=dates,
                           yvalues=yvalues,
                           title=title,
                           **kwargs)

    # get the colours
    df, cmaps = get_colors(df, fillcolumn, bordercolumn, **kwargs)

    # reset the index
    df = df.reset_index(drop=True)

    # iterate through events
    for row, event in df.iterrows():

        # apply custom colors
        if customcolours is not None:
            for item in customcolours:
                if item in str(event[customcolour_field]):
                    event.fillcolour = customcolours[item]

        # create and plot shapes
        yvalue = ylocs[row]

        # create and add the shape
        shape = plot_event(yvalue,
                           event,
                           fill_colour=event.fillcolour,
                           border_colour=event.bordercolour,
                           ax=ax)
        ax.add_patch(shape)

    # add a "now" line
    if nowline is True:
        xs = [mdates.date2num(dt.now())]*2
        ys = [max(ylocs)+1, min(ylocs)-1]
        ax.plot(xs, ys, color=nowline_colour, linestyle='--')

    # add connection arrows
    if connections is True and 'predecessors' in df.columns:
        try:
            plot_connections(df, ax, **kwargs)
        except:
            print('could not add connections')
            #raise

    # add a legend
    if legend is True:
        create_legend(ax, fig, df,
                      cmaps,
                      fillcolumn, bordercolumn,
                      customcolours, customcolour_field,
                      **kwargs)

    # set tight layout, if requested
    if tight is True:
        plt.tight_layout()

    return ax, fig

#%% save figures
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

    #resize and set layout
    plt.rcParams.update({'font.size': 10})
    fig.set_dpi(60)
    width = 15 #inches
    fig.set_size_inches(width, width*2**0.5)
    plt.tight_layout(pad=1.1)

    # set the y axis limits to chunks of the whole and save individual files
    start, stop = 0, 0

    while stop < len(ylocs):
        stop = start + maxlines
        if stop > len(ylocs):
            stop = len(ylocs)
            if stop - start < 5:
                start = stop - 10
        ymin = ylocs[start]
        ymax = ylocs[stop-1]

        #ax.set_ylim((stop+1, start-1))
        ax.set_ylim((ymax+1, ymin-1))
        ax.set_title(f'{title} (rows {start}-{stop})')
        fig.savefig(f'{outputdir}/{title} - {start}-{stop}.png',dpi=300)
        print(f'Plotted lines {start} to {stop}')
        start += maxlines

    return

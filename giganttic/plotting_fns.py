# -*- coding: utf-8 -*-
"""
plotting functions for giganttic

Created on Fri May  5 08:32:23 2023

@author: dhancock
"""

from matplotlib import colors, colormaps
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle, Patch
from itertools import cycle

from datetime import datetime as dt
import pandas as pd


#%% Setup figure
def setup_figure(df,
                 dates = None,
                 yvalues = None,
                 title = "Gantt Chart",
                 **kwargs):
    """
    

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    dates : TYPE, optional
        DESCRIPTION. The default is None.
    yvalues : TYPE, optional
        DESCRIPTION. The default is None.
    title : TYPE, optional
        DESCRIPTION. The default is "Gantt Chart".
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    ax : TYPE
        DESCRIPTION.
    fig : TYPE
        DESCRIPTION.

    """


    # resize and rescale dependent on number of rows
    if yvalues is None:
        rows = len(df)
    else:
        rows = len(df.yloc.unique())
    
    s = 15 # basic figure size, in inches.
    ratio = 2**0.5 # A4 ratio is sqrt 2, but using adjustment ratio to fix odd distortion

    if rows > 60:
        #print('WARNING: trying to print {} rows!'.format(rows))
        plt.rcParams['font.size'] = 8
        figuresize = [s, rows/1.5] 
        figuredpi = 60
    elif rows > 40:
        plt.rcParams['font.size'] = 8
        figuresize = [s, s*ratio] # A4 portrait ratio
        figuredpi = 60
    elif rows > 10:
        plt.rcParams['font.size'] = 8
        figuresize = [s*ratio, s] # A4 landscape ratio
        figuredpi = 100
    else:
        plt.rcParams['font.size'] = 8
        figuresize = [s, rows] # thin landscape ratio
        figuredpi = 100

    
    fig = plt.figure(
        figsize = figuresize,
        dpi = figuredpi,
        num = title,
        )
    
    ax = fig.add_subplot(111)
    ax.set_title(title)

    # assign date locator / formatter to the x-axis to get proper labels
    locator = mdates.AutoDateLocator(minticks = 3)
    formatter = mdates.AutoDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    # set yaxis labels
    ax.set_yticks(yvalues[0], yvalues[1])
    ax.tick_params('y', length = 0)

    # set x and y limits
    if dates == None:
        dates = [dt.now(), dt(2050, 1, 1)]
    xlimits = (mdates.date2num(d) for d in dates)
    plt.xlim(xlimits)        

    if yvalues == None:
        ylimits = (rows, -1)
    else:
        ylimits = (max(yvalues[0])+1, min(yvalues[0])-1)
    plt.ylim(ylimits)

    """
    # add a "now" line
    if nowline is True:
        xs = [mdates.date2num(dt.now())]*2
        ys = [rows+1, -1]
        ax.plot(xs, ys, 'r--')
    """
    plt.grid(linestyle = "--", color = "#eeeeee", zorder = 0)

    return ax, fig

#%% get colors    
def get_colors(df,
               fillcolumn,
               bordercolumn,
               cmap = colormaps['viridis'],
               cmap_border = colormaps['tab10'],
               default_fill = "#002F56",
               default_border = None,
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
    cmaps = dict(
        fill = cmap,
        border = cmap_border)
    
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
    for row, event in df.iterrows():
        if event.end != event.start:
            xval = event.start + (event.end-event.start)/2
            yval = row
            plt.text(
                xval, yval,
                '{}'.format(str(event.milestone)),
                zorder = 20,
                c = 'white',
                va = 'center',
                ha = 'center')
            
    return


#%% plot event
def plot_event(yvalue,
               event,
               fill_colour = "#aaaaaa",
               border_colour = None,
               ax = None,
               **kwargs):
    """
    plots a single event. if it's a milestone (zero-length event) try to add a label
    
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
                marker = "D",
                color = fill_colour,
                #markersize = "10"
                )

        # create a "dummy" rectangle, to avoid errors
        shape = Rectangle(
            anchor,
            width = 0,
            height = 0)
        
        # add a text label if possible
        try:
            if pd.notna(event.milestone):
                try: 
                    mslabel = '  {}'.format(str(event.milestone))
                except:
                    mslabel = '  {}'.format('??')
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

def plot_connections(df, 
                     ax, 
                     line_colour = "grey", 
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
    if 'arrow_style' not in kwargs:
        arrow_style = '->'
    if 'line_colour_error' not in kwargs:
        line_colour_error = 'red'
    line_style = '-'
    line_style_error = ':'
    if 'line_radius' not in kwargs:
        line_radius = 8
    
    
    assert 'predecessors' in df.columns, 'no predecessors defined in dataframe'
    df.predecessors = df.predecessors.str.split(',')
    df.loc[df.predecessors.map(lambda x: x ==['']), 'predecessors'] = float('nan')
    
    for row, event in df.loc[df.predecessors.notna()].iterrows():
        x_end = mdates.date2num(event.start)
        y_end = event.yloc
                
        for predecessor in event.predecessors:
                        
            p = df[df.id == predecessor]
            x_start = mdates.date2num(p.end)
            y_start = p.yloc
            #print(x_start, y_start)
            if x_end < x_start:
                lc = line_colour_error
                ls = line_style_error
            else:
                lc = line_colour
                ls = line_style
            if x_end == x_start:
                cs = "arc3, rad = 0"
            else:
                cs = "angle, angleA = -90, angleB = 180, rad = {}".format(line_radius)
            ax.annotate("",
                        xy = [x_end, y_end], xycoords = 'data',
                        xytext = [x_start, y_start], textcoords = 'data',
                        arrowprops = dict(
                            arrowstyle = arrow_style,
                            linestyle = ls,
                            color = lc,
                            shrinkA = 8,
                            shrinkB = 8,
                            connectionstyle = cs
                            ),
                        zorder = 100
                        )
    
    return df, ax

#%% 
def create_legend(ax,
                  fig,
                  df,
                  cmaps,
                  fillcolumn = None,
                  bordercolumn = None,
                  customcolours = None,
                  customcolour_field = None,
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
    
    cmap = cmaps['fill']
    if 'border' in cmaps:
        cmap_border = cmaps['border']
    else:
        cmap_border = None
        
    '''    
    if isinstance(cmap, list):
        cmap = colors.ListedColormap(cmap, 'cmap')
    
    if cmap_border is not None:
        if isinstance(cmap_border, list):
           cmap_border = colors.ListedColormap(cmap_border, 'cmap_border')
    else:
        cmap_border = cmap
    '''
    
    # choose which bits of the legend to include
    if 'legend_sections' in kwargs:
        legend_sections = kwargs['legend_sections']
    else:
        legend_sections = ['fill', 'border', 'customcolours']
    
    patches = []
    # draw the fill column section of the legend
    if fillcolumn is not None and 'fill' in legend_sections:
        fill_title_patch = Patch(
            color = 'white', label = '{}:'.format(fillcolumn).upper()
            )
        patches.append(fill_title_patch)
        fill_labels = df[fillcolumn].unique().tolist()
        #fill_labels = df.loc[df[fillcolumn].notna(), fillcolumn].unique().tolist()  ##TEST
        for n, i in enumerate(fill_labels):
            color = cmap(n/len(fill_labels))
            patch = Patch(color = color, edgecolor = None, label = i)
            patches.append(patch)
    
    # draw the border colour section of the legend        
    if bordercolumn is not None and 'border' in legend_sections:
        border_title_patch = Patch(
            color = 'white', label = '{}:'.format(bordercolumn).upper()
            )
        patches.append(border_title_patch)
        border_labels = df[bordercolumn].unique().tolist()
        for n, i in enumerate(border_labels):
            color = cmap_border(n/len(border_labels))
            patch = Patch(facecolor = 'white', edgecolor = color, label = i)
            patches.append(patch)
    
    # draw the custom colours section of the legend        
    if customcolours is not None and 'customcolours' in legend_sections:
        if 'customcolour_legend_title' in kwargs:
            customcolour_legend_title = kwargs['customcolour_legend_title']
        else:
            customcolour_legend_title = customcolour_field
        customcolours_title_patch = Patch(
            color = "white", label = "{}:".format(customcolour_legend_title).upper()
            )
        patches.append(customcolours_title_patch)
        for c in customcolours:
            patch = Patch(color = customcolours[c], label = c)
            patches.append(patch)
            
    if len(patches) != 0:
        ax.legend(handles = patches)
    else:
        print("no legend items generated")
    return


#%% gantt chart main function
def gantt_chart(df,
                title = "Gantt Chart",
                fillcolumn = None,
                bordercolumn = None,
                customcolours = None,
                customcolour_field = 'name',
                yvalues = None,
                dates = None,
                legend = False,
                nowline = True,
                nowline_colour = '#7a9aeb',
                connections = True,
                tight = True,
                max_label_length = 100,
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

    assert all([x in df.columns for x in ['name', 'start', 'end']]), 'dataframe must have "name", "start", and "end" columns as a minimum'

    # set the date range
    if dates is None: 
        dates = (min(df.start[df.start.notna()]), max(df.end[df.end.notna()]))
    if dates[0] == dates[1]: 
        dates = [dt(2022, 1, 1), dt(2050, 1, 1)]
   
                
    # set up figure
    if yvalues is None:
        ylocs = list(range(len(df)))
        ylabels = df.name.map(
            lambda x: str(x)[:max_label_length-5]+'...' if len(str(x)) > max_label_length else str(x))
        yvalues = [ylocs, ylabels]

    else:
        ylocs, ylabels = yvalues
    
    df['yloc'] = ylocs

    ax, fig = setup_figure(df, 
                           dates = dates, 
                           yvalues = yvalues, 
                           title = title, 
                           **kwargs)

    # get the colours
    df, cmaps = get_colors(df, fillcolumn, bordercolumn, **kwargs)
    
    # reset the index 
    df = df.reset_index(drop = True)
    
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
                           fill_colour = event.fillcolour,
                           border_colour = event.bordercolour, 
                           ax = ax)
        ax.add_patch(shape)
    
    # add a "now" line
    if nowline is True:
        xs = [mdates.date2num(dt.now())]*2
        ys = [max(ylocs)+1, min(ylocs)-1]
        ax.plot(xs, ys, color = nowline_colour, linestyle = '--')
    
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

def save_figures(df, ax, fig, title, outputdir, maxlines = 60):
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
    
    ylocs = df.yloc.unique().tolist()
        
    print('total number of rows: {}'.format(len(ylocs)))
    print('number of figures: {}'.format(round(len(ylocs)/maxlines)))
    if outputdir.endswith('/'):
        outputdir = outputdir[:-1]
        print('stripped trailing / from outputdir')
        print(outputdir)
    
    #resize and set layout
    plt.rcParams.update({'font.size': 10})
    fig.set_dpi(60)
    width = 15 #inches
    fig.set_size_inches(width, width*2**0.5)
    plt.tight_layout(pad = 1.1)

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
        ax.set_title('{} (rows {}-{})'.format(title, start, stop))
        fig.savefig('{}/{} - {}-{}.png'.format(outputdir, title, start, stop), dpi = 300)
        print('Plotted lines {} to {}'.format(start, stop))
        start += maxlines
        
    return 

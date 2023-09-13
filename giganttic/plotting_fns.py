# -*- coding: utf-8 -*-
"""
plotting functions for giganttic

Created on Fri May  5 08:32:23 2023

@author: dhancock
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
#from matplotlib.patches import Shadow
from matplotlib import colormaps
from datetime import datetime as dt
import pandas as pd
#import numpy as np

#%% Setup figure
def setup_figure(df,
                 dates=None,
                 yvalues = None,
                 title="Gantt Chart",
                 **kwargs):



    # resize and rescale dependent on number of rows
    if yvalues is None:
        rows = len(df)
    else:
        rows = len(df.yloc.unique())
    
    s = 15 # basic figure size, in inches.
    ratio = 2**0.5 * 1.5 # A4 ratio is sqrt 2, but using adjustment ratio to fix odd distortion

    if rows > 60:
        #print('WARNING: trying to print {} rows!'.format(rows))
        plt.rcParams['font.size'] = 8
        figuresize = [s,rows/1.5] 
        figuredpi = 60
    elif rows > 40:
        plt.rcParams['font.size'] = 8
        figuresize = [s,s*ratio] # A4 portrait ratio
        figuredpi = 60
    elif rows > 10:
        plt.rcParams['font.size'] = 8
        figuresize = [s*ratio,s] # A4 landscape ratio
        figuredpi = 100
    else:
        plt.rcParams['font.size'] = 8
        figuresize = [s,rows] # thin landscape ratio
        figuredpi = 100

    
    fig = plt.figure(
        figsize = figuresize,
        dpi=figuredpi,
        num = title,
        )
    
    ax = fig.add_subplot(111)
    ax.set_title(title)

    # assign date locator / formatter to the x-axis to get proper labels
    locator = mdates.AutoDateLocator(minticks=3)
    formatter = mdates.AutoDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    # set yaxis labels
    ax.set_yticks(yvalues[0],yvalues[1])
    ax.tick_params('y',length=0)

    # set x and y limits
    if dates == None:
        dates = [dt.now(),dt(2050,1,1)]
    xlimits = (mdates.date2num(d) for d in dates)
    plt.xlim(xlimits)        

    if yvalues == None:
        ylimits = (rows,-1)
    else:
        ylimits = (max(yvalues[0])+1,min(yvalues[0])-1)
    plt.ylim(ylimits)

    """
    # add a "now" line
    if nowline is True:
        xs = [mdates.date2num(dt.now())]*2
        ys = [rows+1,-1]
        ax.plot(xs,ys,'r--')
    """
    plt.grid(linestyle="--",color="#eeeeee",zorder=0)

    return ax,fig

#%% get colors    
def get_colors(index,
               df,
               fillcolumn,
               bordercolumn,
               cmap = colormaps['viridis'],
               default_fill = "#aaaaaa",
               default_border = None,
               **kwargs):
    
    if 'border_cmap' in kwargs:
        border_cmap = kwargs['border_cmap']
    else:
        border_cmap = cmap
        
    
    
    if fillcolumn is not None:
        fillvalue = df.iloc[index][fillcolumn]
        #fillvalues = [x for x in df[fillcolumn].unique()]
        fillvalues = df[fillcolumn].unique().tolist()
        fillcolor = cmap(
            fillvalues.index(fillvalue)/len(fillvalues))
    else:
        fillcolor = default_fill
    if bordercolumn is not None:
        bordervalue = df.iloc[index][bordercolumn]
        bordervalues = df[bordercolumn].unique().tolist()
        bordercolor = border_cmap(
            bordervalues.index(bordervalue)/len(bordervalues))
    else:
        bordercolor = default_border
        
    return fillcolor, bordercolor

#%% add milestone labels
def add_milestone_labels(df):
    """ add milestone labels to the middle of any bars that are milestones (shrug) """
    for row, event in df.iterrows():
        if event.end != event.start:
            xval = event.start + (event.end-event.start)/2
            yval = row
            plt.text(
                xval,yval,
                '{}'.format(str(event.milestone)),
                zorder=20,
                c='white',
                va='center',
                ha='center')


#%% plot event
def plot_event(yvalue,
               event,
               fill_colour="#aaaaaa",
               border_colour=None,
               ax=None,
               **kwargs):
    
    start = mdates.date2num(event["start"])
    end = mdates.date2num(event["end"])
    width = end - start
    x = start
    y = yvalue
    height = 0.7
    anchor = (x,y-height/2)
    
    # plot as a zero length milestone
    if width == 0:
        ax.plot(x,y,
                marker = "D",
                color = fill_colour,
                #markersize="10"
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
                    mslabel = '  {}'.format(str(event.milestone))
                except:
                    mslabel = '  {}'.format('??')
                plt.text(x,y,mslabel)
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

def plot_connections(df,ax,line_colour="grey", **kwargs):
    assert 'predecessors' in df.columns, 'no predecessors defined in dataframe'
    df.predecessors = df.predecessors.str.split(',')
    df.loc[df.predecessors.map(lambda x: x ==['']),'predecessors'] = float('nan')
    
    for row, event in df.loc[df.predecessors.notna()].iterrows():
        x_end = mdates.date2num(event.start)
        y_end = event.yloc
                
        for predecessor in event.predecessors:
                        
            p = df[df.id == predecessor]
            x_start = mdates.date2num(p.end)
            y_start = p.yloc
            #print(x_start,y_start)
            if x_end < x_start:
                lc = 'red'
                ls = ':'
            else:
                lc = line_colour
                ls = '-'
            if x_end == x_start:
                cs = "arc3,rad=0"
            else:
                cs = "angle,angleA=-90,angleB=180,rad=8"
            ax.annotate("",
                        xy = [x_end,y_end], xycoords = 'data',
                        xytext = [x_start,y_start], textcoords = 'data',
                        arrowprops = dict(
                            arrowstyle = '->',
                            linestyle = ls,
                            color = lc,
                            shrinkA = 8,
                            shrinkB = 8,
                            connectionstyle = cs
                            ),
                        zorder = 100
                        )

    
    return df, ax

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
                connections = False,
                tight = True,
                max_label_length = 100,
                **kwargs):

    assert all([x in df.columns for x in ['name','start','end']]), 'dataframe must have "name", "start", and "end" columns as a minimum'

    # set the date range
    if dates is None: 
        dates = (min(df.start[df.start.notna()]),max(df.end[df.end.notna()]))
    if dates[0] == dates[1]: 
        dates = [dt(2022,1,1),dt(2050,1,1)]
   
                
    # set up figure
    if yvalues is None:
        ylocs = list(range(len(df)))
        ylabels = df.name.map(
            lambda x: str(x)[:max_label_length-5]+'...' if len(str(x)) > max_label_length else str(x))
        yvalues = [ylocs,ylabels]

    else:
        ylocs, ylabels = yvalues
    
    df['yloc'] = ylocs

    ax, fig = setup_figure(df, 
                           dates=dates, 
                           yvalues=yvalues, 
                           title=title, 
                           **kwargs)

    # iterate through events
    df = df.reset_index(drop=True)
    for row, event in df.iterrows():
            
        #get colors
        try:
            fc, bc = get_colors(row, df, fillcolumn, bordercolumn,**kwargs)
        except:
            print("can't find fill color for {} for {}".format(df.iloc[row],fillcolumn))
            fc, bc = 'red',None
            
        # apply custom colors
        if customcolours is not None:
            for item in customcolours:
                if item in str(event[customcolour_field]):
                    fc = customcolours[item]
            
        # create and plot shapes
        yvalue = ylocs[row]
        
        shape = plot_event(yvalue,event,fill_colour = fc,border_colour=bc,ax=ax)
        ax.add_patch(shape)
    
    # add a "now" line
    if nowline is True:
        xs = [mdates.date2num(dt.now())]*2
        ys = [max(ylocs)+1,min(ylocs)-1]
        ax.plot(xs,ys,color = nowline_colour, linestyle='--')
    
    # add connection arrows
    if connections is True:
        try:
            plot_connections(df,ax,**kwargs)
        except:
            
            print('could not add connections')
            raise
        
    # create a legend
    def create_legend(ax,fig,df,**kwargs):
        if 'cmap' in kwargs: 
            cmap = kwargs['cmap']
        else:
            cmap = colormaps['viridis']
        if 'border_cmap' in kwargs:
            border_cmap = kwargs['border_cmap']
        else:
            border_cmap = cmap
        
        patches = []
        if fillcolumn is not None:
            fill_title_patch = mpl.patches.Patch(
                color='white',label='{}:'.format(fillcolumn).upper()
                )
            patches.append(fill_title_patch)
            fill_labels = df[fillcolumn].unique().tolist()
            #fill_labels = df.loc[df[fillcolumn].notna(),fillcolumn].unique().tolist()  ##TEST
            for n,i in enumerate(fill_labels):
                color = cmap(n/len(fill_labels))
                patch = mpl.patches.Patch(color=color,edgecolor=None,label=i)
                patches.append(patch)
        if bordercolumn is not None:
            border_title_patch = mpl.patches.Patch(
                color='white',label='{}:'.format(bordercolumn).upper()
                )
            patches.append(border_title_patch)
            border_labels = df[bordercolumn].unique().tolist()
            for n,i in enumerate(border_labels):
                color = border_cmap(n/len(border_labels))
                patch = mpl.patches.Patch(facecolor='white',edgecolor=color,label=i)
                patches.append(patch)
        if customcolours is not None:
            if 'customcolour_legend_title' in kwargs:
                customcolour_legend_title = kwargs['customcolour_legend_title']
            else:
                customcolour_legend_title = customcolour_field
            customcolours_title_patch=mpl.patches.Patch(
                color="white",label="{}:".format(customcolour_legend_title).upper()
                )
            patches.append(customcolours_title_patch)
            for c in customcolours:
                patch = mpl.patches.Patch(color=customcolours[c],label=c)
                patches.append(patch)
        if len(patches) != 0:
            ax.legend(handles=patches)
        else:
            print("no legend items generated")
        return
    
    if legend is True:
        create_legend(ax, fig, df, **kwargs)
        """
        if 'cmap' in kwargs: 
            cmap = kwargs['cmap']
        else:
            cmap = colormaps['viridis']
        if 'border_cmap' in kwargs:
            border_cmap = kwargs['border_cmap']
        else:
            border_cmap = cmap
        
        patches = []
        if fillcolumn is not None:
            fill_title_patch = mpl.patches.Patch(
                color='white',label='{}:'.format(fillcolumn).upper()
                )
            patches.append(fill_title_patch)
            fill_labels = df[fillcolumn].unique().tolist()
            #fill_labels = df.loc[df[fillcolumn].notna(),fillcolumn].unique().tolist()  ##TEST
            for n,i in enumerate(fill_labels):
                color = cmap(n/len(fill_labels))
                patch = mpl.patches.Patch(color=color,edgecolor=None,label=i)
                patches.append(patch)
        if bordercolumn is not None:
            border_title_patch = mpl.patches.Patch(
                color='white',label='{}:'.format(bordercolumn).upper()
                )
            patches.append(border_title_patch)
            border_labels = df[bordercolumn].unique().tolist()
            for n,i in enumerate(border_labels):
                color = border_cmap(n/len(border_labels))
                patch = mpl.patches.Patch(facecolor='white',edgecolor=color,label=i)
                patches.append(patch)
        if customcolours is not None:
            if 'customcolour_legend_title' in kwargs:
                customcolour_legend_title = kwargs['customcolour_legend_title']
            else:
                customcolour_legend_title = customcolour_field
            customcolours_title_patch=mpl.patches.Patch(
                color="white",label="{}:".format(customcolour_legend_title).upper()
                )
            patches.append(customcolours_title_patch)
            for c in customcolours:
                patch = mpl.patches.Patch(color=customcolours[c],label=c)
                patches.append(patch)
        if len(patches) != 0:
            ax.legend(handles=patches)
        else:
            print("no legend items generated")
        """

    # set tight layout, if requested
    if tight is True:
        plt.tight_layout()

    return ax,fig

def save_figures(df,ax,fig, title, outputdir, maxlines = 60):

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
    fig.set_size_inches(width,width*2**0.5)
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
        
        #ax.set_ylim((stop+1,start-1))
        ax.set_ylim((ymax+1,ymin-1))
        ax.set_title('{} (rows {}-{})'.format(title,start,stop))
        fig.savefig('{}/{} - {}-{}.png'.format(outputdir,title,start,stop),dpi=300)
        print('Plotted lines {} to {}'.format(start,stop))
        start += maxlines
        
    return 

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
#import numpy as np

#SUB-FUNCTIONS
#%% Setup figure
def setup_figure(df,
                 dates=None,
                 yvalues = None,
                 title="Gantt Chart",
                 nowline=True,
                 **kwargs):



    # resize and rescale dependent on number of rows
    rows = len(df)

    if rows>60:
        plt.rcParams['font.size'] = 6
        figuresize = [15,rows/1.5]
        figuredpi = 60
    elif rows>10:
        plt.rcParams['font.size'] = 8
        figuresize = [15,rows/3]
        figuredpi = 100
    else:
        plt.rcParams['font.size'] = 8
        figuresize = [15,rows]
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
    try:
        plt.xlim((mdates.date2num(d) for d in dates))
    except:
        dates = [dt.now(),dt(2050,1,1)]
        plt.xlim((mdates.date2num(d) for d in dates))
    plt.ylim((rows,-1))

    # add a "now" line
    if nowline==True:
        xs = [mdates.date2num(dt.now())]*2
        ys = [rows+1,-1]
        ax.plot(xs,ys,'r--')

    plt.grid(linestyle="--",color="#cccccc",zorder=0)

    return ax,fig

#%% get colors    
def get_colors(index,
               df,
               fillcolumn,
               bordercolumn,
               cmap = colormaps['viridis'],
               **kwargs):
    
    if 'border_cmap' in kwargs:
        border_cmap = kwargs['border_cmap']
    else:
        border_cmap = cmap
        
    default_fill = "#aaaaaa"
    default_border = None
    
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

#%% create legend



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
    height = 0.8
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
            plt.text(x,y,event.milestone)
        except:
            plt.text(x,y,'??')
            #pass

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

#%% MAIN FUNCTION
#%% gantt chart main function
def gantt_chart(df,
                title = "Gantt Chart",
                fillcolumn = None,
                bordercolumn = None,
                customcolors = None,
                yvalues = None,
                dates = None,
                legend = False,
                **kwargs):

    assert all([x in df.columns for x in ['name','start','end']]), 'dataframe must have "name", "start", and "end" columns as a minimum'

    # set the date range
    if dates is None: dates = (min(df.start[df.start.notna()]),max(df.end[df.end.notna()]))
    if dates[0] == dates[1]: dates = [dt(2022,1,1),dt(2050,1,1)]
   
                
    # set up figure
    if yvalues is None: yvalues = [df.index.tolist(),df.name]
    ax, fig = setup_figure(df, title=title,yvalues=yvalues,dates=dates)

    # iterate through events
    for row, event in df.iterrows():
        
        #get colors
        try:
            fc, bc = get_colors(row, df, fillcolumn, bordercolumn,**kwargs)
        except:
            #print("can't find fill color for {} for {}".format(df.iloc[row],fillcolumn))
            fc, bc = 'red',None
            
        # apply custom colors
        if customcolors is not None:
            for item in customcolors:
                #print(event)
                #print(item,str(event.name))
                if item in str(event['name']):
                    fc = customcolors[item]
                    #print(item,event['name'],fc)

            
        # create and plot shapes
        yvalue = row
        shape = plot_event(yvalue,event,fill_colour = fc,border_colour=bc,ax=ax)
        ax.add_patch(shape)
        
        # create a legend
        if legend is True:
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
                    color='white',label='{}:'.format(fillcolumn)
                    )
                patches.append(fill_title_patch)
                fill_labels = df[fillcolumn].unique().tolist()
                for n,i in enumerate(fill_labels):
                    color = cmap(n/len(fill_labels))
                    patch = mpl.patches.Patch(color=color,edgecolor=None,label=i)
                    patches.append(patch)
            if bordercolumn is not None:
                border_title_patch = mpl.patches.Patch(
                    color='white',label='{}:'.format(bordercolumn)
                    )
                patches.append(border_title_patch)
                border_labels = df[bordercolumn].unique().tolist()
                for n,i in enumerate(border_labels):
                    color = border_cmap(n/len(border_labels))
                    patch = mpl.patches.Patch(facecolor='white',edgecolor=color,label=i)
                    patches.append(patch)
            if customcolors is not None:
                customcolors_title_patch=mpl.patches.Patch(
                    color="white",label="custom colours:"
                    )
                patches.append(customcolors_title_patch)
                for c in customcolors:
                    patch = mpl.patches.Patch(color=customcolors[c],label=c)
                    patches.append(patch)
            if len(patches) != 0:
                ax.legend(handles=patches)
            else:
                print("no legend items generated")
        #shadow = Shadow(shape,5,0.05,alpha=0.1)
        #ax.add_patch(shadow)

    plt.tight_layout()

    return ax,fig


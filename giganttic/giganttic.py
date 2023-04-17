# -*- coding: utf-8 -*-
"""
giganttic.py


"""

import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
from matplotlib.patches import Shadow
from matplotlib import colormaps
import numpy as np
import csv
#import mpld3

INPUTFILE = "./input/exampledata.csv"
OUTPUTFILE = "./output/examplechart.png"
TITLE = "Example Gantt Chart"
#FILTER = ["name","T\d[^Aa]"]
FILTER = None

def import_csv(file,columns = ["id","name","start","end","level"]):

    # some dummmy data    
    dummydata = [
        [1,"task 1","31-Jan-2023","12/12/2028",1],
        [2,"task 2","31/08/2023","12/12/2025",2],
        [3,"another task","01/01/2025","12/01/2028",2],
        [4,"do some testing","01/01/2025","12/12/2030",1],
        [5,"design something","01/01/2025","12/12/2028",2],
        [6,"Milestone","01/01/2027","01/01/2027",2],
        [7,"B","01/01/2025","12/12/2026",3],
        [8,"C","01/01/2026","12/01/2027",3],
        [9,"D","01/01/2027","12/12/2028",3],
        [10,"F","01/01/2027","12/12/2030",2],
    ]

    with open(file,'r') as f:
        csvdata = csv.reader(f)
        nestedlist = [row for row in csvdata]

    events = nestedlist
    #events = dummydata

    # create dataframe
    df = pd.DataFrame(events)
    df.columns = columns
    df.start = pd.to_datetime(df.start,dayfirst=True)
    df.end = pd.to_datetime(df.end,dayfirst=True)

    return df

def gantt_chart(df,title="Gantt Chart",fill="level"):

    def setup_figure(df,dates=None,title="Gantt Chart",nowline=True):
        if dates is None: dates = (min(df.start),max(df.end))
        rows = len(df)

        fig = plt.figure(figsize=(20,rows/3))
        ax = fig.add_subplot(111)
        ax.set_title(title)

        # assign date locator / formatter to the x-axis to get proper labels
        locator = mdates.AutoDateLocator(minticks=3)
        formatter = mdates.AutoDateFormatter(locator)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)

        # set yaxis labels
        ax.set_yticks(df.index.tolist(),df.name)
        ax.tick_params('y',length=0)

        # set x and y limits
        plt.xlim((mdates.date2num(d) for d in dates))
        plt.ylim((rows,-1))

        # add a "now" line
        if nowline==True:
            xs = [mdates.date2num(dt.now())]*2
            ys = [rows+1,-1]
            ax.plot(xs,ys,'r--')

        return ax,fig

    def plot_event(index,event,fill="level",border=None,ax=None,cmap=None):
        start = mdates.date2num(event["start"])
        end = mdates.date2num(event["end"])
        width = end - start
        x = start
        y = int(index)
        height = 0.8
        anchor = (x,y-height/2)
        
        # plot as a zero length milestone
        if width == 0:
            ax.plot(x,y,"Dk",markersize="10")

            # create a "dummy" rectangle, to avoid errors
            shape = Rectangle(
                anchor,
                width=0,
                height=0)

        # plot as a bar
        else:
            shape = Rectangle(
                anchor,
                width,
                height,
            )

            try:
                fill_color = cmap(event[fill]/max(df[fill]))
            except:
                values = df[fill].unique().tolist()
                values.sort()
                fill_color = cmap(values.index(event[fill])/len(values))
            shape.set_color(fill_color)
            if border is not None:
                outline_color = cmap(event[border]/max(df[border]))
                shape.set_edgecolor(outline_color)
            shape.set_zorder(10)
        return shape

    border=None
    ax,fig = setup_figure(df, title=title)
    #cmap = colormaps['Spectral']
    #cmap = colormaps['tab20']
    cmap = colormaps['viridis']
    plt.grid(linestyle="--",color="#cccccc",zorder=0)

    for index, event in df.iterrows():
        shape = plot_event(index,event,fill,border=border,ax=ax,cmap=cmap)
        ax.add_patch(shape)
        #shadow = Shadow(shape,5,0.05,alpha=0.1)
        #ax.add_patch(shadow)

    plt.tight_layout()

    return fig

def giganttic(INPUTFILE,OUTPUTFILE,TITLE,FILTER):
    df = import_csv(INPUTFILE)
    if FILTER is not None:
        df = df[df[FILTER[0]].str.contains(FILTER[1], regex=True)].reset_index(drop=True)
    fig = gantt_chart(df,title=TITLE)
    fig.show()
    plt.savefig(OUTPUTFILE)
    
giganttic(INPUTFILE,OUTPUTFILE,TITLE,FILTER)
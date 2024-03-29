# -*- coding: utf-8 -*-
"""
test cases for giganttic 

Created on Fri May  5 08:27:58 2023

@author: dhancock
"""

import os
import sys
from matplotlib import pyplot, colormaps

sys.path.insert(0,os.path.abspath('..'))
import giganttic as gt



#%% CASES
def case_1():
    """
    CASE 1 - import, plot and save separately.
    """

    df = gt.import_csv('./input/exampledata1.csv')

    ax, fig = gt.gantt_chart(df,
                             title='Example 1',
                             fillcolumn="id",
                             cmap_fill=colormaps['tab10'],
                             connections=True,
                             nowline = True)
    fig.savefig('./output/case_1.png')
    fig.show()
    out = df,ax,fig
    return out

def case_2():
    """
    CASE 2 all in one with an excel file
    """
    out = gt.giganttic('./input/exampledata2.xlsx',
                        output_file='./output/case_2.png',
                        'Example 2',
                        default_fill = '#cccccc',
                        cmap_border = colormaps['viridis'],
                        bordercolumn = 'id',
                        connections = False,
                        legend = True,
                        nowline = False)
    return out

def case_3():
    """
    CASE 3 all in one with a list
    """

    dummydata = [
        ["id","activity_name","start","end","level"],
        [1,"task 1","31-Jan-2023","12/12/2028",1],
        [2,"task 2","31/08/2023","12/12/2025",2],
        [3,"another task","01/01/2025","12/01/2028",2],
        [4,"do some testing","01/01/2025","12/12/2030",1],
        [5,"design something","01/01/2025","12/12/2028",2],
        [6,"Milestone","01/01/2027","01/01/2027",2],
        [7,"B","01/01/2025","12/12/2026",3],
        [8,"task C","01/01/2026","12/01/2027",3],
        [9,"D","01/01/2027","12/12/2028",3],
        [10,"F","01/01/2027","12/12/2030",2],
        ]
    out = gt.giganttic(dummydata,
                       './output/case_3.png',
                       'Example 3',
                       connections = False,
                       default_fill='navy')
    return out

def case_4():
    """ 
    CASE 4: manual file picking with a custom colourmap
    """
    out = gt.giganttic(
        output_file='./output/case4.png',
        title = "Case 4",
        cmap_fill=['red','orange','yellow','green','blue','indigo','violet'],
        fillcolumn='id')
    return out

def case_5():
    """ 
    CASE 5: cycling colour map from list
    """
    dummydata = [
            ["id","activity_name","start","end","level"],
            [1,"task","31-Jan-2023","12/12/2028",1],
            [1,"task","31-Jan-2023","12/12/2028",1],
            [1,"task","31-Jan-2023","12/12/2028",1],
            [1,"task","31-Jan-2023","12/12/2028",1],
            [1,"task","31-Jan-2023","12/12/2028",1],
            [1,"task","31-Jan-2023","12/12/2028",1],
            [1,"task","31-Jan-2023","12/12/2028",1],
            [1,"task","31-Jan-2023","12/12/2028",1],
            [1,"task","31-Jan-2023","12/12/2028",1],
            [1,"task","31-Jan-2023","12/12/2028",1],
            [1,"task","31-Jan-2023","12/12/2028",1],
            ]
    df = gt.import_list(dummydata)
    df.id = range(len(df))
    df.loc[:,'activity_name'] = df.id.map(str)+' - '+df.activity_name
    ax, fig = gt.gantt_chart(df,
                             fillcolumn='id',
                             cmap_fill=['#F6D44D',
                                        '#006F45',
                                        '#0082CA',
                                        '#C9252C',
                                        '#002F56',
                                        '#58585B'])

    return df, ax, fig

def case_6():
    inputfile = './input/exampledata1.csv'
    df = gt.import_csv(inputfile)
    plot = gt.plotly_gantt(df,
                           title='Case 6',
                           fillcolumn='id',
                           cmap_fill = colormaps['plasma'],
                           show_rangeslider = True,
                           yaxis_range_menu = True,
                           yaxis_ranges = [5,10,15]
                           )
    
    fig = plot[1]
    fig.update_traces(showlegend=True)
    fig.show('browser')
    fig.write_html('./output/case_6.html')
    
    return df, *plot

#%% MAIN
if __name__ == '__main__':
    pyplot.close('all')
    out_1 = case_1()
    out_2 = case_2()
    out_3 = case_3()
    out_4 = case_4()
    out_5 = case_5()
    out_6 = case_6()

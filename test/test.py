# -*- coding: utf-8 -*-
"""
test sctipt for giganttic 

Created on Fri May  5 08:27:58 2023

@author: dhancock
"""

import os
import sys
from matplotlib import pyplot as plt

sys.path.insert(0,os.path.abspath('..'))

import giganttic as gt


#%% CASE 1 - import, plot and save separately.
def case_1():
    df = gt.import_csv('./exampledata1.csv')
    ax, fig = gt.gantt_chart(df,title='Example 1',fillcolumn="id",connections=True)
    fig.savefig('exampledata1.png')
    fig.show()
    
    return df, ax, fig

#%% CASE 2 all in one with an excel file
def case_2():
    return gt.giganttic('exampledata2.xlsx','exampledata2.png','Example 2', connections = False)

#%% CASE 3 all in one with a list
def case_3():
    
    DUMMYDATA = [
        ["id","name","start","end","level"],
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
    
    return gt.giganttic(DUMMYDATA,'exampledata3.png','Example 3', connections = False,default_fill='pink')

#%% MAIN
plt.close('all')
case_1()
case_2()
case_3()
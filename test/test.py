# -*- coding: utf-8 -*-
"""
test sctipt for giganttic 

Created on Fri May  5 08:27:58 2023

@author: dhancock
"""

import os
import sys

sys.path.insert(0,os.path.abspath('..'))

import giganttic as gt
#import pandas as pd

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


#%% CASE 1 - directly plot dummy data




df1 = gt.import_csv('./exampledata1.csv')
df1, fig1 = gt.gantt_chart(df1,title='Example 1',fillcolumn="id")
fig1.savefig('exampledata1.png')
fig1.show()


#%% CASE 2

df2,fig2 = gt.giganttic('exampledata2.xlsx','exampledata2.png','Example 2')

#%% CASE 3
df3,fig3 = gt.giganttic(DUMMYDATA,'exampledata3.png','Example 3')



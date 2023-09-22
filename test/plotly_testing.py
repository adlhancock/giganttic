# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 14:53:40 2023

@author: dhancock
"""
import pandas as pd
import giganttic as gt
from giganttic.plotly_gantt import plotly_gantt as pg
from shared_functions import latestfile, ukaea_colours

path = './input/'
filestring = "STEP Test Programmes List-"
inputfile, datestring = latestfile(path,filestring,'csv')
df = gt.import_csv(inputfile)
df = df.rename(columns={'Title':'name'})
milestone_cols = ['T0','T1','T3','T4','T5']
df[milestone_cols] = df[milestone_cols].apply(pd.to_datetime,dayfirst = True)
df = gt.data_fns.get_durations(df, milestone_cols)
df = gt.extract_milestones(df,milestone_cols)
df['yvalue'] = list(range(len(df)))
df['ylabel'] = df.name
df = gt.data_fns.flatten_milestones(df)

df,cmaps = gt.plotting_fns.get_colors(df,cmap=ukaea_colours,fillcolumn='milestone',bordercolumn=None)

#maxrows = 200
fig = pg(df,rows_to_show=40)
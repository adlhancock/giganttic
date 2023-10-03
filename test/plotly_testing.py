# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 14:53:40 2023

@author: dhancock
"""
import pandas as pd
import giganttic as gt
from giganttic.plotly_gantt import plotly_gantt as pg
#from shared_functions import latestfile, ukaea_colours
from matplotlib import colormaps as cm

inputfile = 'exampledata1.csv'
df = gt.import_csv(inputfile)


df,cmaps = gt.get_colors(df,cmap=cm['viridis'],fillcolumn='name',bordercolumn=None)

#maxrows = 200
fig = pg(df,)
fig.show('browser')
#fig.write_html('plotly_testing.html')
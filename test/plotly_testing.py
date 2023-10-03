# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 14:53:40 2023

@author: dhancock
"""

import giganttic as gt

inputfile = 'exampledata1.csv'

df = gt.import_csv(inputfile)
ax, fig = gt.plotly_gantt(df,rows_to_show=7,yaxis_range_menu=True)
fig.show('browser')
#fig.write_html('plotly_testing.html')
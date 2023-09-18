# -*- coding: utf-8 -*-
"""
Created on Tue May  2 11:12:32 2023

@author: dhancock
"""

import os
import sys

sys.path.insert(0,os.path.abspath('..'))
import giganttic as gt

TESTFILE = './exampledata2.xlsx'
dataframe = gt.import_excel(TESTFILE)
output = gt.extract_milestones(dataframe)
gt.gantt_chart(output,fill='id')

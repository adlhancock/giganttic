# -*- coding: utf-8 -*-
"""
Created on Tue May  2 11:12:32 2023

@author: dhancock
"""
import pandas as pd
import giganttic as gt

testfile = './testdata.xlsx'

df = gt.import_excel(testfile)


output = gt.extract_milestones(df)

gt.gantt_chart(output,fill='id')
#for ms in output.keys():
#        print(ms,len(output[ms]))
        

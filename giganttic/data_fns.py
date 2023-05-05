# -*- coding: utf-8 -*-
"""
data manipulation ond filtering functions for giganttic

Created on Fri May  5 08:30:31 2023

@author: dhancock
"""

import pandas as pd
import numpy as np


#%% data modification

def filter_data(df,column,regex):
    df = df[df[column].str.contains(
                regex, regex=True)].reset_index(drop=True)
    return df

def extract_milestones(df,milestones = ['T0','T3','T4']):
    
    for milestone in milestones:
        #ms = milestone.lower()
        ms = milestone
        milestonerowsms = df[pd.notna(df[ms])]
        for i, row in milestonerowsms.iterrows():
            newrow = pd.DataFrame({
                'num' : i,
                'id': row['id'] + '.{}'.format(ms),
                'name' : row['name'] + ' ({})'.format(ms),
                'start' : row[ms],
                'end': row[ms],
                'milestone' : ms,
                ms:row[ms]
                },
                index=['num']
                )
            df = pd.concat(
                [df.iloc[:i],newrow,df.iloc[i:]]).reset_index(drop=True)
            df = df.drop('num',axis=1)
            #df = df.sort_values('milestone')
            #df = df.sort_values('name').reset_index(drop=True)
            df = df.sort_values('id').reset_index(drop=True)
    return df
    
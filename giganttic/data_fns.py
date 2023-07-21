# -*- coding: utf-8 -*-
"""
data manipulation ond filtering functions for giganttic

Created on Fri May  5 08:30:31 2023

@author: dhancock
"""

import pandas as pd
import numpy as np
from datetime import datetime as dt


#%% data modification

def filter_data(df,column,regex):
    df = df[df[column].str.contains(
                regex, regex=True)].reset_index(drop=True)
    return df

def extract_milestones(df,milestones = ['T0','T1','T2','T3','T4','T5','R0','R1','R2','R3','R4']):
    df = df.reindex()
    df['id'] = df.index.map(lambda x: str(x).zfill(4))
    for j, ms in enumerate(milestones):

        milestonerowsms = df[pd.notna(df[ms])]
        for i, row in milestonerowsms.iterrows():
            newrow = pd.DataFrame({
                'num' : i,
                'id': row['id'] + '.{}'.format(j),
                'name' : row['name'] + ' ({})'.format(ms),
                'start' : row[ms],
                'end': row[ms],
                'milestone' : ms,
                ms:row[ms]
                },
                index=['id']
                )

            
            df = pd.concat([df,newrow])
            df = df.drop('num',axis=1)
    df = df.sort_values('id').reset_index(drop=True)
    return df

def get_durations(df,milestone_cols):
    def startend(row,func):
        if list(row) == [pd.NaT]*5:
            out = dt.now()
        else:
            out = func([x for x in row if x is not pd.NaT])
        return out    
    
    df['start'] = df[milestone_cols].apply(lambda x: startend(x,min),axis=1)
    df['end'] = df[milestone_cols].apply(lambda x: startend(x,max),axis=1)
    
    df['duration'] = df.end-df.start
    return df
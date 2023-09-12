# -*- coding: utf-8 -*-
"""
data manipulation ond filtering functions for giganttic

Created on Fri May  5 08:30:31 2023

@author: dhancock
"""

import pandas as pd
#import numpy as np
from datetime import datetime as dt

def get_datestring():
    timenow = dt.now()
    
    return timenow.strftime("%Y%m%d")


#%% data modification

def filter_data(df,column,regex):
    df = df[df[column].str.contains(
                regex, regex=True,na=False)].reset_index(drop=True)
    return df

def extract_milestones(df,milestones = ['T0','T1','T2','T3','T4','T5','R0','R1','R2','R3','R4']):
    """ 
    this assumes the dataframe is a row of activities with columns for the milestone dates
    """
    #df = df.reindex()
    df['activity_id'] = df.index.map(lambda x: str(x).zfill(4))
    df['ordering'] = df.activity_id.str.zfill(4)
    df['row_type'] = 'Activity'
    for ms_number, ms in enumerate(milestones):
        ms_id = str(ms_number).zfill(4)
        activities_with_this_ms = df[pd.notna(df[ms])]
        for row_number, row in activities_with_this_ms.iterrows():
            newrow = pd.DataFrame({
                'row_type' : 'Milestone',
                #'name' : row['name'] + ' ({})'.format(ms),
                'name' : '({})'.format(ms),
                'activity_id': row['activity_id'],
                #'milestone_id': ms_id,
                'ordering': row['activity_id'] + '.{}'.format(ms_id),
                'start' : row[ms],
                'end': row[ms],
                'milestone' : ms,
                ms:row[ms]
                },
                index=['ordering']
                )

            
            df = pd.concat([df,newrow])
    df = df.sort_values('ordering').reset_index(drop=True)
    return df

def flatten_milestones(df):
    """ 
    Return values and labels in the format 
    [yloc, ylabel] which clears the milestone labels and puts them 
    in a single line below the main task bar 
    """
    
    df['ylabel'] = df.name
    df.loc[df['row_type'] == 'Milestone','ylabel'] = ''
    df['yvalue'] = df.activity_id.map(float) * 2
    df.loc[df['row_type'] == 'Milestone','yvalue'] = df.yvalue + 0.7
    #ylocs = df.activity_id
    yvalues = [df.yvalue.tolist(),df.ylabel.tolist()]
    return yvalues

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
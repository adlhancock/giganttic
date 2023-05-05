# -*- coding: utf-8 -*-
"""
import functions for giganttic 

Created on Fri May  5 08:27:58 2023

@author: dhancock
"""
import csv
import pandas as pd


#%% data import functions

def import_csv(
    file,
    headers = True, 
    columns=["id","name","start","end","level"]
    ):
    '''
    headers: if the first line of the csv file has headers
    columns: if headers is false, use this list as dataframe columns
    '''

    with open(file,'r') as f:
        csvdata = csv.reader(f)
        nestedlist = [row for row in csvdata]

    events = nestedlist
    
    # create dataframe
    
    if headers is True:
        df = pd.DataFrame(events[1:])
        df.columns = events[0]
    else:
        df = pd.DataFrame(events)
        df.columns = columns

    df.start = pd.to_datetime(df.start,dayfirst=True)
    df.end = pd.to_datetime(df.end,dayfirst=True)

    return df

def import_excel(file,**kwargs):
    if "sheet" in kwargs.keys():
        sheet = kwargs["sheet"]
    else:
        sheet = "Sheet1"
    df = pd.read_excel(file,sheet)
    try:
        df.start = pd.to_datetime(df.start,dayfirst=True)
    except:
        pass
    try:
        df.end = pd.to_datetime(df.end,dayfirst=True)
    except:
        pass 
    df = df[df.start.notna()]
    df = df[df.end.notna()].reset_index(drop=True)
    #df.columns = df.columns.str.lower()
    #print(df)
    return df

def import_list(data):
    df = pd.DataFrame(data[1:],columns=data[0])
    df.columns = df.columns.str.lower()
    df.start = pd.to_datetime(df.start,dayfirst=True)
    df.end = pd.to_datetime(df.end,dayfirst=True)
    
    return df
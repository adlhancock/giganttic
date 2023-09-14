# -*- coding: utf-8 -*-
"""
import functions for giganttic 

Created on Fri May  5 08:27:58 2023

@author: dhancock
"""
import csv
import pandas as pd
#import numpy as np
import xmltodict
from tkinter import Tk
from tkinter.filedialog import askopenfilename


#%% data import functions

def import_csv(
    file,
    headers = True, 
    columns=["id","name","start","end","level"],
    **kwargs
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

    if all(["start" in df.columns, "end" in df.columns]):
        
        df.start = pd.to_datetime(df.start,dayfirst=True)
        df.end = pd.to_datetime(df.end,dayfirst=True)
    else:
        print("{}: WARNING - no start and end values defined".format(__name__))        

    return df

def import_excel(file,sheet=0,**kwargs):
    """
    import an excel file, defaulting to the first worksheet

    Parameters
    ----------
    file : str
        
    sheet : str, optional
        The default is 0.
    **kwargs : 
        

    Returns
    -------
    df: pandas.DataFrame

    """

    df = pd.read_excel(file,sheet)
    
    if all(["start" in df.columns, "end" in df.columns]):
        df.start = pd.to_datetime(df.start,dayfirst=True)
        df.end = pd.to_datetime(df.end,dayfirst=True)
    else:
        print("{}: WARNING - no start and end values defined".format(__name__))   

    '''    
    try:
        df['id'] = df['id'].astype(str)
    except:
        df['id'] = df.index.astype(str)    
    '''
    #df.columns = df.columns.str.lower()
    #print(df)
    return df

def import_list(data,**kwargs):
    """
    import a list and generate a dataframe
    uses the first item as column names and trys to convert start and end to datetime
    
    Parameters
    ----------
    data: list
    
    Returns
    -------
    df: pandas.DataFrame
    
    """
    df = pd.DataFrame(data[1:],columns=data[0])
    df.columns = df.columns.str.lower()
    df.start = pd.to_datetime(df.start,dayfirst=True)
    df.end = pd.to_datetime(df.end,dayfirst=True)
    
    return df

def import_mpp_xml(filename,**kwargs):
    """
    import a ms project xml file
    WARNING: this is definitely beta and has only been tried on one file!
    
    Parameters
    ---------
    filename: str
    
    Returns
    -------
    df: pandas.DataFrame
    
    """
    
    with open(filename,'r') as f:
        xml = xmltodict.parse(f.read())
        
    df_all = pd.DataFrame(xml['Project']['Tasks']['Task'])
    
    
    df_all['predecessors'] = df_all.loc[df_all.PredecessorLink.map(
        lambda x: isinstance(x,dict)),'PredecessorLink'].map(lambda x: x['PredecessorUID'])
    
    df_all.loc[df_all.predecessors.isna(),'predecessors'] = df_all.loc[df_all.PredecessorLink.map(
        lambda x: isinstance(x,list)),'PredecessorLink'].map(
            lambda x: ','.join([i['PredecessorUID'] for i in x]))
    
    df = df_all[['UID','WBS','Name','Start','Finish','predecessors']].copy()
    
    datefmt = '%Y-%m-%dT%H:%M:%S'
    
    df.Start = pd.to_datetime(df.Start,format=datefmt)
    df.Finish = pd.to_datetime(df.Finish,format=datefmt)
    
    df = df.rename(columns=dict(
        UID = 'id',
        Name = 'name',
        Start = 'start',
        Finish = 'end')
        )
    
    df.name = df.WBS+' '+df.name
    return df


def choosefile(path = './'):
    """
    uses tkinter.filedialogue.askopenfilename to pick a file
    """
    dialogue = Tk()
    dialogue.withdraw()
    dialogue.wm_attributes('-topmost', 1)
    filename = askopenfilename(parent=dialogue, initialdir=path)
    
    return filename
# -*- coding: utf-8 -*-
"""
import functions for giganttic

Created on Fri May  5 08:27:58 2023

@author: dhancock
"""
import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd
import xmltodict


def import_csv(file, headers=True, columns=None, **kwargs):
    """
    headers: if the first line of the csv file has headers
    columns: if headers is false, use this list as dataframe columns
    """

    with open(file, 'r', encoding="utf8") as file_object:
        csvdata = csv.reader(file_object)
        # nestedlist = [row for row in csvdata]
        nestedlist = list(csvdata)

    events = nestedlist

    # create dataframe
    if headers is True:  # read the top row of the file to get headers
        dataframe = pd.DataFrame(events[1:])
        dataframe.columns = events[0]
    else:  # manually apply column labels based on keyword or assumption
        dataframe = pd.DataFrame(events)
        if columns is None:
            columns = ["id", "activity_name", "start", "end"]
            try:
                dataframe.columns = columns
            except AssertionError:
                print(f'Assumed columns were {columns}')
                raise

    if all([
            "start" in dataframe.columns,
            "end" in dataframe.columns,
            ]):
        if kwargs.get('numerical_dates', False):
            dataframe.start = pd.to_numeric(dataframe.start, errors='coerce')
            dataframe.end = pd.to_numeric(dataframe.end, errors='coerce')
            dataframe.start = dataframe.start.fillna(dataframe.end)
            dataframe.end = dataframe.end.fillna(dataframe.start)
        else:
            # dataframe.start = pd.to_datetime(dataframe.start, dayfirst=True, format='mixed')
            # dataframe.end = pd.to_datetime(dataframe.end, dayfirst=True, format='mixed')
            dataframe.start = pd.to_datetime(dataframe.start, dayfirst=True, format='%d/%m/%Y')
            dataframe.end = pd.to_datetime(dataframe.end, dayfirst=True, format='%d/%m/%Y')

    else:
        print(f"{__name__}: WARNING - no start and end values defined")

    if 'yvalue' in dataframe.columns:
        dataframe.yvalue = pd.to_numeric(dataframe.yvalue, errors='coerce')

    return dataframe


def import_excel(file,
                 sheet=0,
                 # **kwargs
                 ):
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
    dataframe: pandas.DataFrame

    """

    dataframe = pd.read_excel(file, sheet)

    if all(["start" in dataframe.columns, "end" in dataframe.columns]):
        # dataframe.start = pd.to_datetime(dataframe.start, dayfirst=True, format='mixed')
        # dataframe.end = pd.to_datetime(dataframe.end, dayfirst=True, format='mixed')
        dataframe.start = pd.to_datetime(dataframe.start, dayfirst=True)
        dataframe.end = pd.to_datetime(dataframe.end, dayfirst=True)
    else:
        print(f"{__name__}: WARNING - no start and end values defined")

    return dataframe


def import_list(data,
                # **kwargs
                ):
    """
    import a list and generate a dataframe
    uses the first item as column names
    and trys to convert start and end to datetime

    Parameters
    ----------
    data: list

    Returns
    -------
    dataframe: pandas.DataFrame

    """
    dataframe = pd.DataFrame(data[1:], columns=data[0])
    dataframe.columns = dataframe.columns.str.lower()
    dataframe.start = pd.to_datetime(dataframe.start, dayfirst=True)
    dataframe.end = pd.to_datetime(dataframe.end, dayfirst=True)

    return dataframe


def import_mpp_xml(filename,
                   # **kwargs
                   ):
    """
    import a ms project xml file
    WARNING: this is definitely beta and has only been tried on one file!

    Parameters
    ---------
    filename: str

    Returns
    -------
    dataframe: pandas.DataFrame

    """

    with open(filename, 'r', encoding="utf8") as file_object:
        xml = xmltodict.parse(file_object.read())

    df_all = pd.DataFrame(xml['Project']['Tasks']['Task'])

    df_all['predecessors'] = df_all.loc[df_all.PredecessorLink.map(
        lambda x: isinstance(x, dict)), 'PredecessorLink'].map(
            lambda x: x['PredecessorUID'])

    df_all.loc[
        df_all.predecessors.isna(), 'predecessors'] = df_all.loc[
            df_all.PredecessorLink.map(
                lambda x: isinstance(x, list)), 'PredecessorLink'].map(
                    lambda x: ','.join([i['PredecessorUID'] for i in x]))

    dataframe = df_all[['UID', 'WBS', 'Name', 'Start', 'Finish', 'predecessors']].copy()

    # datefmt = '%Y-%m-%dT%H:%M:%S'

    # dataframe.Start = pd.to_datetime(dataframe.Start, format='mixed')
    # dataframe.Finish = pd.to_datetime(dataframe.Finish, format='mixed')
    dataframe.Start = pd.to_datetime(dataframe.Start)
    dataframe.Finish = pd.to_datetime(dataframe.Finish)

    dataframe = dataframe.rename(columns={'UID': 'id',
                                          'Name': 'activity_name',
                                          'Start': 'start',
                                          'Finish': 'end'})

    dataframe.activity_name = dataframe.WBS+' '+dataframe.activity_name
    return dataframe


def choosefile(path='./'):
    """
    uses tkinter.filedialogue.askopenfilename to pick a file
    """
    dialogue = Tk()
    dialogue.withdraw()
    dialogue.wm_attributes('-topmost', 1)
    filename = askopenfilename(parent=dialogue, initialdir=path)

    return filename

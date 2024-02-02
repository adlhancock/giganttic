# -*- coding: utf-8 -*-
"""
data manipulation ond filtering functions for giganttic

Created on Fri May  5 08:30:31 2023

@author: dhancock
"""
from datetime import datetime as dt
import pandas as pd


def get_datestring():
    """ uses dt.now() to return a yyymmdd string
    """

    return dt.now().strftime("%Y%m%d")


def filter_data(df, column, regex):
    """
    filters dataframe and reindexes

    Parameters
    ----------
    df : TYPE
        DESCRIPTION.
    column : TYPE
        DESCRIPTION.
    regex : TYPE
        DESCRIPTION.

    Returns
    -------
    df : TYPE
        DESCRIPTION.
    """
    df = df[df[column].str.contains(regex,
                                    regex=True,
                                    na=False)].reset_index(drop=True)
    return df


def extract_milestones(df,
                       milestone_columns=None):
    """
    extracts milestones if the dataframe has columns with milestone dates

    Parameters
    ---------
    df: pandas.DataFrame

    milestones: list, optional
        If None or not specified, will look for:
            ['T0','T1','T2','T3','T4','T5','R0','R1','R2','R3','R4']

    Returns
    ------
    df: pandas.DataFrame
    """

    if milestone_columns is None:
        milestone_columns = ['T0', 'T1', 'T2', 'T3', 'T4', 'T5',
                             'R0', 'R1', 'R2', 'R3', 'R4']
    df['activity_id'] = df.index.map(lambda x: str(x).zfill(4))
    df['ordering'] = df.activity_id.str.zfill(4)
    df['row_type'] = 'Activity'
    for ms_number, ms in enumerate(milestone_columns):
        ms_id = str(ms_number).zfill(4)
        # activities_with_this_ms = df[pd.notna(df[ms])]
        activities_with_this_ms = df.loc[df[ms].notna()]
        for row_number, row in activities_with_this_ms.iterrows():
            # for row in activities_with_this_ms:
            '''
            newrow = row.copy()
            newrow.row_type = 'Milestone'
            newrow['activity_name'] = f'({ms})'
            newrow.activity_id = row['activity_id']
            newrow.ordering = row['activity_id'] + f'.{ms_id}'
            newrow.start = row[ms]
            newrow.end = row[ms]
            newrow.miilestone = ms
            #newrow.loc[:,milestone_columns] = float('nan')
            #newrow.set_index(row.ordering)
            #print(newrow)
            #input()
            '''

            newrow = pd.DataFrame({
                'row_type': 'Milestone',
                'activity_name': '({}) {}'.format(ms, row["activity_name"]),
                # 'ylabel': f'({ms})',
                'activity_id': row['activity_id'],
                # 'milestone_id': ms_id,
                'ordering': row['activity_id'] + f'.{ms_id}',
                'start': row[ms],
                'end': row[ms],
                'milestone': ms,
                ms: row[ms]
                },
                index=['ordering']
                )
            for column in row.keys():
                if column not in newrow.keys():
                    newrow[column] = row[column]
            for m in milestone_columns:
                newrow[m] = float('nan')
            df = pd.concat([df, newrow])
            df = df[df.end.notna()]
    df = df.drop_duplicates()
    df = df.sort_values('ordering').reset_index(drop=True)
    return df


def categorise_rows(df):
    if 'row_type' not in df.columns:
        df['row_type'] = 'Activity'
        df.loc[df.end == df.start, 'row_type'] = 'Milestone'
    return df


def assign_activity_ids(df):
    if 'activity_id' not in df.columns:
        assert 'WBS' in df.columns, 'dataframe must have WBS to assign activity ids'
        df['activity_id'] = df.WBS.map(lambda x: df.WBS.unique().tolist().index(x))
    try:
        df.activity_id = df.activity_id.map(float)
    except ValueError:
        raise ValueError('activity_id must be numerical')
    return df


def autopopulate_milestones(df):
    """ tries to autopopulate milestones by looking for similarities in names"""
    if 'row_type' not in df.columns:
        df = categorise_rows(df)
    if 'activity_id' not in df.columns:
        df = assign_activity_ids(df)
    if 'milestone' not in df.columns:
        df['milestone'] = float('nan')
        for i, activity_row in df.loc[df.row_type == 'Activity'].iterrows():
            activity_name = activity_row['activity_name']
            df.loc[df.activity_id == activity_row['activity_id'],
                   'milestone'] = df.activity_name.map(
                               lambda x: ''.join(x.split(activity_name)).strip())
    return df


def flatten_milestones(df):
    """
    returns the dataframe with additional columns ylabel and yvalue
    which clears the milestone labels and puts
    them in a single line below the main task bar

    Parameters
    ----------
        df: pandas.DataFrame

    Returns
    -------
        df: pandas.DataFrame
    """
    df = categorise_rows(df)
    df = assign_activity_ids(df)

    df['ylabel'] = df.get('ylabel', df.activity_name)

    # try to autopopulate milestone labels if they're missing
    if 'milestone' not in df.columns:
        print('WARNING: no milestone column in dataframe. Trying to autopopulate')
        df = autopopulate_milestones(df)

    df.loc[df['row_type'] == 'Milestone', 'ylabel'] = ''
    df['yvalue'] = df.activity_id.map(lambda x: df.activity_id.unique().tolist().index(x)) * 1.8
    # df['yvalue'] = df.activity_id.map(float) * 1.8
    # df['yvalue'] = [x*1.8 for x in np.range(len(df))]
    df.loc[df['row_type'] == 'Milestone', 'yvalue'] = df.yvalue + 0.7
    # ylocs = df.activity_id
    # yvalues = [df.yvalue.tolist(),df.ylabel.tolist()]
    return df


def get_durations(df, milestone_cols):
    """
    if overall start and end aren't defined, uses a list of milestone columns
    to generate them.

    Parameters
    ----------
    df : pandas.DataFrame

    milestone_cols : TYPE

    Returns
    -------
    df: pandas.DataFrame

    """

    def startend(row, func):
        """
        finds the min or max of a df row which includes nan values

        Parameters
        ---------
        row: pandas.DataFrame row
            one line dataframe
        func
            must be min or max

        Returns
        -------
        out: float

        """
        assert func in [min, max], 'function must be min or max'
        if list(row) == [pd.NaT]*5:
            out = dt.now()
        else:
            out = func([x for x in row if x is not pd.NaT])
        return out

    df['start'] = df[milestone_cols].apply(lambda x: startend(x, min), axis=1)
    df['end'] = df[milestone_cols].apply(lambda x: startend(x, max), axis=1)
    df['duration'] = df.end-df.start
    return df

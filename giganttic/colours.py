# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 16:55:00 2023

@author: dhancock
"""

import pandas as pd
from itertools import cycle
from matplotlib import colors, colormaps


def get_colours(df,
                fillcolumn=None,
                bordercolumn=None,
                customcolour_column='activity_name',
                cmap_fill=colormaps['viridis'],
                cmap_border=colormaps['tab10'],
                customcolours=None,
                default_fill="#002F56",
                default_border=None,
                recolour=False,
                **kwargs
                ):
    """
    gets colours for the dataframe

    Parameters
    ----------

    df
        dataframe
    fillcolumn
        which column is used to set the fill colour
    bordercolumn
        which column is used to set the border colour
    cmap_fill
        The default is matplotlib.colormaps['viridis']
    default_fill
        event fill if cannot be found
    default_border : TYPE, optional
        event border colour
    **kwargs : TYPE
        DESCRIPTION.

    Returns
    -------
    df

    cmaps: dict
        keys are 'fillcolour', 'bordercolour', 'custommcolour'

    """

    def get_colour_dict(df_column: pd.Series, colourmap):
        """ creates a dictionary to populate a colour column"""

        values = df_column.unique().tolist()
        nvalues, ncolours = len(values), len(colourmap.colors)
        if nvalues < ncolours*0.5 and ncolours > 30:
            # case - lots of colours and not many values
            colours = [colourmap(x/nvalues) for x in range(nvalues)]
        elif nvalues > ncolours:
            # case - not enough colours
            print(f'WARNING: more values in {df_column.name} than colours in {colourmap.name}')
            print(f'trying to map {len(values)} values to {len(colourmap.colors)} colours')
            print('this will result in duplicate colours')

            iterator = cycle(colourmap.colors)
            colours = [next(iterator) for x in range(nvalues)]
        else:
            # case - just right
            colours = colourmap.colors[0:nvalues]
        colours = [colors.to_hex(c) for c in colours]
        assert len(colours) == len(values), 'counts of colours and values don\'t match'
        return dict(zip(values, colours))

    # if colourmaps are provided as a list of colours, convert them to colormaps
    if isinstance(cmap_fill, list):
        cmap_fill = colors.ListedColormap(cmap_fill, 'cmap_fill')
    if isinstance(cmap_border, list):
        cmap_border = colors.ListedColormap(cmap_border, 'cmap_border')

    for colourcolumn in ['fillcolour', 'bordercolour', 'customcolour']:
        # create the colour columns if needed
        if colourcolumn not in df.columns:
            df[colourcolumn] = None
        # blank them if going to re-colour from scratch
        if recolour is True:
            df[colourcolumn] = None

    # set the fill colour
    if fillcolumn is not None:
        fill_dict = get_colour_dict(df[fillcolumn], cmap_fill)
        # print(f'DEBUG: {fill_dict}')
        df.loc[df.fillcolour.isna(), 'fillcolour'] = df[fillcolumn].map(fill_dict.get)
    else:
        df.fillcolour = default_fill

    # set the border colour
    if bordercolumn is not None:
        border_dict = get_colour_dict(df[bordercolumn], cmap_border)
        df.loc[df.bordercolour.isna(), 'bordercolour'] = df[bordercolumn].map(border_dict.get)
    else:
        df.bordercolour = default_border

    # populate any custom colours
    if customcolours is not None:
        for term in customcolours:
            df.loc[df[customcolour_column].map(lambda x: term in str(x)),
                   ['fillcolour', 'customcolour']] = customcolours.get(term)

    cmaps = {'fill': cmap_fill, 'border': cmap_border, 'custom': customcolours}

    # convert all notna colours to hex
    for colourcolumn in ('fillcolour', 'bordercolour', 'customcolour'):
        df.loc[df[colourcolumn].notna(), colourcolumn] = df.loc[
            df[colourcolumn].notna(), colourcolumn].map(colors.to_hex)

    return df, cmaps

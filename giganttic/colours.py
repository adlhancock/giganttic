# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 16:55:00 2023

@author: dhancock
"""
from itertools import cycle
from matplotlib import colors, colormaps

def get_colours(df,
               fillcolumn=None,
               bordercolumn=None,
               customcolour_column='name',
               cmap_fill=colormaps['viridis'],
               cmap_border=colormaps['tab10'],
               customcolours=None,
               default_fill="#002F56",
               default_border=None,
               recolour=True,
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
    fillcolour

    bordercolour

    df

    cmaps: dict
        keys are 'fill' and 'border'

    """

    # set the colourmaps
    if isinstance(cmap_fill, list):
        cmap_fill = colors.ListedColormap(cmap_fill, 'cmap')

    if cmap_border is not None:
        if isinstance(cmap_border, list):
            cmap_border = colors.ListedColormap(cmap_border, 'cmap_border')
    else:
        cmap_border = cmap_fill

    if recolour is True:
        df['fillcolour'] = None
        df['bordercolour'] = None
        df['customcolour'] = None

    #set the fill colour
    if fillcolumn is not None:
        fillvalues = df[fillcolumn].unique().tolist()
        if len(fillvalues) < len(cmap_fill.colors)*0.5 or len(cmap_fill.colors) > 30:
            #fillcolor = cmap(fillvalues.index(fillvalue)/len(fillvalues))
            df.fillcolour = df[fillcolumn].map(
                lambda x: cmap_fill(fillvalues.index(x)/len(fillvalues)))
        else:
            iterator = cycle(cmap_fill.colors)
            fillcolours = [next(iterator) for x in range(len(fillvalues))]
            #fillcolor = fillcolours[fillvalues.index(fillvalue)]
            df.fillcolour = df[fillcolumn].map(
                lambda x: fillcolours[fillvalues.index(x)])
    else:
        df.fillcolour = default_fill

    #set the border colour
    if bordercolumn is not None:
        bordervalues = df[bordercolumn].unique().tolist()
        df.bordercolour = df[bordercolumn].map(
            lambda x: cmap_border(bordervalues.index(x)/len(bordervalues)))
    else:
        df.bordercolor = default_border

    # populate any custom colours
    if customcolours is not None:
        #print('DEBUG: applying custom colours')
        """
        for row, event in df.iterrows():
            for item in customcolours:  
                if item in str(event[customcolour_column]): # uses a very simple string search
                    #print('DEBUG: applying {} to {}'.format(customcolours[item],event['name']))    
                    event.fillcolour = customcolours[item]
                    event.customcolour = customcolours[item]
                    #print('DEBUG: fill colour = {}'.format(event.fillcolour))
                    #print('DEBUG: custom colour = {}'.format(event.customcolour))
        """
        for term in customcolours:
            df.loc[df[customcolour_column].map(lambda x: term in str(x)),
                   ['fillcolour','customcolour']] = customcolours[term]


    cmaps = {'fill':cmap_fill,'border':cmap_border,'custom':customcolours}
    # convert all notna colors to hex
    
    for colourcolumn in ('fillcolour', 'bordercolour','customcolour'):
        df.loc[df[colourcolumn].notna(),colourcolumn] = df.loc[
            df[colourcolumn].notna(),colourcolumn].map(colors.to_hex)
    
    return df, cmaps
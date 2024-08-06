# -*- coding: utf-8 -*-
""" giganntic figure sizes
Created on Mon Sep 25 23:29:20 2023

@author: dhancock
"""
_verbose = True


def get_figure_dimensions(rows, ratio=1.414, short_side=10):

    figure_sizes = [
            {'name': 'tiny',
             'max_rows': 10,
             'font_size': 10,
             'figure_width': short_side*2,
             'figure_height': rows,  # thin landscape ratio
             'figure_dpi': 100},
            {'name': 'small',
             'max_rows': 40,
             'font_size': 8,
             'figure_width': short_side*ratio,
             'figure_height': short_side,  # landscape ratio
             'figure_dpi': 100},
            {'name': 'medium',
             'max_rows': 65,
             'font_size': 7,
             'figure_width': short_side,
             'figure_height': short_side*ratio,  # portrait ratio
             'figure_dpi': 100},
            {'name': 'large',
             'max_rows': 120,
             'font_size': 6,
             'figure_width': short_side,
             'figure_height': rows/2,  # tall portrait ratio
             'figure_dpi': 80},
            {'name': 'huge',
             'max_rows': 240,
             'font_size': 4,
             'figure_width': short_side,
             'figure_height': rows/1.5,  # very tall portrait ratio
             'figure_dpi': 70},
            {'name': 'giant',
             'max_rows': 500,
             'font_size': 4,
             'figure_width': short_side/1.5,
             'figure_height': rows/3,  # try to squeeze it all in
             'figure_dpi': 60},
            {'name': 'nearly_illegible',
             'max_rows': 900,
             'font_size': 2,
             'figure_width': short_side/1.5,
             'figure_height': rows/2,  # try to squeeze it all in
             'figure_dpi': 60},
    ]

    # use the max_row values in the figure_sizes dict to set figure_size
    size_names = list(figure_sizes.keys())
    size_names.remove('default')
    max_row_values = [figure_sizes[size_name]['max_rows']
                      for size_name in size_names]
    size_dictionary = dict(zip(max_row_values, size_names))
    for max_size in sorted(max_row_values, reverse=True):
        if rows < max_size:
            figure_size = size_dictionary[max_size]

    
    
    return dimensions


def get_figure_dimensions(n_rows):
    """ works out figure size, dpi, and font size from number of rows
    Parameters
    ----------
    n_rows

    Returns
    -------
    dimensions

    """


    figure_sizes = get_figure_sizes(rows, ratio, short_side=10)
    figure_size = kwargs.get('figure_size', None)

    if isinstance(figure_size, list):
        figure_width, figure_height = figure_size
        figure_size = 'manual'
    else:
        pass
    # apply the figure dimensions
    figure_dimensions = figure_sizes.get(figure_size,
                                         figure_sizes['default'])

    print(f'DEBUG:{rows:<5} {figure_size:<10} {figure_dimensions}')
    dimensions = {'size': figure_size,
                  'rows': rows,
                  'height': figure_dimensions.get('figure_height'),
                  'width': figure_dimensions.get('figure_width'),
                  'font_size': kwargs.get('font_size', figure_dimensions.get('font_size')),
                  'dpi': kwargs.get('figure_dpi', figure_dimensions.get('figure_dpi'))}

    return dimensions

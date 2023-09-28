# -*- coding: utf-8 -*-
""" giganntic figure sizes
Created on Mon Sep 25 23:29:20 2023

@author: dhancock
"""

def get_figure_sizes(rows, ratio = 1.414, short_side=10):

    figure_sizes = {
        'tiny':{
            'max_rows':10,
            'font_size':10,
            'figure_width':short_side*2,
            'figure_height':rows, # thin landscape ratio
            'figure_dpi':100},
        'small':{
            'max_rows':40,
            'font_size':8,
            'figure_width':short_side*ratio, 
            'figure_height':short_side, # landscape ratio
            'figure_dpi':100},
        'medium':{
            'max_rows':65,
            'font_size':7,
            'figure_width':short_side,
            'figure_height':short_side*ratio, # portrait ratio
            'figure_dpi':100},
        'large':{
            'max_rows':120,
            'font_size':6,
            'figure_width':short_side,
            'figure_height':rows/1.5, # tall portrait ratio
            'figure_dpi':80},
        'huge':{
            'max_rows':240,
            'font_size':4,
            'figure_width':short_side,
            'figure_height':rows/2, # very tall portrait ratio
            'figure_dpi':70},
        'giant':{
            'max_rows':500,
            'font_size':3,
            'figure_width':short_side/1.5,
            'figure_height':rows/2.5, # try to squeeze it all in
            'figure_dpi':60},
        'nearly_illegible':{
            'max_rows':900,
            'font_size':2,
            'figure_width':short_side/1.5,
            'figure_height':rows/2, # try to squeeze it all in
            'figure_dpi':60},
        'default':{
            'max_rows':'None',
            'font_size':2,
            'figure_width':short_side/2,
            'figure_height':rows, # 6:4 modest size
            'figure_dpi':60}
    }
    return figure_sizes
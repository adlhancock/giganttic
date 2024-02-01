# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 17:04:14 2023

@author: dhancock
"""

import os
import sys

sys.path.insert(0,os.path.abspath('..'))
import giganttic as gt

t = gt.Giganttic(data_source = '../test/exampledata1.csv')

figure = t.figure
colours = t.colours
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 16:18:29 2023

@author: dhancock
"""
#import pandas as pd
from pandas import DataFrame
from plotly import graph_objects as go
from .import_functions import import_csv, import_excel, import_mpp_xml, import_list

class Giganttic():
    figure = {}
    colours = {}
    files = {}
    #rawdata = pd.DataFrame()
    def __init__(self,**kwargs):
        self.files = kwargs.get('files',None)
        self.figure = self.Figure()
        self.colours = self.Colours()
        self.data_source = kwargs.get('data_source',None)
        if self.data_source is not None:
            self.rawdata = self.import_data(self.data_source)

    def import_data(self,data_source):
        assert isinstance(data_source, (str,list)), f'{data_source}'
        if isinstance(data_source,str):
            import_functions = {
                'csv':import_csv,
                'xlsx':import_excel,
                'xml':import_mpp_xml}
            for file_extension in import_functions:
                if data_source.endswith(file_extension):
                    data = import_functions[file_extension](data_source)
        else:
            data = import_list(data_source)
        return data

    def cleanup_data(self,**kwargs):
        pass

    def setup_figure(self,**kwargs):
        pass

    def save_images(self,**kwargs):
        pass

    class Figure(go.Figure):
        options = {}
        def __init__(self,**kwargs):
            super().__init__()
            self.options = kwargs.get('figure',None)
            pass
        def plot(self):
            pass

    class Colours(dict):
        options = {}
        def __init__(self,**kwargs):
            super().__init__()
            self.options = kwargs.get('colours',None)
            pass






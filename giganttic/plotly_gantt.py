# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 13:51:40 2023

@author: dhancock
"""


import plotly.graph_objects as go
import giganttic as gt

def plotly_gantt(df,**kwargs):
    rows_to_show = kwargs.get('rows_to_show',20)
    if rows_to_show == 'all': rows_to_show = max(df.yvalue)
    fig = go.Figure()
    fig.update_layout(dict(
        title = "Plotly Gantt Chart",
        showlegend=False,
        plot_bgcolor = '#ffffff'))
    fig.update_yaxes(
                     #autorange='reversed',
                     range = [rows_to_show,0],
                     ticktext=df.ylabel,
                     tickvals=df.yvalue,
                     tickfont=dict(size=8),
                     gridcolor='#cccccc')
    fig.update_xaxes(range=[min(df.start),max(df.end)],
                     type='date',
                     gridcolor='#cccccc')
    
    bar_size = 0.6
    ms_size = 8
    
    for i, row in df.iterrows():
        
        
        start = row.start
        finish = row.end
        yvalue = row.yvalue
        fillcolour = row.get('fillcolour',"LightSkyBlue")
        
        if start != finish:
            fig.add_shape(type="rect",
                x0=start, y0=yvalue-bar_size/2, x1=finish, y1=yvalue+bar_size/2,
                line=dict(
                    #color="RoyalBlue",
                    color=None,
                    width=0,
                ),
                fillcolor=fillcolour
                )
        else:
            mslabel = row.get('milestone','')
            fig.add_scatter(x=[finish],y=[yvalue],
                            text=[mslabel],
                            textposition='bottom center',
                            marker=dict(
                                size=ms_size,
                                symbol='diamond',
                                color=fillcolour,),
                            mode='markers+text'
                            )
    
    fig.show(renderer='browser')
    
    return fig

# test
def test():
    testfile = '/local/python/giganttic/test/exampledata1.csv'
    df = gt.import_csv(testfile)
    df['yvalue'] = list(range(len(df)))
    df['ylabel'] = df.name
    plotly_gantt(df)
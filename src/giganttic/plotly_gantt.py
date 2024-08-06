# -*- coding: utf-8 -*-
"""
plotly-based version of giganttic
Created on Tue Sep 19 13:51:40 2023

@author: dhancock
"""

import plotly.graph_objects as go
from .colours import get_colours
from .plotting_extras import get_fontsize
# from datetime import timedelta
# import pandas as pd


def gantt_chart(df,
                title='plotly giganttic',
                **kwargs):
    """ produces a gantt chart using plotly"""

    def set_up_figure(df, **kwargs):

        # how many rows to show
        rows_to_show = kwargs.get('rows_to_show', 'all')
        if rows_to_show == 'all':
            rows_to_show = df.get('yvalue', df.get('activity_name')).size

        # Range Slider
        show_rangeslider = kwargs.get('show_rangeslider', False)
        if show_rangeslider is False:
            rangeslider_thickness = 0
        else:
            rangeslider_thickness = kwargs.get('rangeslider_thickness', 0.05)

        # set up y values and labels
        if 'yvalue' not in df.columns and kwargs.get('yvalues') is None:
            # print('data has no yvalues, autogenerating')
            df['yvalue'] = df.index.tolist()
        if 'ylabel' not in df.columns and kwargs.get('ylabels') is None:
            df['ylabel'] = df['activity_name'].copy()

        # initiate figure
        fig = go.Figure()

        # option to allow numerical rather than date formatted x axis.
        if kwargs.get('numerical_dates', False) is True:
            axistype = 'linear'
        else:
            axistype = 'date'

        fig.update_layout(
            title=title,
            showlegend=kwargs.get('showlegend', False),
            plot_bgcolor='# ffffff',
            yaxis={"autorange": 'reversed',
                   "ticktext": df.ylabel,
                   "tickvals": df.yvalue,
                   "tickfont": dict(size=get_fontsize(rows_to_show)),
                   "gridcolor": None},
            xaxis={"type": axistype,
                   "gridcolor": '# cccccc',
                   "rangeslider": {"visible": show_rangeslider,
                                   "thickness": rangeslider_thickness}
                   },
            dragmode='pan'
            )
        fig.update_layout(
            xaxis=dict(range=[min(df.start), max(df.end)]),
            yaxis=dict(range=[max(df.yvalue)+1, min(df.yvalue)-1])
            )

        return fig

    def plot_shapes(df, fig, **kwargs):

        default_fill = kwargs.get('default_fill', "LightSkyBlue")
        default_border = kwargs.get('default_border', None)

        for i, row in df.iterrows():
            start = row.start
            finish = row.end
            yvalue = row.yvalue
            fillcolour = row.get('fillcolour', default_fill)
            bordercolour = row.get('bordercolour', default_border)
            bar_size = float(row.get('bar_size', kwargs.get('bar_size', 20)))
            ms_size = float(row.get('ms_size', kwargs.get('ms_size', 8)))

            if bordercolour is None:
                borderwidth = 0
            else:
                borderwidth = kwargs.get('borderwidth', 2)

            if start == finish:   # zero-length events are milestones
                # plot a diamond if it's a milestone
                mslabel = row.get('milestone', row.get('activity_name', ''))
                fig.add_scatter(x=[finish], y=[yvalue],
                                text=[mslabel],
                                textposition='top center',
                                marker=dict(
                                    size=ms_size,
                                    symbol='diamond',
                                    color=fillcolour),
                                mode='markers+text',
                                name=row.get('activity_name', i))

            else:  # everything else is a bar
                # plot a path
                fig.add_shape(
                    type='path',
                    path='M {} {} L {} {}'.format(start, yvalue, finish, yvalue),
                    line=dict(color=row.fillcolour, width=bar_size),
                    fillcolor=None
                    )

                # add borders
                if borderwidth != 0:
                    for yoffset in [bar_size, -bar_size]:
                        fig.add_shape(
                            type='path',
                            path='M {} {} L {} {}'.format(
                                start, yvalue+yoffset, finish, yvalue+yoffset),
                            line=dict(color=row.bordercolour, width=borderwidth),
                            fillcolor=None
                            )

                """
                # add bar labels - white, inside
                if kwargs.get("bar_labels", False) is True:
                    middle = start + ((finish - start)/2)
                    fig.add_annotation(
                        x=middle,
                        y=yvalue,
                        # yshift=-16,
                        text=row.get('activity_name', i),
                        showarrow=False,
                        font=dict(
                            size=0.5*bar_size,
                            color='white',
                            )
                        )
                """
                # add bar labels - black, on top
                if kwargs.get("bar_labels", False) is True:
                    fig.add_annotation(
                        x=start,
                        y=yvalue,
                        yshift=bar_size,
                        xshift=bar_size,
                        text=row.get('activity_name', i),
                        showarrow=False,
                        font=dict(
                            size=14,
                            color=kwargs.get('labelcolour','black'),
                            ),
                        align='left',
                        xanchor='left'
                        )
                    

            # Add link lines
            if all([
                    kwargs.get("plot_dependencies", False) is True,
                    ]):
                startx = float(row.end)
                endx = float(row.end)
                starty = float(row.yvalue)
                endy = float(row.depend_yvalue)
                if row.start == row.end:
                    arrow_size = 2
                else:
                    arrow_size = kwargs.get('arrow_size', bar_size*0.7)

                fig.add_annotation(
                    ax=startx,
                    ay=starty,
                    ayref="y",
                    axref="x",
                    startstandoff=bar_size/3,
                    x=endx,
                    y=endy,
                    xref="x",
                    yref="y",
                    standoff=bar_size/2,
                    text=None,
                    showarrow=True,
                    arrowhead=4,
                    arrowsize=0.4,
                    arrowwidth=arrow_size,
                    arrowcolor=row.fillcolour,
                    visible=True,
                    )
                
                """
                if row.start != row.end:
                    fig.add_shape(
                        type='circle',
                        xanchor=startx,
                        yanchor=starty,
                        x0=-bar_size/2,
                        y0=-bar_size/2,
                        x1=bar_size/2,
                        y1=bar_size/2,
                        xref='x',
                        yref='y',
                        xsizemode='pixel',
                        ysizemode='pixel',
                        fillcolor=row.fillcolour,
                        line=dict(width=0),
                        )
                """

                """
                link_path = 'M {} {} L {} {} Q {} {} {} {} L {} {}'.format(
                    startx-0.1, starty,  # starting point
                    startx, starty,  # start of curve
                    startx, starty,  # middle of curve
                    endx, (starty + endy) / 2,  # end of curve
                    endx, endy)  # end of line

                # Add the arrow shape
                fig.add_shape(
                    type='path',
                    path=link_path,
                    line=dict(color=row.fillcolour, width=bar_size),
                    fillcolor=None
                )
                """

    def make_yaxis_range_menu(df,
                              yaxis_ranges=[5, 10, 50, 100, 1000],
                              **kwargs):
        rows_to_show = kwargs.get('rows_to_show', 'all')
        if rows_to_show == 'all':
            rows_to_show = df.yvalue.max()
        ranges = {f'default ({rows_to_show})': [rows_to_show+1, -1],
                  'all': [df.yvalue.max()+1, -1]}
        fontsizes = {f'default ({rows_to_show})': get_fontsize(rows_to_show),
                     'all': get_fontsize(df.yvalue.max())}
        for n in yaxis_ranges:
            ranges[f'{n} rows'] = [n+1, -1]
            fontsizes[f'{n} rows'] = get_fontsize(n)

        yaxis_range_buttons = []
        for r in ranges:
            yaxis_range_buttons.append(
                dict(
                    args=[{'textfont_size': fontsizes[r]},
                          {'yaxis.range': ranges[r],
                           'yaxis.tickfont.size': fontsizes[r]}],
                    label=r,
                    method='update'
                    ))

        yaxis_range_menu = dict(buttons=yaxis_range_buttons,
                                direction="down",
                                pad={"r": 10, "t": 10},
                                showactive=True,
                                x=0.95,
                                xanchor="right",
                                y=1.1,
                                yanchor="top")
        return yaxis_range_menu

    def make_filter_menu(df, **kwargs):

        milestone_filters = {'all': df.yvalue.notna(),
                             'no milestones': df.start != df.end,
                             'just milestones': df.start == df.end}

        manual_filters = kwargs.get('manual_filters', None)

        filter_column = kwargs.get('filter_column', None)
        if filter_column is not None:
            column_values = df[filter_column].unique().tolist()
            column_filters = {'all': df[filter_column].notna()}
            column_filters.update(dict(
                zip([x for x in column_values],
                    (df[filter_column] == x for x in column_values))))

        filters = {}
        if 'auto milestones' in filters:
            filters.update(milestone_filters)
            filters.pop('auto milestones')
        if manual_filters is not None:
            filters.update(manual_filters)
        if filter_column in df.columns:
            filters.update(column_filters)

        filter_buttons = []
        for i in filters:
            row_count = len(df.loc[filters[i]])
            yvalues = list(df.loc[filters[i], 'yvalue'])
            # print(f'DEBUG: row_count = {row_count}')
            filter_buttons.append(
                dict(
                    args=[
                        {'visible': list(filters[i]),
                         'textfont_size': get_fontsize(row_count)},
                        {'yaxis.tickvals': [yvalues.index(x) for x in yvalues],
                         # 'yaxis.tickvals': list(df.loc[filters[i], 'yvalue']),
                         'yaxis.autorange': True,
                         'yaxis.tickfont.size': get_fontsize(row_count),
                         'yaxis.ticktext': list(df.loc[filters[i], 'ylabel'])
                         # 'yaxis.range': list([len(df.loc[filters[i]]), -1])
                         },
                        ],
                    label=i,
                    method='update'),
                )

        filter_menu = dict(buttons=filter_buttons,
                           direction="down",
                           pad={"r": 10, "t": 10},
                           showactive=True,
                           x=0.3,
                           xanchor="left",
                           y=1.1,
                           yanchor="top"
                           )
        return filter_menu

    # main function
    fig = set_up_figure(df, **kwargs)
    df, cmaps = get_colours(df, **kwargs)
    plot_shapes(df, fig, **kwargs)

    # optional clever menus
    menus = []
    if kwargs.get('filters_menu', False) is True:
        menus.append(make_filter_menu(df, **kwargs))
    if kwargs.get('yaxis_range_menu', False) is True:
        menus.append(make_yaxis_range_menu(df, **kwargs))
    if len(menus) > 0:
        fig.update_layout(updatemenus=menus)

    ax = 'no axes generated, because plotly'
    return ax, fig

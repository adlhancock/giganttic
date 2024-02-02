""" __init__ file for giganttic
"""
# from .classes import *
from .data_import import *
from .data_modify import *
from .data_export import *
from .mpl_gantt import gantt_chart as mpl_gantt
from .plotly_gantt import gantt_chart as plotly_gantt
from .plotting_extras import plot_by_column, get_fontsize
from .colours import get_colours
from .giganttic import *

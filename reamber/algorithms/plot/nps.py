from typing import Tuple, List

import matplotlib.pyplot as plt
import numpy as np

from reamber.algorithms.plot.timedXAxis import timed_x_axis
from reamber.base.RAConst import RAConst
from reamber.base.lists.NotePkg import NotePkg


def nps_plot(pkg: NotePkg, ax:plt.Axes = None, window=1000, stride=None, legend=True, tick_step_size=60000,
             bar_kwargs=None) -> plt.Axes:
    """ This creates an NPS Plot with the axes.

    :param pkg: Any Note Package
    :param ax: The axis to plot on, if None, we use gca()
    :param window: The window of the roll
    :param stride: The stride length of the roll
    :param legend: Whether to show the legend
    :param tick_step_size: How many milliseconds per tick
    :param bar_kwargs: The kwargs to pass into plot()
    """
    if ax is None: ax = plt.gca()
    if bar_kwargs is None: bar_kwargs = {}
    dns = pkg.rolling_density(window=window, stride=stride)

    prev_heights = None
    for lis_type, lis in dns.items():
        if all(v == 0 for v in lis.values()): continue
        curr_indexes = list(lis.keys())
        curr_heights = [RAConst.sec_to_msec(v / window) for v in list(lis.values())]
        ax.bar(curr_indexes, curr_heights,
               width=pkg.duration() / (len(lis.keys()) - 1),  # -1 to make sure there's no gaps
               bottom=prev_heights,  # Aligns next bar heights with previous
               label=lis_type,
               **bar_kwargs)  # Aligns the bars next to each other
        prev_heights = curr_heights
    if legend: ax.legend()
    ax.set_xlim(left=pkg.first_offset(), right=pkg.last_offset())
    ax = timed_x_axis(ax=ax, step_size=tick_step_size)
    return ax

def nps_plot_by_key(pkg: NotePkg, fig:plt.Figure = None, shape: Tuple = None,
                    window=1000, stride=None, title=True, legend=True, bar_kwargs=None) -> plt.Figure:
    """ This creates an NPS Plot with the axes.

    :param pkg: Any Note Package
    :param fig: The figure to plot on, if None, we use gcf()
    :param shape: The shape of the axes to take. (rows, columns)
    :param window: The window of the roll
    :param stride: The stride length of the roll
    :param title: Whether to show the key titles
    :param legend: Whether to show legend. False to show none, True to show on first, 'all' to show on all
    :param bar_kwargs: The kwargs to pass into plot()
    """
    if fig is None: fig = plt.gcf()
    if bar_kwargs is None: bar_kwargs = {}

    keys = pkg.max_column() + 1  # This gives us the keys
    if shape is None:
        rows = keys
        cols = 1
        shape = (rows, cols)
    else:
        assert shape[0] * shape[1] >= keys, "Shape must be able to hold all keys."

    ax: np.ndarray = fig.subplots(nrows=shape[0], ncols=shape[1],
                                  sharex='all', sharey='all')
    ax = ax.flatten()

    for key in range(keys):
        if legend == 'all':
            nps_plot(pkg.in_columns([key]), ax=ax[key], window=window, stride=stride, legend=True, bar_kwargs=bar_kwargs)
        elif legend is True and key == 0:
            nps_plot(pkg.in_columns([key]), ax=ax[key], window=window, stride=stride, legend=True, bar_kwargs=bar_kwargs)
        else:
            nps_plot(pkg.in_columns([key]), ax=ax[key], window=window, stride=stride, legend=False, bar_kwargs=bar_kwargs)

        ax: List[plt.Axes]
        if title: ax[key].set_title(f"Key: {key}")

    fig.tight_layout()
    return fig

import matplotlib.pyplot as plt
import numpy as np

from reamber.base.RAConst import RAConst


def timedXAxis(ax: plt.Axes, stepSize: float = 60000) -> plt.Axes:
    """ Makes the current axis use a custom time tick instead of just plain milliseconds """
    ticks = np.arange(0, ax.get_xlim()[1], stepSize)
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{int(RAConst.mSecToMin(t))}:{int(RAConst.mSecToSec(t) % 60):02d}" for t in ticks])
    ax.margins(x=0)
    return ax

from reamber.osu.OsuMap import OsuMap
import matplotlib.pyplot as plt

from reamber.algorithms.analysis.generic.rollingDensity import rollingDensity
import os

m = OsuMap()
m.readFile("PLANETSHAPER.osu")

rollingDensity(m.notes.hits().offsets(), rollingWindowS=2).plot()
plt.show()
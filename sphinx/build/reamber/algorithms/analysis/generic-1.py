from reamber.osu.OsuMapObj import OsuMapObj
import matplotlib.pyplot as plt

from reamber.algorithms.analysis.generic.rollingDensity import rollingDensity
import os

m = OsuMapObj()
m.readFile("../../../../../rsc/maps/osu/PLANETSHAPER.osu")

rollingDensity(m.notes.hits().offsets(), rollingWindowS=2).plot()
plt.show()
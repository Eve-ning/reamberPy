from reamber.algorithms.analysis.note.nps import nps, npsPlot
from reamber.osu.OsuMap import OsuMap
import matplotlib.pyplot as plt

m = OsuMap()
m.readFile("PLANETSHAPER.osu")
npsPlot(m, binSize=500)
plt.show()
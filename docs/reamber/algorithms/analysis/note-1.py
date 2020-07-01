from reamber.algorithms.plot.nps import npsPlot
from reamber.osu.OsuMapObj import OsuMapObj
import matplotlib.pyplot as plt

m = OsuMapObj()
m.readFile("PLANETSHAPER.osu")
npsPlot(m, binSize=500)
plt.show()
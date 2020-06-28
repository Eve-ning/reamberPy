from reamber.algorithms.analysis.note.nps import nps, npsPlot
from reamber.osu.OsuMapObj import OsuMapObj
import matplotlib.pyplot as plt

m = OsuMapObj()
m.readFile("../../../../../rsc/maps/osu/PLANETSHAPER.osu")
npsPlot(m, binSize=500)
plt.show()
from reamber.algorithms.plot.nps import nps_plot
from reamber.osu.OsuMap import OsuMap
import matplotlib.pyplot as plt

m = OsuMap.read_file("plot/PLANETSHAPER.osu")
nps_plot(m, binSize=500)
plt.show()
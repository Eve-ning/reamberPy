from reamber.osu.OsuMap import OsuMap
import matplotlib.pyplot as plt

m = OsuMap()
m.readFile("PLANETSHAPER.osu")

m.notes.hits().rollingDensity(2).plot()
plt.show()
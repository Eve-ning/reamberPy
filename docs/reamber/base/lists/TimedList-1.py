from reamber.osu.OsuMap import OsuMap
import matplotlib.pyplot as plt

m = OsuMap()
m.readFile("PLANETSHAPER.osu")

density = m.notes.hits().rollingDensity(window=5000, stride=2500)
plt.plot(list(density.keys()), list(density.values()))
plt.show()
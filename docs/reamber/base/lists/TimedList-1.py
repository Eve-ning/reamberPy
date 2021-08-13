from reamber.osu.OsuMap import OsuMap
import matplotlib.pyplot as plt

m = OsuMap.read_file("PLANETSHAPER.osu")

density = m.notes.hits().rolling_density(window=5000, stride=2500)
plt.plot(list(density.keys()), list(density.values()))
plt.show()
from src.osu.OsuMapObject import OsuMapObject
import matplotlib.pyplot as plt

m = OsuMapObject()
m.readFile("John Wasson - Caravan (Evening) [drown].osu")

t = [p.bpm for p in m.timingPoints if type(p).__name__ == "OsuTimingPoint"]

plt.plot(t)
plt.show()

m.version = "ex"

m.writeFile("John Wasson - Caravan (Evening) [ex].osu")

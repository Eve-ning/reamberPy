from reamber.osu import OsuMap
from reamber.osu.lists.notes import OsuHitList

m = OsuMap.read_file("osu/ZENITHALIZE_19.osu")
s = m.stack([OsuHitList])
#%%
s._stacked
#%%

from reamber.bms import BMSMap
m = BMSMap.read_file("bms/coldBreath.bme")
m.bpms.offset += 100
m.version = "Shifted"
m.write_file("test.bme")

#%%
from reamber.quaver import QuaMap
m = QuaMap.read_file("qua/CarryMeAway.qua")
m.bpms.offset += 100
m.version = "Shifted"
m.write_file("test.qua")

#%%
from reamber.sm import SMMapSet
ms = SMMapSet.read_file("sm/ICFITU.sm")
ms.stack()
ms.offset += 10000000
#%%
ms.write_file("out.sm")
#%%
from reamber.o2jam import O2JMapSet
ms = O2JMapSet.read_file("o2jam/o2ma120.ojn")
for m in ms:
    m.bpms.offset += 100
    m.version = "Shifted"
# O2J Writing is not supported yet. You can convert to other games
# and write it there.

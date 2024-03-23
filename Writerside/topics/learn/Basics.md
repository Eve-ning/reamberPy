# Basics of ReamberPy

## Brief Look

ReamberPy supports 5 different games, osu!, Quaver, BMS, O2Jam & StepMania

Through bundling all in 1 package, you benefit from:

- Similar Python syntax across different games
- In-built conversions between games.

Take a look at the following example that does the following on all games
<procedure>
<step>Load in a map</step>
<step>Shift all its BPMs by 100ms</step>
<step>Change its difficulty name</step>
<step>Save the map</step>
</procedure>

<tabs>
    <tab title="osu!mania">
        <code-block lang="python">
from reamber.osu.OsuMap import OsuMap
osu = OsuMap.read_file("my_map.osu")
osu.bpms.offset += 100
osu.version = "Shifted"
osu.write_file("my_new_map.osu")
        </code-block>
    </tab>
    <tab title="Quaver">
        <code-block lang="python">
from reamber.quaver.QuaMap import QuaMap
qua = QuaMap.read_file("my_map.qua")
qua.bpms.offset += 100
qua.difficulty_name = "Shifted"
qua.write_file("my_new_map.qua")
</code-block>
    </tab>
    <tab title="BMS">
<code-block lang="python">
from reamber.bms import BMSMap
m = BMSMap.read_file("my_map.bme")
m.bpms.offset += 100
m.version = "Shifted"
m.write_file("my_new_map.bme")
</code-block>
    </tab>
    <tab title="Stepmania">
<code-block lang="python">
from reamber.sm import SMMapSet
ms = SMMapSet.read_file("my_map.sm")
for m in ms:
    m.bpms.offset += 100
    m.version = "Shifted"
ms.write_file("my_new_map.sm")
</code-block>
    </tab>
    <tab title="O2Jam">
<code-block lang="python">
from reamber.o2jam import O2JMapSet
ms = O2JMapSet.read_file("my_map.ojn")
for m in ms:
    m.bpms.offset += 100
    m.version = "Shifted"
# O2J Writing is not supported yet. You can convert to other games 
# and write it there.
</code-block>
    </tab>
</tabs>

> Some games load in as `MapSet`s, you can treat them as `List[Map]`.
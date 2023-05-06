# Basics of ReamberPy

## Brief Look 

ReamberPy supports 5 different games, osu!, Quaver, BMS, O2Jam & StepMania

Through bundling all in 1 package, you benefit from:
- Similar Python syntax across different games
- In-built conversions between games.

Take a look at this example.

```py
from reamber.osu.OsuMap import OsuMap

osu = OsuMap.read_file("my_map.osu")
osu.bpms.offset += 100
osu.version = "Shifted"
osu.write_file("my_new_map.osu")
```

We load a map, and shifted its BPMs by 100ms, then wrote it back as ``my_new_map.osu``

See how we replicate it in Quaver.

```py
from reamber.quaver.QuaMap import QuaMap

qua = QuaMap.read_file("my_map.qua")
qua.bpms.offset += 100
qua.difficulty_name = "Shifted"
qua.write_file("my_new_map.qua")
```

The syntax is similar!

```py
from reamber.sm.SMMapSet import SMMapSet

sms = SMMapSet.read_file("my_map.sm")
for sm in sms:
    sm.bpms.offset += 100
sms.write_file("my_new_map.sm")
```

For StepMania, since each file contains multiple maps, we loop through each map in the ``MapSet``.

## Fundamental Tutorials

I have lined up a few tutorials below, I recommend taking a look at them!

```{toctree}
---
maxdepth: 1
---

Building Blocks of ReamberPy <BuildingBlocks>
Working with Maps <WorkingWithMaps>
Stacking <Stacking>
Map Conversions <Conversions>
Full LN Conversion <FullLN>
Pattern Finding <Pattern>
Play Field Image Generation <PlayField>
Play Field Imaging for Patterns <PlayFieldPattern>
osu! Hitsound Copying <osu/HitsoundCopy>
osu! Parse Replay <osu/ParseReplay>
Scroll Speed Analysis <ScrollSpeed>
```

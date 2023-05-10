# SV Normalize

Generates necessary SVs to normalize the scroll speed of the map.

Note that this only generates the SV List, it doesn't directly append to the map.

Merging of the normalizing SVs to the current SVs must be handled separately.

## Usage

You can automatically find the normalizing SVs

```python
from reamber.algorithms.generate import sv_normalize
from reamber.osu import OsuMap
from reamber.osu.lists import OsuSvList

osu_map = OsuMap.read_file(...)
svs = sv_normalize(osu_map)

# Append new svs to our map
osu_map.svs = osu_map.svs.append(svs)

# Remove any duplicates, if any
osu_map.svs = OsuSvList(osu_map.svs.df.drop_duplicates())
```

If it's not correctly normalizing, it's likely that the dominant bpm 
is incorrectly found. If so, override the dominant bpm.

```python
from reamber.algorithms.generate import sv_normalize
from reamber.osu import OsuMap

osu_map = OsuMap.read_file(...)
svs = sv_normalize(osu_map, override_bpm=200)
```
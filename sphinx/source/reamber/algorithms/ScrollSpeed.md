# Scroll Speed

This algorithm evaluates the effective, relative scroll speed to the most active bpm

The most active bpm is defined as the bpm which is present in the most of the map. This value can be manually overriden.

## Special Cases

This also considers maps with SVs. So it will properly multiply the scroll speed with it. 

## Return

This returns a `pd.Series` of name `speed`, with the `offset` as the index. 

## Usage

```py
from reamber.algorithms.analysis import scroll_speed
from reamber.osu import OsuMap
import pandas as pd


osu_map = OsuMap.read_file("path/to/map.osu")
s: pd.Series = scroll_speed(osu_map)
offset = s.index
```

# Dominant BPM

A utility function to find the most common BPM. Mostly used to evaluate the reference bpm used in osu!mania

This also considers the last map object when calculating the intervals.

## Usage

```python

from reamber.algorithms.utils import dominant_bpm
from reamber.osu import OsuMap

osu = OsuMap.read_file(...)
print(dominant_bpm(osu))
```

 
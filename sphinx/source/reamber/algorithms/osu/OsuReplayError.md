# Osu! Replay Error

You need 

Replays:
- Path to osu! replays or
- ``Replays``

Map:
- Path to osu! map
- ``OsuMap``

After initialization, to get the errors, call ``errors()``.


## Example

The following example extracts the hit errors of the first replay and plots in a histogram.

**Input**

```python
from reamber.algorithms.osu.OsuReplayError import OsuReplayError
rep = OsuReplayError(["path/to/rep1.osr", "path/to/rep2.osr"], "path/to/map.osu")
er = rep.errors()
```


# Osu!

We support the osu! file format except for the following:

- Storyboard Elements
- Standard, Catch, Taiko

This package supports most operations for osu! To better understand how to use this package here are some examples

## Examples

### Read and Write

```python
from reamber.osu.OsuMap import OsuMap

osu = OsuMap.read_file("file.osu")
osu.write_file("file_out.osu")
```

### Print all LN Lengths

```python
from reamber.osu.OsuMap import OsuMap

osu = OsuMap.read_file("file.osu")
print(osu.holds.length)
```

### Set all notes' volume to 0

```python
from reamber.osu.OsuMap import OsuMap

osu = OsuMap.read_file("file.osu")
osu.hits.volume = 0
osu.holds.volume = 0
```
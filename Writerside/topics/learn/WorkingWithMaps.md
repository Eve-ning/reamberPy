# Working with Maps

For this, I'll be doing examples with osu!, however, other game modes are
compatible.

## Reading a Map

```python
from reamber.osu import OsuMap

m = OsuMap.read_file("path/to/map.osu")
```

Now you have `m`, you can access objects related to it

```python
from reamber.osu import OsuMap

m = OsuMap.read_file("path/to/map.osu")
print(m.hits.offset)
```

```
1     189227.0
2     191210.0
3     193185.0
...
```


## Hits, Hold & BPM

All maps are guaranteed to have `hits`, `holds`, `bpms`.

```python
m.hits.offset
m.holds.length
m.bpms.bpm
```

## Mutating

### Inplace Operations

You can mutate with inplace assignment operators

```python
from reamber.osu import OsuMap

m = OsuMap.read_file("path/to/map.osu")
m.hits.column += 1
m.bpms.bpm /= 4
```

### Adding One Object

You may use `append` to add an object.
However, note that this is slow on a loop.

```python
from reamber.osu import OsuMap
from reamber.osu.OsuHit import OsuHit

m = OsuMap.read_file("path/to/map.osu")
m.hits = m.hits.append(OsuHit(1000, 1))
```

Because we build upon `pandas`, append is slow, see how to append multiple
objects below

### Adding Multiple Objects

Instead of appending a single `OsuHit`, consider appending a `OsuHitList`.

```python
from reamber.osu import OsuMap
from reamber.osu.lists.notes.OsuHitList import OsuHitList

m = OsuMap.read_file("path/to/map.osu")
m.hits = m.hits.append(
    OsuHitList.from_dict(
        {'offset': [1000, 2000, 3000], 'column': [1, 2, 3]}
    )
)
```

For longer lists, this will be significantly faster.

### Stacking

Stacking is a whole topic on its own, however, have a little preview.

```python
from reamber.osu import OsuMap

m = OsuMap.read_file("path/to/map.osu")
s = m.stack()
# Multiply all offsets in the map by 2
s.offset *= 2

# Add 100 ms to all LNs of > 100ms length
s.loc[(s.length > 100), 'offset'] += 100

# Move all notes 1 to the right if they are Column == 2 and beyond 1000ms
s.loc[(s.column == 2) & (s.offset > 1000), 'column'] += 1
```

## Writing a Map

> Note that not all games are supported for writing yet, such as O2Jam
{style="warning"}

Closing off, we write back the map

```python
from reamber.osu import OsuMap

m = OsuMap.read_file("path/to/map.osu")
...
m.write_file("path/to/new_map.osu")
```



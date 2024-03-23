# Getting Started

Install reamber via `pip`

`pip install reamber`

## Conventions

- **Note Object**: Means all playable objects, inclusive of Hit, Hold, Mine,
  Roll, etc.
- **Hit Object**: This means any note that is just a single tap.
- **BPM Point/Object**: These are aliases.
- **Map/Map Set**: A Map Set contains a list of Maps.
    - Some games have multiple maps in a single file, hence they will load as a
      `Mapset`.

## [Tutorials](Basics.md)

## Quick Examples

> ReamberPy is designed to be game-agnotic, so you can use the same code for
> different games. Just swap out the game name. 
> 
> E.g. `OsuMap` to `QuaMap`


### Load a Map

```python
from reamber.osu.OsuMap import OsuMap
m = OsuMap.read_file("path/to/file.osu")
```

### Load a Mapset

Games with multiple maps in a single file, will return a `MapSet`.
Here's how to grab maps from a set.

```python
from reamber.sm.SMMapSet import SMMapSet
sms = SMMapSet.read_file("path/to/file.sm")
sm = sms[0]
```

## Properties

All `Map`s are guaranteed to have 3 properties

- Hit Objects
- Hold Objects
- Bpm Objects

> Depending on the map type, there may be extra properties.
> E.g. StepMania maps have mines

### Example: Get the first 5 hit offsets in the file

```python
from reamber.osu.OsuMap import OsuMap
m = OsuMap.read_file("path/to/file.osu")

print(m.hits.offset[:5])
```

## Converting

### Example: Read an osu! file and export as a Quaver file

```python
from reamber.osu.OsuMap import OsuMap
from reamber.algorithms.convert.OsuToQua import OsuToQua
m = OsuMap.read_file("path/to/file.osu")
qua = OsuToQua.convert(m)
qua.write_file("out.qua")
```

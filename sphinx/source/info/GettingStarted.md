# Getting Started

**Installation**

If you haven't installed reamber you can just run

``pip install reamber``

in your terminal

## Requirements

If pip doesn't install extra dependencies for you, you also require these libraries.

- Python >=3.7
- numpy - For common mathematical operations and the numpy.Series
- pyyaml - To handle Quaver files easily
- pandas - To facilitate some algorithms and allow conversion to pandas.DataFrame
- matplotlib - To allow plotting on some algorithms (e.g. nps_plot)
- pillow - To enable drawing on some algorithms (e.g. PlayField)

## Conventions

- **Note Object**: This means all playable objects, inclusive of Hit, Hold, Mine, Roll, etc.
- **Hit Object**: This means any note that is just a single tap.
- **Bpm Point/Object**: These are aliases.
- **Map/Map Set**: A Map Set contains a list of Maps.
  - Some games have multiple maps in a single file, hence they will load as a Mapset.

## Examples

### Loading a Map

```py
from reamber.osu.OsuMap import OsuMap
m = OsuMap.read_file("path/to/file.osu")
```

### Loading a Mapset

Sometimes a game will put multiple maps in a single file, hence you get a mapset.
Here's how to grab maps from a set.

```py
from reamber.sm.SMMapSet import SMMapSet
sms = SMMapSet.read_file("path/to/file.sm")
sm = sms[0]
```

## Grabbing Properties

All maps are guaranteed to have 3 properties

- Hit Objects
- Hold Objects
- Bpm Objects

Depending on the map type, there may be extra properties.

E.g. StepMania maps have mines

### Example: Get the first 5 hit offsets in the file

```pycon
>>> from reamber.osu.OsuMap import OsuMap
>>> m = OsuMap.read_file("path/to/file.osu")
>>> print(m.hits.offset[:5])
[4113, 4113, 4142, 4200, 4631]
```

## Converting

### Example: Read an osu! file and export as a Quaver file

```pycon
>>> from reamber.osu.OsuMap import OsuMap
>>> from reamber.algorithms.convert.OsuToQua import OsuToQua
>>> m = OsuMap.read_file("path/to/file.osu")
>>> qua = OsuToQua.convert(m)
>>> qua.write_file("out.qua")
```
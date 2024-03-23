# osu! Hit Sound Copy

<tldr>
    <p>Copies over osu!mania hitsounds from another map.</p>
</tldr>

This also [combines default hitsounds if necessary](#packing)

## Example

```python
from reamber.osu.OsuMap import OsuMap
from reamber.algorithms.osu.hitsound_copy import hitsound_copy

m_from = OsuMap.read_file("hitsound.osu")
m_to = OsuMap.read_file("hitsoundable.osu")
m_out = hitsound_copy(m_from=m_from, m_to=m_to)
m_out.write_file("file_out.osu")
```

- If you have **excess** default hitsounds (Clap, Finish, Whistle), 
  the algorithm will drop them. You can find out which are dropped in the
  DEBUG logger.

- If you have **excess named** samples (e.g. "clap.wav", "sub.wav"), the
  algorithm will push it as an event sample. This can also be found with
  the DEBUG logger.

- This algorithm uses a packing method for hitsound copying. i.e. it will
  group as many hitsounds together as possible while maintaining their
  resulting sound.

## Packing

```
e.g. < (C)lap (F)inish (W)histle >

C F W  Vol |               | C F W  Vol
1 0 0  20  |               | 1 1 1  20
0 1 0  20  |               | 1 0 0  30
0 0 1  20  | == Copier ==> | 0 1 1  40
1 0 0  30  |               | CUSTOM 20
0 1 1  40  |               |
CUSTOM 20  |               |
```

### Packing Algorithm

1. Drop all non-hitsound notes
2. Group by offset and loop through them
3. For each offsetGroup, we group them by volume.
4. For each volumeGroup, we attempt to snap them into available notes in our
   target map. This process separates default hitsounds and samples
5. If there are no slots:
    1. The algorithm will drop any default hitsounds
    2. The algorithm will sample any named samples
6. Return the map


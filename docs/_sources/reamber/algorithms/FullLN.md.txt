# Full LN

## Usage 

To convert a map to a Full LN:

```py
from reamber.algorithms.generate import full_ln
from reamber.osu.OsuMap import OsuMap

osu = OsuMap.read_file("my_map.osu")
osu2 = full_ln(osu, gap=150, ln_as_hit_thres=100)
osu2.write_file("new_map.osu")
```

> This works with other map types. It doesn't work with `MapSet`s

## Params

- `gap`: Gap between an LN Tail and the next note.
- `ln_as_hit_thres`: Smallest LN length before it's converted to a hit.

For example:

- If the distance between 2 notes is 250ms
- The `gap` is 150ms
- There will be a 100ms LN rendered.


- If the distance between 2 notes is 249ms
- The `gap` is 150ms
- There won't be a 99ms LN rendered if `ln_as_hit_thres=100`. Instead, a `Hit` will be rendered.


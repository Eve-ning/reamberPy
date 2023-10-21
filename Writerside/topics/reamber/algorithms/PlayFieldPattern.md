# Play Field Imaging with Patterns

<tldr>
    <p>Visualizes Patterns discovered with 
       <code>Pattern</code> into <code>PlayField</code></p>
</tldr>

> You don't need to read the [Pattern Article](Pattern.md) to use this
> However you can read it to understand the API better.
> {style="note"}

## Pattern API

Using `PFDrawLines.from_combo` you can directly render lines in combinations.

It's **recommended** to use the recipe below and modify to your liking.
The implementation is complex but easily modifiable.

```python
from reamber.algorithms.pattern.Pattern import Pattern
from reamber.algorithms.pattern.combos import PtnCombo
from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import *
from reamber.osu.OsuMap import OsuMap

osu = OsuMap.read_file("path/to/map.osu")

ptn = Pattern.from_note_lists([osu.notes.hits, osu.notes.holds])
grp = ptn.group(h_window=None, v_window=50, avoid_jack=True)

keys = osu.stack().column.max() + 1

pf = (
        PlayField(m=osu, duration_per_px=5)
        + PFDrawLines.from_combo(keys=keys,
                                 **PFDrawLines.Colors.RED,
                                 combo=PtnCombo(grp).template_chord_stream(
                                     primary=3, secondary=2,
                                     keys=keys, and_lower=True)
                                 )
        + PFDrawLines.from_combo(keys=keys,
                                 **PFDrawLines.Colors.BLUE,
                                 combo=PtnCombo(grp).template_chord_stream(
                                     primary=2, secondary=1,
                                     keys=keys, and_lower=True)
                                 )
        + PFDrawLines.from_combo(keys=keys,
                                 **PFDrawLines.Colors.PURPLE,
                                 combo=PtnCombo(grp).template_jacks(
                                     minimum_length=2, keys=keys)
                                 )
)

pf.export_fold(maxHeight=1750, stageLineWidth=0).save("osu.png")
```

{collapsible="true" collapsed-title="PlayField Recipe"}

## Understanding the Recipe

We firstly group by `hits` and `holds` of the read osu map with a **Vertical
Window** of 50.

```python
ptn.group(h_window=None, v_window=50, avoid_jack=True)
```

Using that group, we construct lines for **Chordstreams**. The first
chordstream template looks for all pairs that are
`[3, 2], [2, 3], [2, 2], [2, 1], [1, 2], [1, 1]`

```python
PFDrawLines.from_combo(
    ...,
    combo=PtnCombo(grp).template_chord_stream(primary=3,
                                              secondary=2,
                                              keys=keys,
                                              andLower=True))
```

- The second one looks for all pairs that are `[2, 1], [1, 2], [1, 1]`

```python
PFDrawLines.from_combo(
    ...,
    combo=PtnCombo(grp).template_chord_stream(primary=2,
                                              secondary=1,
                                              keys=keys,
                                              andLower=True))
```

The third locates **jacks** that are at least a minimum length of 2 (i.e. all
jacks)

```python
PFDrawLines.from_combo(..., combo=PtnCombo(grp).template_jacks(minimumLength=2,
                                                               keys=keys))
```

The last line folds the image so that it's more squarey then saves as `osu.png`

```python
pf.export_fold(maxHeight=1750, stageLineWidth=0).save("osu.png")
```


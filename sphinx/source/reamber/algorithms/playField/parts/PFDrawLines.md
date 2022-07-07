# Play Field Draw Lines

## Pattern API

**You need knowledge about the Pattern package.**

I added 2 templates to easily generate the filters, however you can create filters of your own. Instructions are in
the ``combinations`` **docstring**.

**Input**

```py
from reamber.osu.OsuMap import OsuMap
from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import *
from reamber.algorithms.pattern.Pattern import Pattern
from reamber.algorithms.pattern.combos import PtnCombo

osu = OsuMap.read_file(OSU_BOOGIE)

ptn = Pattern.from_note_lists([osu.notes.hits, osu.notes.holds])
grp = ptn.group(h_window=None, v_window=50, avoid_jack=True)

keys = osu.stack().column.max() + 1

pf = (
    PlayField(m=osu, duration_per_px=5)
    + PFDrawLines.from_combo(
    keys=keys, **PFDrawLines.Colors.RED,
    combo=PtnCombo(grp).template_chord_stream(primary=3, secondary=2, keys=keys, and_lower=True)
) + PFDrawLines.from_combo(
    keys=keys, **PFDrawLines.Colors.BLUE,
    combo=PtnCombo(grp).template_chord_stream(primary=2, secondary=1, keys=keys, and_lower=True)
) + PFDrawLines.from_combo(keys=keys, **PFDrawLines.Colors.PURPLE,
                           combo=PtnCombo(grp).template_jacks(minimum_length=2, keys=keys))
)
pf.export_fold(maxHeight=1750, stageLineWidth=0).save("osu.png")
```

- We firstly group by ``hits`` and ``holds`` of the read osu map with a **Vertical Window** of 50.
- Using that group, we construct lines for **Chordstreams**.
- The first chordstream template looks for all pairs that are ``[3, 2], [2, 3], [2, 2], [2, 1], [1, 2], [1, 1]``

```
PFDrawLines.from_combo(...,
    combo=PtnCombo(grp).template_chord_stream(primary=3, secondary=2, keys=keys, andLower=True))
```

- The second one looks for all pairs that are ``[2, 1], [1, 2], [1, 1]``

```
PFDrawLines.from_combo(...,
    combo=PtnCombo(grp).template_chord_stream(primary=2, secondary=1, keys=keys, andLower=True))
```

- The third locates all jacks that are at least a minimum length of 2 (all jacks in other words)

```
PFDrawLines.from_combo(..., combo=PtnCombo(grp).template_jacks(minimumLength=2, keys=keys))
```

- Note that the chordstream template will not look for jacks unless specifically stated.
- The last line folds the image so that it's more squary then saves it as ``osu.png``

```
pf.export_fold(maxHeight=1750, stageLineWidth=0).save("osu.png")
```

## Template Chord Stream

The underlying algorithm uses this lower-level interface. This part requires knowledge about how ``PtnFilter``
creates its filter.

```py
from reamber.algorithms.pattern.filters import PtnFilterType, PtnFilterCombo
from reamber.base.Hold import HoldTail
from reamber.algorithms.pattern.filters import PtnFilterChord
from reamber.algorithms.pattern.Pattern import Pattern
from reamber.algorithms.pattern.combos import PtnCombo

primary = 3
secondary = 4
keys = 7
and_lower = False
include_jack = False
combo = PtnCombo.combinations(
    ...,
    chord_filter=PtnFilterChord.create(
        [[primary, secondary]], keys=keys,
        options=PtnFilterChord.Option.ANY_ORDER | PtnFilterChord.Option.AND_LOWER if and_lower else 0,
        exclude=False).filter,
    combo_filter=PtnFilterCombo.create(
        [[0, 0]], keys=keys,
        options=PtnFilterCombo.Option.REPEAT,
        exclude=True).filter if not include_jack else None,
    type_filter=PtnFilterType.create(
        [[HoldTail, object]], keys=keys,
        options=PtnFilterType.Option.ANY_ORDER,
        exclude=True).filter)
```

- we define the detection to be ``size=2``, so it only looks for pairs.

- The ``chordFilter`` will filter **in** anything that matches the ``primary`` and ``secondary`` parameters and below. (
  this is made possible by the ``PtnFilterChord.Method.AND_LOWER`` argument.)

- The ``comboFilter`` excludes any jacks. ``[0, 0], [1, 1], ...`` is rejected. (Using the ``invertFilter=True``
  argument.)

- the ``typeFilter`` excludes the ``HoldTail`` being included in any pair. (Using the ``invertFilter=True`` argument.)

## Template Jacks

```py
from reamber.algorithms.pattern.filters import PtnFilterType, PtnFilterCombo
from reamber.base.Hold import HoldTail
from reamber.algorithms.pattern.combos import PtnCombo

keys = 4
minimum_length = 2
combo = PtnCombo.combinations(
    ...,
    combo_filter=PtnFilterCombo.create(
        [[0] * minimum_length], keys=keys,
        options=PtnFilterCombo.Option.REPEAT,
        exclude=False).filter,
    type_filter=PtnFilterType.create(
        [[HoldTail, object]], keys=keys,
        options=PtnFilterType.Option.ANY_ORDER,
        exclude=True).filter
)
```

The ``comboFilter`` include any jacks. ``[0, 0], [1, 1], ...`` is accepted.

the ``typeFilter`` excludes the ``HoldTail`` being included in any pair. (Using the ``exclude=True`` argument.)




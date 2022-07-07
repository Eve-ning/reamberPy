# Pattern Combinations

[After creating groups](../Pattern), you can find relationships between them with this.

| Input                          |
|--------------------------------|
| [Grouping] (../Pattern)        |
| [Combinations] (PtnCombo)      |
| [Filtering] (PtnFilter)        |
| ------------------------------ |
| Output                         |

Pattern Combinations loops groups yielding their Cartesian Product.

```
Cartesian Product of [0, 1, 2] [A, B, C]
    A  B  C
  +---------
0 | A0 B0 C0
1 | A1 B1 C1
2 | A2 B2 C2
= A0 B0 C0 A1 B1 C1 A2 B2 C2
```

```python
from reamber.algorithms.pattern.combos import PtnCombo
from reamber.algorithms.pattern import Pattern

g = Pattern.from_note_lists(...).group(...)

combos = PtnCombo(g).combinations(
    size=2, flatten=False, make_size2=False
)
```

Take for example:

```
If Group B comes after A,
Group A = [0, 1]
Group B = [3, 4]

Combinations = [0, 3] [0, 4] [1, 3] [1, 4]
```

Size
====

Size defines number of groups combined together.

**Size 2**

```
With 3 Groups, we yield 2 Cartesian products
GRP 1  GRP 2  GRP 3
[1, 2] [0, 3] [0, 2]

GRP 1 x GRP 2 = [1, 0], [1, 3], [2, 0], [2, 3]
GRP 2 x GRP 3 = [0, 0], [0, 2], [3, 0], [3, 2]
```

**Size 3**

```
GRP 1 GRP 2 GRP 3
[1, 2] [0, 3] [0, 2]

GRP 1 x GRP 2 x GRP 3 = [1, 0, 0], [1, 0, 2], [1, 3, 0], ..., [2, 3, 2]
```

## Flatten & Make Size 2

By default, the returned structure is

```
If we are combining
Group A = [0, 1]
Group B = [3, 4]
size = 2

Combination: [[[0, 3], [0, 4]], [[1, 3], [1, 4]]]
Combination with Flatten: [[0, 3], [0, 4], [1, 3], [1, 4]]
```

If ``size>2``

```
If we are combining
Group A = [0, 1]
Group B = [3, 4]
Group C = [2]
size = 3

Combination: [[[0, 3, 2], [0, 4, 2]], [[1, 3, 2], [1, 4, 2]]]
Combination with Make Size 2: [0, 3], [3, 2], ..., [1, 4], [4, 2]
[0, 3, 2] -> [0, 3], [3, 2]
[0, 4, 2] -> [0, 4], [4, 2]
[1, 3, 2] -> [1, 3], [3, 2]
[1, 4, 2] -> [1, 4], [4, 2]
```

## Filtering

You may not need all combinations, thus you can filter unwanted patterns/combinations.

There are **3 Filters**:

- Chord Filtering
- Combo Filtering
- Type Filtering

Take a look at [Filtering](PtnFilter) to utilize ``chord_filter, combo_filter, type_filter``.

## Template Combinations

``PtnCombo`` provides common filter templates.

This uses [filtering](PtnFilter) arg to remove unwanted combinations.

Chord Stream
============

```py
from reamber.algorithms.pattern.combos import PtnCombo
from reamber.algorithms.pattern import Pattern
from reamber.algorithms.pattern.filters import PtnFilterCombo, PtnFilterType, PtnFilterChord
from reamber.base.Hold import HoldTail

minimum_length = 2
keys = 4
g = Pattern.from_note_lists(...).group(...)
primary = 3
secondary = 4
and_lower = True
include_jack = False
combo = PtnCombo(g).combinations(

    chord_filter=PtnFilterChord.create(
        [[primary, secondary]],
        options=PtnFilterChord.Option.ANY_ORDER |
                PtnFilterChord.Option.AND_LOWER if and_lower else 0,
        exclude=False).filter,

    combo_filter=PtnFilterCombo.create(
        [[0, 0]],
        options=PtnFilterCombo.Option.REPEAT,
        exclude=True).filter if not include_jack else None,

    type_filter=PtnFilterType.create(
        [[HoldTail, object]],
        options=PtnFilterType.Option.ANY_ORDER,
        exclude=True).filter)
```

**In Summary:**

1. Looks for any chord size pair below the ``primary`` and ``secondary`` value.
2. Excludes jacks
3. Excludes ``HoldTail`` and any other ``object`` combinations.

The above rules can be adjusted by either creating another template or adjusting provided parameters.

## Jack

```python
from reamber.algorithms.pattern.combos import PtnCombo
from reamber.algorithms.pattern import Pattern
from reamber.algorithms.pattern.filters import PtnFilterCombo, PtnFilterType
from reamber.base.Hold import HoldTail

minimum_length = 2
keys = 4
g = Pattern.from_note_lists(...).group(...)

combo = PtnCombo(g).combinations(
    ...,
    combo_filter=PtnFilterCombo.create(
        [[0] * minimum_length],
        keys=keys,
        options=PtnFilterCombo.Option.REPEAT,
        exclude=False).filter,
    type_filter=PtnFilterType.create(
        [[HoldTail] + [object] * (minimum_length - 1)],
        keys=keys,
        options=PtnFilterType.Option.ANY_ORDER,
        exclude=True).filter
)
```

**In Summary:**

1. Looks for any ``[0, 0, ...], [1, 1, ...], [2, 2, ...], ...`` dependent on ``minimum_length``
2. Excludes ``HoldTail`` and any other ``object`` combinations.



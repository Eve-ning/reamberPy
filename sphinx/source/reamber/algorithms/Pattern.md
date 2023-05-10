# Patterns

The pattern package aids finding patterns within a map.

## Theory

To find patterns, we must:

- Cluster Notes. [**Grouping**](grouping)
- Find association between clusters. [**Combinations**](combinations)
- Remove unwanted associations. [**Filtering**](filters)

### Theory in Example

```
       +---------------+
       | C |   | D |   |
       | A | B |   |   |
       +---------------+
Column   0   1   2   3
```

Let's say we want to find patterns like ``A -> C``. i.e. Jacks

Working **backwards**:

- To find ``A -> C``, we **filtered** it from the associations
    - ``A -> C``, ``A -> D``, ``B -> C``, ``B -> D``
- To find associations, we find **combinations** in chords ``[A B] x [C D]``
- To find chords, we group notes ``A <-> B, C <-> D``

Working **forwards**:

- Firstly, **group** ``A <-> B`` and ``C <-> D`` because they are on the same offset
- Then, find all **combinations** of ``[A B] x [C D]``
    - ``A -> C``, ``A -> D``, ``B -> C``, ``B -> D``
- Finally, **filter** out combinations that aren't of the same column
    - ``A -> C``

## Input

To start, we initialize ``Pattern`` in 2 ways:

```py
from reamber.algorithms.pattern.Pattern import Pattern
from reamber.osu.OsuHit import OsuHit

# Method 1
p = Pattern([0, 1, 2, 3], [1000, 2000, 3000, 4000], [OsuHit, OsuHit, OsuHit, OsuHit])

from reamber.osu.OsuMap import OsuMap

# Method 2
m = OsuMap.read_file("...")
p = Pattern.from_note_lists([m.hits, m.holds], include_tails=True)
```

You may choose to exclude tails in patterns with `include_tails=False`

(grouping)=

## Grouping

> ``group`` Groups the package horizontally and vertically, returns a list of groups.

- **Horizontally**: Grouping across columns of the same offset
- **Vertically**: Grouping across offsets of the same column

For example, since graces can be played as chords, we can **vertically**
group them with a threshold.

```py
from reamber.algorithms.pattern.Pattern import Pattern
from reamber.osu.OsuMap import OsuMap

m = OsuMap.read_file("...")
p = Pattern.from_note_lists([m.hits, m.holds], include_tails=True)
g = p.group(v_window=50, h_window=None, avoid_jack=True)
```

### Vertical & Horizontal Window `v_window` `h_window`

Windows define how far _forward_ / _sideways_ a note should look to group.

Consider the following marked X

```
[20ms] | _ O _ _ |^
[10ms] | _ _ _ _ || Vertical
[0ms]  | X _ O _ |v
         <--->
         Horizontal
```

If ``h_window=2, v_window=20``. All notes will be grouped as one, anything smaller will split them.

The default, ``h_window=None`` will yield all columns.

### Avoid Jack

When grouping, you want to avoid grouping jacks together

```
[20ms] | O _ _ _ |^
[10ms] | _ _ _ _ || Vertical
[0ms]  | X _ _ _ |v
```

``avoid_jack=True`` prevents that, forcing the next note to another group.

### Large Horizontal Window with Jack Avoidance

A large `h_window` and `avoid_jack`, **can cause overlapping groups.**

Example

```
Unlabelled       Labelled
===========      ===========
| O O _ O |      | 6 7 _ 8 |
| _ _ _ _ |      | _ _ _ _ | ^
| O _ _ O |  ==  | 4 _ _ 5 | | Vertical
| _ _ O _ |      | _ _ 3 _ | | Window
| _ O O _ |      | _ 1 2 _ | v
===========      ===========

! Notes are labelled from 1 to 8

Group 1         Group 2
Labelled        Labelled
===========     ===========
| _ _ _ _ |     | 6 7 _ 8 | ^
| _ _ _ _ | ^   | _ _ _ _ | |
| 4 _ _ 5 | |   | _ _ _ _ | |
| _ _ _ _ | |   | _ _ 3 _ | v
| _ 1 2 _ | v   | _ _ _ _ |
===========     ===========
```

Notice that ``3`` was rejected from **Group 1** because ``avoid_jack=True``. Thus moved to **Group 2**

### Examples

Let's say we want to group with the parameters

``vwindow = 0, hwindow = None``

```
[4s]  _5__           _5__           _5__           _5__           _X__
[3s]  ___4  GROUP 1  ___4  GROUP 2  ___4  GROUP 3  ___X  GROUP 4  ___X
[2s]  _2_3  ------>  _2_3  ------>  _X_X  ------>  _X_X  ------>  _X_X
[1s]  ____  [1]      ____  [2,3]    ____  [4]      ____  [5]      ____
[0s]  1___           X___           X___           X___           X___

Output: [1][2,3][4][5]
```

``vwindow = 1000, hwindow = None``

```
[4s]  _5__           _5__           _5__           _X__
[3s]  ___4  GROUP 1  ___4  GROUP 2  ___X  GROUP 3  ___X
[2s]  _2_3  ------>  _2_3  ------>  _X_X  ------>  _X_X
[1s]  ____  [1]      ____  [2,3,4]  ____  [5]      ____
[0s]  1___           X___           X___           X___

Output: [1][2,3,4][5]
```

2, 3 and 4 are together as 4 is within the ``vwindow`` of 2;

``vwindow = 1000, hwindow = 1``

```
[4s]  _5__           _5__          _5__           _5__           _X__
[3s]  ___4  GROUP 1  ___4  GROUP 2 ___4  GROUP 3  ___X  GROUP 4  ___X
[2s]  _2_3  ------>  _2_3  ------> _X_3  ------>  _X_X  ------>  _X_X
[1s]  ____  [1]      ____  [2]     ____  [3,4]    ____  [5]      ____
[0s]  1___           X___          X___           X___           X___

Output: [1][2][3,4][5]
```

2 and 3 aren't together as they are > 1 column apart, due to ``hwindow``

(combinations)=

## Combinations

> [After creating groups](grouping), ``combinations`` finds relationships between
> them with their Cartesian Product.

```
Cartesian Product of [0, 1, 2] [A, B, C]
    A  B  C
  +---------
0 | A0 B0 C0
1 | A1 B1 C1
2 | A2 B2 C2
= A0 B0 C0 A1 B1 C1 A2 B2 C2
```

For example:

```
If Group B comes after A,
Group A = [0, 1]
Group B = [3, 4]

Combinations = [0, 3] [0, 4] [1, 3] [1, 4]
```

```py
from reamber.algorithms.pattern.Pattern import Pattern
from reamber.algorithms.pattern.combos.PtnCombo import PtnCombo
from reamber.osu.OsuMap import OsuMap

m = OsuMap.read_file("...")
p = Pattern.from_note_lists([m.hits, m.holds], include_tails=True)
g = p.group(v_window=50, h_window=None, avoid_jack=True)
c = PtnCombo(g).combinations(
    size=2, make_size2=False,
    # We'll talk about Filters later.
    chord_filter=None, combo_filter=None, type_filter=None
)
```

### Size `size`

Size defines number of groups to combine.

With ``size=2``

```
With 3 Groups, we yield 2 Cartesian products
GRP 1  GRP 2  GRP 3
[1, 2] [0, 3] [0, 2]

GRP 1 x GRP 2 = [1, 0], [1, 3], [2, 0], [2, 3]
GRP 2 x GRP 3 = [0, 0], [0, 2], [3, 0], [3, 2]
```

With ``size=3``

```
GRP 1 GRP 2 GRP 3
[1, 2] [0, 3] [0, 2]

GRP 1 x GRP 2 x GRP 3 = [1, 0, 0], [1, 0, 2], [1, 3, 0], ..., [2, 3, 2]
```

### Flatten & Make Size 2 `flatten` `make_size2`

By default, the returned structure is ``List[List[List[int]]]``.

You may `flatten` it.

```
If we are combining
Group A = [0, 1]
Group B = [3, 4]
size = 2

Combination: [[[0, 3], [0, 4]], [[1, 3], [1, 4]]]
Combination with Flatten: [[0, 3], [0, 4], [1, 3], [1, 4]]
```

``make_size2`` splits ``size>3`` into 2s

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

(filters)=

## Filters

> After [combining groups](combinations), filter out unwanted combinations.

For each ``..._filter``, we expect a ``Callable / lambda``.

You can create custom filters, however, I recommend our lambdas for this.

```py
from reamber.algorithms.pattern.filters import PtnFilterChord,

PtnFilterType, PtnFilterCombo
from reamber.algorithms.pattern.Pattern import Pattern
from reamber.algorithms.pattern.combos.PtnCombo import PtnCombo
from reamber.osu.OsuMap import OsuMap

m = OsuMap.read_file("...")
p = Pattern.from_note_lists([m.hits, m.holds], include_tails=True)
g = p.group(v_window=50, h_window=None, avoid_jack=True)
c = PtnCombo(g).combinations(
    size=2, make_size2=False,
    # We'll talk about Filters later.
    chord_filter=PtnFilterChord.create(...).filter,
    combo_filter=PtnFilterCombo.create(...).filter,
    type_filter=PtnFilterType.create(...).filter
)
```

**By Default, all filters are INCLUDE**.

### Filter Chord

```py
from reamber.algorithms.pattern.filters import PtnFilterChord

chord_filter = PtnFilterChord.create(
    [[2, 2]], 4,
    options=PtnFilterChord.Option.AND_LOWER,
    exclude=False
).filter,
```

- Include only chord combinations of `[2, 2]` and lower.
    - `[1, 1]`, `[1, 2]`, `[2, 1]`

Chord filtering simply filters using group size

```
===========
| O O _ O | Group C
| _ _ _ _ |
| O _ _ O | Group B
| _ _ _ _ |
| _ O O _ | Group A
===========

Combination Size = 2

Group   A       -> B       -> C
Chord   [1, 2]  -> [0, 3]  -> [0, 1, 3]
Size    2       -> 2       -> 3
        ^----------^
           [2, 2]  ^----------^ Combination Size = 2
             |        [2, 3]
             |          |
             v          v
        +---------------------+ [2, 2] not in [[3, 2], [2, 3]]
Filter  |  [[2, 3], [3, 2]]   |
        +---------------------+ [2, 3] in [[3, 2], [2, 3]]
             |          |
             x          |
                        V
                      Output
```

Filter Chord controls which group combinations pass through.

#### Options `options`

- ``ANY_ORDER``
    - Make Additional Filters of any order

      ```[A, B, C] -> Any Order -> [A, B, C], [A, C, B], ..., [C, B, A]```
- ``AND_LOWER``
    - Make Additional Filters of any lower combination (Down to 1)

      ```[2, 3] -> And Lower -> [2, 3], [2, 2], ... , [1, 2], [1, 1]```

- ``AND_HIGHER``
    - Make Additional Filters of any higher combination (Up to Keys)

      ```[1, 2] -> And Higher -> [1, 2], [2, 2], ... , [3, 4], [4, 4]```

### Filter Combo

```py
from reamber.algorithms.pattern.filters import PtnFilterCombo

combo_filter = PtnFilterCombo.create(
    [[0, 1, 2, 3]], 4,
    options=PtnFilterCombo.Option.HMIRROR,
    exclude=False
).filter,
```

- Includes any occurence of `[0, 1, 2, 3]` and its horizontal mirror
    - Its horizontal mirror is: `[3, 2, 1, 0]`

Filters in/out specific combinations

```
===========
| O _ _ O | Group B
| _ _ _ _ |
| _ O O _ | Group A
===========

Combination Size = 2

Group     A       -> B
Chord     [1, 2]  -> [0, 3]
Cartesian [1, 0], [1, 3], [2, 0], [2, 3] Combination Size = 2
            |       |       |       |
            v       v       v       v
        +-------------------------------+
Filter  |       [[1, 3], [2, 3]]        |
        +-------------------------------+
            |       |       |       |
            x       |       x       |
                    v               v
                 Output          Output
```

#### Options `options`

- ``REPEAT``
    - Repeats the filter that are within bounds
      ```
      For example, a [1, 2] filter
      
      ===========
      | _ _ O _ |
      | _ O _ _ | -> Repeat ->
      ===========
      
      =========== =========== ===========
      | _ O _ _ | | _ _ O _ | | _ _ _ O |
      | O _ _ _ | | _ O _ _ | | _ _ O _ |
      =========== =========== ===========
      [0, 1]      [1, 2]      [2, 3]
      
      [1, 2] -> Repeat -> [0, 1], [1, 2], [2, 3]
      ```
- ``HMIRROR``
    - Mirrors the filter Horizontally
      ```
      For example, a [1, 3] filter
                                    Mirror
                                      |
      ===========                =====|=====
      | _ _ _ O |                | _ _|_ O |
      | _ _ _ _ |                | _ _|_ _ |
      | _ O _ _ | -> H Mirror -> | _ O|_ _ |
      ===========                =====|=====
                                      |
                                    Mirror
      =========== ===========
      | _ _ _ O | | O _ _ _ |
      | _ _ _ _ | | _ _ _ _ |
      | _ O _ _ | | _ _ O _ |
      =========== ===========
      [1, 3]      [2, 0]
      
      [1, 3] -> H Mirror -> [1, 3], [2, 0]
      ```
- ``VMIRROR``
    - Mirrors the filter Vertically
      ```
      For example, a [1, 3] filter
      
      ===========                ===========
      | _ _ _ O |                | _ _ _ O |
      | _ _ _ _ |       Mirror --------------- Mirror
      | _ O _ _ | -> V Mirror -> | _ O _ _ |
      ===========                ===========
      
      =========== ===========
      | _ _ _ O | | _ O _ _ |
      | _ _ _ _ | | _ _ _ _ |
      | _ O _ _ | | _ _ _ O |
      =========== ===========
      [1, 3]      [3, 1]
      
      [1, 3] -> V Mirror -> [1, 3], [3, 1]
      ```

### Filter Type

```py
from reamber.algorithms.pattern.filters import PtnFilterType
from reamber.osu.OsuHold import OsuHold
from reamber.osu.OsuHit import OsuHit

combo_filter = PtnFilterType.create(
    [[OsuHit, OsuHit, OsuHold]], 4,
    options=PtnFilterType.Option.ANY_ORDER,
    exclude=False
).filter,
```

- Includes any occurence of `[OsuHit, OsuHit, OsuHold]` and any order
    - Other orders: `[OsuHit, OsuHold, OsuHit]`, `[OsuHold, OsuHit, OsuHit]`

Filters i/o specific type combinations

For example, if we want to match only LN Heads/Hits, excluding LN Tails.

```
===========
| H | _ H | Group B
| _ | _ _ |
| _ L H _ | Group A
===========

L: LN Head
H: Hit

Combination Size = 2

Group     A       -> B
Chord     [L, H]  -> [H, H]
Cartesian [L, H], [L, H], [H, H], [H, H] Combination Size = 2
            |       |       |       |
            v       v       v       v
        +-------------------------------+
Filter  |           [[H, H]]            |
        +-------------------------------+
            |       |       |       |
            x       x       |       |
                            v       v
                          Output  Output
```

#### Options `options`

- ``ANY_ORDER``
    - Make Additional Filters of any order

      ```[A, B, C] -> Any Order -> [A, B, C], [A, C, B], ..., [C, B, A]```

- ``VMIRROR``
    - Mirrors the filter

      ```[A, B] -> Mirror -> [A, B], [B, A]```

## Custom Filters

You may customize your own filters as long they fit the signature.

```
combinations(
    ...,
    chord_filter: Callable[[np.ndarray], bool] = None,
    combo_filter: Callable[[np.ndarray], np.ndarray[bool]] = None,
    type_filter:  Callable[[np.ndarray], np.ndarray[bool]] = None
)
```

All of them are callables. They will accept a certain data structure and the ``Callable`` must return the boolean filter
verdict.

### Chord Filter

Take in an ``np.ndarray[int]`` of chord sizes, and it should return a ``bool`` verdict

Example I/O

```
Input:  np.ndarray([1, 3])
Output: False
```

Example Implementation

```py
def chord_filter(ar: np.ndarray):
    return ar[0] > 1


combos = combinations(..., chord_filter=chord_filter)
```

### Combo Filter

Take in an ``np.ndarray[int]`` of combos, and it should return a ``np.ndarray[bool]`` verdict

Example I/O

```
Input:  np.ndarray([[1, 2], [2, 3], [3, 4]])
Output: np.ndarray([True, True, False])
```

Example Implementation

```python
def combo_filter(ar: np.ndarray):
    return ar[:, 0] < 3


combos = combinations(..., combo_filter=combo_filter)
```

### Type Filter

Take in an ``np.ndarray[type]`` of combos, and it should return a ``np.ndarray[bool]`` verdict

Example I/O

```
Input:  np.ndarray([[Hit, HoldTail], [Hit, Hit], [Hold, HoldTail]])
Output: np.ndarray([True, False, True])
```

Example Implementation

```python
def type_filter(ar: np.ndarray):
    return [isssubclass(t, HoldTail) for t in ar[:, 1]]


combos = combinations(..., type_filter=type_filter)
```

For all end of Holds, they are classes of ``HoldTail``, ``HoldTail`` is never subclassed.



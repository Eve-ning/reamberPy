# Pattern Filters

| Input                          |
|--------------------------------|
| [Grouping] (../Pattern)        |
| [Combinations] (PtnCombo)      |
| [Filtering] (PtnFilter)        |
| ------------------------------ |
| Output                         |

After [combining groups](PtnCombo), we can filter out unwanted combinations.

## Using Filters

Here's the function signature of ``combinations``.

```py
import numpy as np
from typing import Callable


def combinations(
    chord_filter: Callable[[np.ndarray], bool] = None,
    combo_filter: Callable[[np.ndarray], np.ndarray[bool]] = None,
    type_filter: Callable[[np.ndarray], np.ndarray[bool]] = None
) -> np.ndarray:
    ...
```

For each ``..._filter``, we expect a ``Callable / lambda``.

You may create custom filters, however, I recommend our lambdas for this.

```py
from reamber.algorithms.pattern.filters import PtnFilterChord, PtnFilterType, PtnFilterCombo

g = ...
g.combinations(
    ...,
    chord_filter=PtnFilterChord.create(...).filter,
    combo_filter=PtnFilterCombo.create(...).filter,
    type_filter=PtnFilterType.create(...).filter
)
```

**By Default, all filters are INCLUDE**.

## Filter Chord

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

Filter controls which group combinations pass through.

```python
from reamber.algorithms.pattern.filters import PtnFilterChord


def create(chord_sizes: List[List[int]], keys: int,
           options: PtnFilterChord.Option | int = 0,
           exclude: bool = False):

```

## Options

Options simplify chord filters creation.

The options provided are

- ``ANY_ORDER``
- ``AND_LOWER``
- ``AND_HIGHER``

### Any Order

Make Additional Filters of any order

```[A, B, C] -> Any Order -> [A, B, C], [A, C, B], ..., [C, B, A]```

### And Lower

Make Additional Filters of any lower combination (Down to 1)

```[2, 3] -> And Lower -> [2, 3], [2, 2], ... , [1, 2], [1, 1]```

### And Higher

Make Additional Filters of any higher combination (Up to Keys)

```[1, 2] -> And Higher -> [1, 2], [2, 2], ... , [3, 4], [4, 4]```

## Filter Combo

Combo-filtering filters using specific combinations

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

```python
from reamber.algorithms.pattern.filters import PtnFilterCombo

def create(combos: List[List[int]],
           keys: int,
           options: Option | int = 0,
           exclude: bool = False) -> PtnFilterCombo:
```

## Options

Options simplify combo filters creation.

The methods provided are

- ``REPEAT``
- ``HMIRROR``
- ``VMIRROR``

### Repeat

Repeats the filter that are within bounds
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
### Horizontal Mirror

Mirrors the filter Horizontally
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

### Vertical Mirror

Mirrors the filter Vertically
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

## Filter Type

Type filtering filters on the combinations
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
```python
from reamber.algorithms.pattern.filters import PtnFilterType

def create(types: List[List[type]],
           keys: int,
           options: PtnFilterType.Option or int = 0,
           exclude: bool = False) -> PtnFilterType:
    ...
```
## Options

Options simplify combo filters creation.

The methods provided are

- ``ANY_ORDER``
- ``VMIRROR``

### Any Order

Make Additional Filters of any order

```[A, B, C] -> Any Order -> [A, B, C], [A, C, B], ..., [C, B, A]```

### Mirror

Mirrors the filter

```[A, B] -> Mirror -> [A, B], [B, A]```

# Custom Filters

You may customize your own filters as long they fit the signature.

Here's the signature again

```py
combinations(...
    chord_filter: Callable[[np.ndarray], bool] = None,
    combo_filter: Callable[[np.ndarray], np.ndarray[bool]] = None,
    type_filter: Callable[[np.ndarray], np.ndarray[bool]] = None
    )
```
All of them are callables. They will accept a certain data and the ``Callable`` must return the boolean filter verdict.

## Chord Filter

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
## Combo Filter

Take in an ``np.ndarray[int]`` of combos, and it should return a ``np.ndarray[bool]`` verdict

Example I/O

```
Input:  np.ndarray([[1, 2], [2, 3], [3, 4]])
Output: np.ndarray([True, True, False])
```

Example Implementation

```python
def combo_filter(ar: np.ndarray):
    return ar[:,0] < 3

combos = combinations(..., combo_filter=combo_filter)
```
## Type Filter

Take in an ``np.ndarray[type]`` of combos, and it should return a ``np.ndarray[bool]`` verdict

Example I/O

```
Input:  np.ndarray([[Hit, HoldTail], [Hit, Hit], [Hold, HoldTail]])
Output: np.ndarray([True, False, True])
```

Example Implementation

```python
def type_filter(ar: np.ndarray):
    return [isssubclass(t, HoldTail) for t in ar[:,1]]

combos = combinations(..., type_filter=type_filter)
```
For all end of Holds, they are classes of ``HoldTail``, ``HoldTail`` is never subclassed.



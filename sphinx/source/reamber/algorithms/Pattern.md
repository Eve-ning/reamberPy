# Pattern Detection

This is to find occurrence of specific patterns.

| Input                            |
|----------------------------------|
| [Grouping](Pattern)              |
| [Combinations](pattern/PtnCombo) |
| [Filtering](pattern/PtnFilter)   |
| Output                           |

## Input

2 Ways to initialize, either by providing the ``Lists`` or ``List[NoteList]``.

```py
Pattern(cols: List[int], offsets: List[float], types: List[Type])
Pattern.from_note_lists(note_lists: List[NoteList])
```

It's recommended to use the 2nd method as it's easier. See the following example:

```py
Pattern.from_note_list([m.hits, m.holds])
```
## Grouping

Now, we group notes together as chords.
However, some graces can be played as chords, thus we group with some buffer.

``group`` Groups the package horizontally and vertically, returns a list of groups.

```py
Pattern.from_note_list(...).group(
    v_window: float = 50.0,
    h_window: None or int = None,
    avoid_jack=True,
    avoid_regroup=True
    )
```

### Vertical & Horizontal Window

These windows define how far forward or to the side a note should look for to group.

Consider the following marked X
```
[20ms] | _ O _ _ |^
[10ms] | _ _ _ _ || Vertical
[0ms]  | X _ O _ |v
         <--->
         Horizontal
```
If we had ``h_window=2`` and ``v_window=20``. These will be grouped as one, anything smaller will split them.

This is to group grace notes together as they are played as a chord if close enough.

By default, ``h_window=None`` will simply yield all columns.

### Avoid Jack

When grouping, you want to avoid grouping jacks together
```
[20ms] | O _ _ _ |^
[10ms] | _ _ _ _ || Vertical
[0ms]  | X _ _ _ |v
```

``avoid_jack=True`` will prevent that, forcing the next note to be in another group.

### Large Horizontal Window with Jack Avoidance

**This can cause overlapping groups.**

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

Notice the odd grouping. ``3`` was rejected as ``avoid_jack=True``. Causing it to group separately

## Examples

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

## Moving Forward

Understand this is basic, however, we need relationships between the groups to find patterns.

See the following.

```{toctree}
---
maxdepth: 1
---

Pattern Combinations <pattern/PtnCombo>
Pattern Filters <pattern/PtnFilter>
```
## Conventions

**Group**: Notes bounds together, by ``v_window`` & ``h_window``.

**Window**: The area to check. If in time, milliseconds as unit. If in columns, column difference as unit.


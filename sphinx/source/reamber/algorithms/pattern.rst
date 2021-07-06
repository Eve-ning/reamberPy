#################
Pattern Detection
#################

The aim of this package is to ease the way to find occurrence of specific patterns. See PtnCombo on how to detect
patterns/combinations after grouping.

**Input**

The ``Pattern.__init__()`` takes in ``cols: List[int], offsets: List[float], types: List[Type]``. However if you are
using ``Map`` objects, you can extract from the ``NoteList`` s with ``fromPkg`` like such.

.. code-block:: python

    osu = OsuMap.read_file("path/to/file.osu")

    Pattern.fromPkg([osu.notes.hits(), osu.notes.holds()])

This initializes the class with required lists for you to use ``group()``

***********
Conventions
***********

The conventions in this package may be confusing as some are not used anywhere in VSRGs.

**Group**: Notes grouped together, usually by a specified condition.

**Sequence**: Singular notes, one after another. E.g. ``[0, 1, 3, 0, ...]``

**Chord**: Multiple notes on the (almost) same offset. E.g. ``[0 1 4], [2 5 6]``

**Chord Sequence**: (Unused) Chords, one after another. E.g. ``[[0 1], [2 3], [1 3], ...]``

**Window**: The area to check. If in time, milliseconds as unit. If in columns, column difference as unit.

********
Grouping
********

The grouping algorithm looks at every note and tries to group them with other notes according to conditions specified.

``group`` Groups the package horizontally and vertically, returns a list of groups.

Vertical & Horizontal Window
============================

These windows define how far forward or to the side a note should look for to group.

If 3 notes are each **30ms** apart, a **50ms** VWindow will group them as ``[0, 1][2]`` as ``2`` is **60ms** away from
``1``

If there's a chord ``[0 1 6 7]``, a **1** HWindow will group them as ``[0, 1][6, 7]``. HWindow is rarely used, but kept
in case it's required.

There are multiple examples below to further illustrate how it works.

Warning
=======

**Warning: Having too high of a hwindow can cause overlapping groups.**

A 4K Example::

    ===========      ===========
    | O O _ O |      | 6 7 _ 8 |
    | O _ O O |  ==  | 3 _ 4 5 | ! Notes are labelled from 1 to 8 for simplicity
    | _ O O _ |      | _ 1 2 _ |
    ===========      ===========

If our window is too large, the algorithm will group it as ``[1,2,3,5][4,6,7,8]``.

The overlapping ``[3,4,5]`` in 2 groups may cause issues in calculation.

Examples
========

Let's say we want to group with the parameters
``vwindow = 0, hwindow = None``::

    [4s]  _5__           _5__           _5__           _5__           _X__
    [3s]  ___4  GROUP 1  ___4  GROUP 2  ___4  GROUP 3  ___X  GROUP 4  ___X
    [2s]  _2_3  ------>  _2_3  ------>  _X_X  ------>  _X_X  ------>  _X_X
    [1s]  ____  [1]      ____  [2,3]    ____  [4]      ____  [5]      ____
    [0s]  1___           X___           X___           X___           X___

    Output: [1][2,3][4][5]

``vwindow = 1000, hwindow = None``::

    [4s]  _5__           _5__           _5__           _X__
    [3s]  ___4  GROUP 1  ___4  GROUP 2  ___X  GROUP 3  ___X
    [2s]  _2_3  ------>  _2_3  ------>  _X_X  ------>  _X_X
    [1s]  ____  [1]      ____  [2,3,4]  ____  [5]      ____
    [0s]  1___           X___           X___           X___

    Output: [1][2,3,4][5]

2, 3 and 4 are grouped together because 4 is within the vwindow of 2;

``2.offset + vwindow <= 4.offset``

``vwindow = 1000, hwindow = 1``::

    [4s]  _5__           _5__          _5__           _5__           _X__
    [3s]  ___4  GROUP 1  ___4  GROUP 2 ___4  GROUP 3  ___X  GROUP 4  ___X
    [2s]  _2_3  ------>  _2_3  ------> _X_3  ------>  _X_X  ------>  _X_X
    [1s]  ____  [1]      ____  [2]     ____  [3,4]    ____  [5]      ____
    [0s]  1___           X___          X___           X___           X___

    Output: [1][2][3,4][5]

2 and 3 aren't grouped together because they are > 1 column apart. (Hence the hwindow argument)

*************
Going Forward
*************

You could directly use groups for your own uses or pivot off these other sub-packages.

.. toctree::
    :maxdepth: 1

    Pattern Combinations <pattern/PtnCombo>
    Pattern Filters <pattern/PtnFilter>

***********
Module Info
***********

.. automodule:: reamber.algorithms.pattern.Pattern


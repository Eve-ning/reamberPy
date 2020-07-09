Pattern Detection
=================

The aim of this sub-package is to ease the way to find occurrence of specific patterns.

Here's what it offers:

1. Customizable notes to group. If you want to only check notes from different categories, you can do so.
2. Grouping of notes. E.g. If you are looking for a ``[1][2][1]`` pattern, the algorithm will include ``[13][2][14]``.
3. Fuzzy Offset Grouping (1.), i.e. it can look for graces and lasso them into 1 single group.
4. Fuzzy Column Grouping (1.), i.e. you can conditionally only group within **n columns** of the current note.
5. Combination finding. This ``combinations`` algorithm can help find all possible sequences of notes for you. E.g.
   ``[13][2][14]`` will yield ``[1][2][1], [1][2][4], [3][2][1], [3][2][4]``
6. Custom filtering. You can use 3 different filters to remove unwanted sequences/chords/type sequences on output.

Example
-------

This example extracted from PFDrawLines shows a usage on how we can detect jacks only

.. code-block:: python
   :linenos:

   osu = OsuMap()
   osu.readFile("path/to/file.osu")

   ptn = Pattern.fromPkg([osu.notes.hits(), osu.notes.holds()])
   grp = ptn.group(hwindow=None, vwindow=50, avoidJack=True)

   combo = Pattern.combinations(
               groups,
               size=minimumLength,
               flatten=True,
               makeSize2=True,
               comboFilter=PtnFilterCombo.create(
                   [[0] * minimumLength], keys=keys,
                   method=PtnFilterCombo.Method.REPEAT,
                   invertFilter=False).filter,
               typeFilter=PtnFilterType.create(
                   [[HoldTail, object]],
                   method=PtnFilterType.Method.ANY_ORDER,
                   invertFilter=True).filter)

In this short example, what happened was that:

1. We groups the hits and holds with a **50ms** Vertical Window. That means any notes that are 50ms away from each other
   will be grouped together.
2. We then find the ``combinations`` of all groups. That is, in a way, all permutations. E.g. ``[1,2][3,4]`` will yield
   ``[1,3][2,3][2,4][1,4]``. The size of the permutation can be scaled infinitely determined by ``size=size``
3. ``flatten`` and ``makeSize2`` are arguments to drop groupings and make it a 2 column, n row ndarray.
4. A ``comboFilter`` can be used to filter out unwanted combos. E.g. as above, ``[1,3][2,3][2,4][1,4]`` can be filtered
   with ``[1,3]`` or ``[2,4]`` only, to reduce the size of the output.
5. A ``typeFilter`` does the same. The algorithm keeps the classes of the notes and filters out unwanted types.
6. There's also a ``chordFilter`` unused here, **(4.),(5.),(6.)** documentation can be found below.

Module Info
-----------

.. automodule:: reamber.algorithms.pattern.Pattern


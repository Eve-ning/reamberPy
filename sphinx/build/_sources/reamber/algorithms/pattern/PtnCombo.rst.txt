####################
Pattern Combinations
####################

After feeding ``PtnCombo`` with ``Pattern.groups(...)`` you can find out different combinations that the map has.

This ``combinations`` algorithm can help find all possible sequences of notes for you. E.g.
   ``[13][2][14]`` will yield ``[1][2][1], [1][2][4], [3][2][1], [3][2][4]``

With custom :doc:`filtering<PtnFilter>`, you can use 3 different filters to remove unwanted sequences/chords/type
sequences on output.

*******
Example
*******

This example extracted from PFDrawLines shows a usage on how we can detect jacks only

.. code-block:: python
   :linenos:

   osu = OsuMap()
   osu.readFile("path/to/file.osu")

   ptn = Pattern.fromPkg([osu.notes.hits(), osu.notes.holds()])
   grp = ptn.group(hwindow=None, vwindow=50, avoidJack=True)

   combo = PtnCombo(grp).combinations(
               size=minimumLength,
               flatten=True,
               makeSize2=True)

In this short example, what happened was that:

1. **Line 5**: We groups the hits and holds with a **50ms** Vertical Window. That means any notes that are 50ms away
   from each other will be grouped together.
2. **7**: We then find the ``combinations`` of all groups. That is, in a way, all permutations. E.g. ``[1,2][3,4]`` will
   yield ``[1,3][2,3][2,4][1,4]``. The size of the permutation can be scaled infinitely determined by ``size=size``
3. **9 & 10**: ``flatten`` and ``makeSize2`` are arguments to drop groupings and make it a 2 column, n row ndarray.

*********************
Template Combinations
*********************

In the ``PtnCombo`` class, there's default templates available to be used. This uses a :doc:`filtering<PtnFilter>` arg
to sieve out unwanted combinations.

Chord Stream Template
=====================

.. code-block:: python
   :linenos:

   combo = self.combinations(...

       chordFilter=PtnFilterChord.create(
           [[primary, secondary]],
           method=PtnFilterChord.Method.ANY_ORDER | PtnFilterChord.Method.AND_LOWER if andLower else 0,
           invertFilter=False, ...).filter,

       comboFilter=PtnFilterCombo.create(
           [[0, 0]],
           method=PtnFilterCombo.Method.REPEAT,
           invertFilter=True, ...).filter if not includeJack else None,

       typeFilter=PtnFilterType.create(
           [[HoldTail, object]],
           method=PtnFilterType.Method.ANY_ORDER,
           invertFilter=True, ...).filter)

**In Summary:**

1. Looks for any chord size pair below the ``primary`` and ``secondary`` value.
2. Excludes jacks
3. Excludes ``HoldTail`` and any other ``object`` combinations.

The above rules can be adjusted by either creating another template or adjusting provided parameters.

Jack Template
=============

.. code-block:: python
   :linenos:

   combo = self.combinations(...,

        comboFilter=PtnFilterCombo.create(
            [[0] * minimumLength], keys=keys,
            method=PtnFilterCombo.Method.REPEAT,
            invertFilter=False).filter,

        typeFilter=PtnFilterType.create(
            [[HoldTail] + [object] * (minimumLength - 1)],
            method=PtnFilterType.Method.ANY_ORDER,
            invertFilter=True).filter)

**In Summary:**

1. Looks for any ``[0, 0, ...], [1, 1, ...], [2, 2, ...], ...`` dependent on ``minimumLength``
2. Excludes ``HoldTail`` and any other ``object`` combinations.

***********
Module Info
***********

.. automodule:: reamber.algorithms.pattern.combos.PtnCombo
   :inherited-members:




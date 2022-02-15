####################
Pattern Combinations
####################

**Not supported beyond v0.1.0, open to request of revival.**

You can find out different combinations that the map has from ``Pattern.groups(...)`` with this class.

This ``combinations`` algorithm can help find all possible sequences of notes for you. E.g.
``[13][2][14]`` will yield ``[1][2][1], [1][2][4], [3][2][1], [3][2][4]``

With custom :doc:`filtering<PtnFilter>`, you can use 3 different filters to remove unwanted sequences/chords/type
sequences on output.

*******
Example
*******

This simply gets all possible combinations from the notes provided in ``combinations``.

.. code-block:: python

   ptn = Pattern.from_note_lists([osu.notes.hits(), osu.notes.holds()])
   grp = ptn.group(hwindow=None, vwindow=50, avoidJack=True)

   combo = PtnCombo(grp).combinations(size=minimumLength, flatten=True, makeSize2=True)

``flatten`` and ``makeSize2`` are arguments to drop groupings and make it a 2 column, n row ndarray.

Size
====

If you want to group by 2, that is, find all combinations from pairs, ``size=2`` is the argument.
Here's an illustration.

**Size 2**::

   GRP 1  GRP 2  GRP 3      CMB 1                          CMB 2
   [1, 2] [0, 3] [0, 2] --> [1, 0], [1, 3], [2, 0], [2, 3] [0, 0], [0, 2], [3, 0], [3, 2]

**Size 3**::

   GRP 1  GRP 2  GRP 3      CMB 1
   [1, 2] [0, 3] [0, 2] --> [1, 0, 0], [1, 0, 2], [1, 3, 0], ..., [2, 3, 2]

*********************
Template Combinations
*********************

In the ``PtnCombo`` class, there's default templates available to be used. This uses a :doc:`filtering<PtnFilter>` arg
to sieve out unwanted combinations.

Chord Stream
============

.. code-block:: python

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

Jack
====

.. code-block:: python

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




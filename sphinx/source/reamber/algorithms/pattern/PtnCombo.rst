####################
Pattern Combinations
####################

:doc:`After creating groups<../Pattern>`, you find relationships between them through this.

This loops through groups and yields their Cartesian Product.::

    Cartesian Product of [0, 1, 2] [A, B, C]
        A  B  C
      +---------
    0 | A0 B0 C0
    1 | A1 B1 C1
    2 | A2 B2 C2

    = A0 B0 C0 A1 B1 C1 A2 B2 C2

Here's how you run it.

.. code-block:: python

    g = Pattern.from_note_lists(...).group(...)

    combos = PtnCombo(g).combinations(
        size=2,
        flatten=False,
        make_size2=False,
        chord_filter: Callable[[np.ndarray], bool] = None,
        combo_filter: Callable[[np.ndarray], np.ndarray[bool]] = None,
        type_filter: Callable[[np.ndarray], np.ndarray[bool]] = None
        )

This looks daunting, however all arguments are optional.

Take for example::

    If Group B comes after A,
    Group A = [0, 1]
    Group B = [3, 4]

    Combinations = [0, 3] [0, 4] [1, 3] [1, 4]

Here's a real example

.. code-block:: python

    m: OsuMap
    g = Pattern.from_note_lists([m.hits, m.holds])
              .group(hwindow=None, vwindow=50, avoidJack=True)

    combos = PtnCombo(g).combinations()

Size
====

Size defines how many groups to be combined together.

**Size 2**::

    With 3 Groups, we yield 2 Cartesian products
    GRP 1  GRP 2  GRP 3
    [1, 2] [0, 3] [0, 2]

    GRP 1 x GRP 2 = [1, 0], [1, 3], [2, 0], [2, 3]
    GRP 2 x GRP 3 = [0, 0], [0, 2], [3, 0], [3, 2]

**Size 3**::

   GRP 1  GRP 2  GRP 3
   [1, 2] [0, 3] [0, 2]

   GRP 1 x GRP 2 x GRP 3 = [1, 0, 0], [1, 0, 2], [1, 3, 0], ..., [2, 3, 2]

*********************
Flatten & Make Size 2
*********************

By default, the returned structure is::

    If we are combining
    Group A = [0, 1]
    Group B = [3, 4]
    size = 2

    Combination: [[[0, 3], [0, 4]], [[1, 3], [1, 4]]]
    Combination with Flatten: [[0, 3], [0, 4], [1, 3], [1, 4]]

If ``size>2``::


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

*********
Filtering
*********

Not all combinations may be desired, thus filtering is in-built to remove unwanted patterns/combinations.

There are **3 Filters**:

- Chord Filtering
- Combo Filtering
- Type Filtering

Take a look at :doc:`Filtering<PtnFilter>` to utilize ``chord_filter, combo_filter, type_filter``.

# TODO Migrate the bottom to Filter

*********************
Template Combinations
*********************

In ``PtnCombo``, I provide templates to common filters. This uses a :doc:`filtering<PtnFilter>` arg
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




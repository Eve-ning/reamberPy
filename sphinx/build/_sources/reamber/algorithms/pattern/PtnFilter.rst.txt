###############
Pattern Filters
###############

This class facilitates filtering unwanted sequences, chord sequences from the ``combination`` function provided by
``PtnCombo``.

This class is used in the :doc:`Combinations Class <PtnFilter>`, it's main use is through that.

*************
Using Filters
*************

By default, ``combination`` has 3 custom filters set to ``None``, that is, it's not active. All of them expect a
``Callable`` and require specific inputs and outputs of that.

For this, I also developed a simple way to create callable with filters.

In ``PtnFilter``, there are ``PtnFilterChord, PtnFilterCombo, PtnFilterType``, according to the required input of
``combination``. By initializing each class and getting their ``filter`` function callable, you can easily create a
filter.

Here's a simple example on how to fill it in

.. code-block:: python

    combinations(
        size=2,
        flatten=True,
        makeSize2=True,
        chordFilter=PtnFilterChord.create(...).filter,
        comboFilter=PtnFilterCombo.create(...).filter,
        typeFilter=PtnFilterType.create(...).filter)

Within create, ``...`` requires specific arguments to initialize the filter

************
Filter Chord
************

Arguments::

    sizes: List[List[int]],
    keys:int,
    method: PtnFilterChord.Method or int = 0,
    invertFilter:bool = False

Sizes
=====

These are the sizes of the chords to include (if ``invertFilter is False``).

Example (assume ``keys=4``)::

    sizes=[[1, 2], [2, 3]]

    These chords sequences (in columns) are therefore accepted.

    For [1, 2] sizes:
        [[0], [0, 1]], [[0], [0, 2]], ..., [[1], [2, 3]], ... , [[3], [2, 3]]

    For [2, 3] sizes:
        [[0, 1], [0, 1, 2]], [[0, 1], [0, 1, 2]], ..., [[2, 3], [1, 2, 3]]

Note that columns aren't repeated.

Methods
=======

Methods are options you can toggle in order to get a required filter faster instead of manually inputting all of them.

The methods provided are::

    ANY_ORDER
    AND_LOWER
    AND_HIGHER

The details are specified in the docstring::

    AnyOrder generates any chord sequences that is a combination of the current

    [2][2][1] --ANYORDER-> [[2][2][1],[1][2][2],[2][1][2]]

    AndLower generates any chord sequences that is lower than the current

    [2][2][1] --ANDLOWER-> [[2][2][1],[1][2][1],[2][1][1],[1][1][1]]

    AndHigher is just the opposite of AndLower

************
Filter Combo
************

Arguments::

    cols: List[List[int]],
    keys: int,
    method: Method or int = 0,
    invertFilter: bool = False

Columns
=======

These are the columns of the combinations to include (if ``invertFilter is False``).

Example (assume ``keys=4``)::

    columns=[[1, 2], [2, 3]]

    These chords sequences (in columns) are therefore accepted.

    As expected, we only accept [1, 2] or [2, 3]

Methods
=======

Methods are options you can toggle in order to get a required filter faster instead of manually inputting all of them.

The methods provided are::

    REPEAT
    HMIRROR
    VMIRROR

The details are specified in the docstring::

    Repeat just repeats the base pattern without changing its orientation.

    [0][1] --REPEAT-> [[0][1],[1][2],[2][3]] for keys=4

    Hmirror reflects the pattern on the y-axis

    [0][1] --HMIRROR-> [[0][1],[2][3]] for keys=4

    Vmirror reflects the pattern on the x-axis

    [0][1] --HMIRROR-> [[0][1],[1][0]] for keys=4

***********
Filter Type
***********

Arguments::

    types: List[List[type]],
    keys: int,
    method: PtnFilterType.Method or int = 0,
    invertFilter: bool = False

Types
=====

These are the types of the combinations to include (if ``invertFilter is False``).

Example::

    columns=[[Hit, Hit], [Hold, Hit]]

    These type sequences are therefore accepted.

    As expected, we will only accept sequences that are (Hit then Hit) or (Hold then Hit)

Methods
=======

Methods are options you can toggle in order to get a required filter faster instead of manually inputting all of them.

The methods provided are::

    ANY_ORDER
    MIRROR

The details are specified in the docstring::

    AnyOrder generates any chord sequences that is a combination of the current

    [A][A][B] --ANYORDER-> [[A][A][B],[A][B][A],[B][A][A]]

    mirror generates a flipped copy

    [A][A][B] --VMIRROR-> [[A][A][B],[B][A][A]]

**************
Custom Filters
**************

Though not recommended, I deliberately made it such that the filter arguments can accept any ``Callable`` so that you
can implement your own lambdas to detect patterns.

Extracted from the ``PtnCombo.combination()`` docstring, these are the details to implement your own filters.

**Chord Filter**

Input: ndarray of ``({size},)``. Where it tells us the length of each chord.

e.g. [3, 4, 1] means there is a 3, 4, 1 note chord respectively.

The filter must take that as an argument and return a boolean, whether to INCLUDE the chord sequence or not.

**Combo Filter**

Input: ndarray of ``(x, {size})``. Where each row tells us the column

e.g. [[1, 3, 2], [3, 1, 0]] means there is both a 1 -> 3 -> 2 and 3 -> 1 -> 0 sequence in the chunk.

The filter must take this and return an ndarray boolean of ``(x,)``.

Each boolean will tell if the chord should be INCLUDED or not.

**Type Filter**

Input: ndarray of ``(x, {size})``. Where each row tells us the type

e.g. [[Hit, Hold], [Hold, HoldTail]] means there is both a Hit -> Hold and Hold -> HoldTail sequence in the chunk

The filter must take this and return an ndarray boolean of ``(x,)``.

Each boolean will tell if the chord should be INCLUDED or not.

***********
Module Info
***********

.. automodule:: reamber.algorithms.pattern.filters.PtnFilter



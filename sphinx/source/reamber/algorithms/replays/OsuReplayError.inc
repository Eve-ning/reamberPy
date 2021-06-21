Osu! Replay Error
=================

To initialize the class, you need 2 arguments

Replays:
- Path to osu! replays or
- `Replays`

Map:
- Path to osu! map
- `OsuMap`

After initialization, to get the errors, call `errors()`.

Output
------

The output format is slightly complex

.. code-block:: python

    hit_errors: List[List[List[int]]]
    rel_errors: List[List[List[int]]]
    hit_map:    List[List[int]]
    rel_map:    List[List[int]]
    ln_len_map: List[List[int]]
    hit_reps:   List[List[List[int]]]
    rel_reps:   List[List[List[int]]]

**Hit/Release Errors**

Nesting
- Replay Index
- Key of Error
- Index of Error (This is consistent with the map hits)

.. code-block:: python

    rep.errors().hit_error[0][3][10]

Gets the **First Replay**, **Errors of 4th Column**, **11th Hit Error**.

**Hit/Release/LN Length Map**

Nesting
- Key of Offset/Length
- Index of Offset/Length

.. code-block:: python

    rep.errors().hit_map[3][10]

Gets the **Offsets of 4th Column**, **11th Hit Offset**.

**Hit/Release Replays**

Nesting
- Key of Hit/Release
- Index of Hit/Release

.. code-block:: python

    rep.errors().hit_rep[3][10]

Gets the **Hit of 4th Column**, **11th Hit Offset**.

Note that this is whenever the player hits/releases a key.

Example
-------

The following example extracts the hit errors of the first replay and plots in a histogram.

**Input**

.. code-block:: python
   :linenos:

    rep = OsuReplayError(["path/to/rep1.osr", "path/to/rep2.osr"], "path/to/map.osu")
    er = rep.errors()
    plt.hist([e for k in er.hit_errors[1] for e in k], bins=100)
    plt.show()

Module Info
-----------

.. automodule:: reamber.algorithms.replays.OsuReplayError

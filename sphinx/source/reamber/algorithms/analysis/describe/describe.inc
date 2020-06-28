Describe
========

Example describe
----------------

.. code-block:: python
    :linenos:

    from reamber.algorithms.analysis.describe.describe import describe

    m = OsuMapObj()
    m.readFile("../rsc/maps/osu/ICFITU.osu")
    describe(m, s=None)

.. code-block::
    :linenos:

    Average BPM: 175.0
    Map Length: 0:06:48.514000
    Camellia - I Can Fly In The Universe, Schizophrenia (Evening)
    ---- NPS ----
    All:  Count: 6896, 50% (Median): 12.00, 75%: 14.00, 100% (Max): 24.00
    Col0: Count: 1709, 50% (Median): 6.00, 75%: 6.00, 100% (Max): 9.00
    Col1: Count: 1736, 50% (Median): 6.00, 75%: 6.00, 100% (Max): 8.00
    Col2: Count: 1735, 50% (Median): 6.00, 75%: 6.00, 100% (Max): 9.00
    Col3: Count: 1716, 50% (Median): 6.00, 75%: 7.00, 100% (Max): 9.00

Example describeNotes
---------------------

Describes the notes in columns 0 and 2.

.. code-block:: python
    :linenos:

    from reamber.algorithms.analysis.describe.describe import describeNotes

    m = OsuMapObj()
    m.readFile("../rsc/maps/osu/ICFITU.osu")

    describeNotes(m.notes.inColumns([0,2]))

.. code-block::
    :linenos:

    Count: 3444, 50% (Median): 9.00, 75%: 10.00, 100% (Max): 16.00

Module Info
-----------

.. automodule:: reamber.algorithms.analysis.describe.describe
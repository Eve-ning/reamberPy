Map
===

Activity
--------

This algorithm finds out how long each Bpm is active and returns a List of tuple of ``(Bpm, ActiveTimeMs)``.

The last Bpm is calculated by the last Note present if not overridden.

**Input**

.. code-block:: python
   :linenos:

   from reamber.osu.OsuMap import OsuMap

   osu = OsuMap()
   osu.readFile("path/to/file.osu")
   print(osu.activity())

**Output**

Some redundant parameters redacted into ``...``.

.. code-block:: python
   :linenos:

    [(OsuBpm(offset=575.0, bpm=145, ...), 108974.0),
     (OsuBpm(offset=109549.0, bpm=175, ...), 54857.0)]


Describe
--------

Map sets will loop through describe.

.. code-block:: python
    :linenos:

    from reamber.algorithms.analysis.describe.describe import describe

    m = OsuMap()
    m.readFile("path/to/file.osu")
    describe(m, s=None)

.. code-block::
    :linenos:

   Average BPM: 175.0
   Map Length: 0:06:48.514000
   Camellia - I Can Fly In The Universe, Schizophrenia (Evening)
   ---- NPS ----
   hits
   Count: 6036, 50% (Median): 12.00, 75%: 14.00, 100% (Max): 24.00
   holds
   Count: 860, 50% (Median): 9.00, 75%: 12.00, 100% (Max): 12.00
   Average BPM: 172.0

Describe Notes
--------------

Describes the notes in columns 0 and 2.

.. code-block:: python
    :linenos:

    from reamber.algorithms.analysis.describe.describe import describeNotes

    m = OsuMap()
    m.readFile("path/to/file.osu")

    describeNotes(m.notes.inColumns([0,2]))

.. code-block::
    :linenos:

    Count: 3444, 50% (Median): 9.00, 75%: 10.00, 100% (Max): 16.00

Metadata
--------

.. code-block:: python
    :linenos:

    from reamber.osu.OsuMap import OsuMap
    from reamber.algorithms.analysis.describe.meta import mapMetadata

    m = OsuMap()
    m.readFile("path/to/file.osu")

    print(m.metadata())

.. code-block::
    :linenos:

    Camellia - I Can Fly In The Universe, Schizophrenia (Evening)


Notes Per Second (NPS)
----------------------

**Input**

.. code-block:: python
   :linenos:

    from reamber.algorithms.analysis.plot.nps import npsPlot

    from reamber.osu.OsuMap import OsuMap
    import matplotlib.pyplot as plt

    m = OsuMap()
    m.readFile("path/to/file.osu")
    print(m.nps())
    npsPlot(m, binSize=500)
    plt.show()

**Output**

.. code-block::
   :linenos:

        offset  hits  holds
   0         0   0.0    0.0
   1      2000   0.0    1.5
   2      4000   0.0    1.5
   3      6000   0.0    1.0
   4      8000   6.5    1.0
   ..      ...   ...    ...
   195  390000   2.0    1.0
   196  392000   5.5    1.0
   197  394000   1.0    1.0
   198  396000   1.5    0.5
   199  398000   3.0    2.0

   [200 rows x 3 columns]

Module Info
-----------

.. automodule:: reamber.base.Map
Bpm Activity
============

This algorithm finds out how long each Bpm is active and returns a List of tuple of ``(Bpm, ActiveTimeMs)``.

The last Bpm is calculated by the last Note present.

Example
-------

**Input**

.. code-block:: python
   :linenos:

   from reamber.algorithms.analysis.bpm.bpmActivity import bpmActivity
   from reamber.osu.OsuMap import OsuMap

   osu = OsuMap()
   osu.readFile("path/to/file.osu")
   print(bpmActivity(osu))

**Output**

Some redundant parameters redacted into ``...``.

.. code-block:: python
   :linenos:

    [(OsuBpm(offset=575.0, bpm=145.00000120833334, ...), 108974.0),
     (OsuBpm(offset=109549.0, bpm=175.00002187500274, ...), 54857.0)]

Module Info
-----------

.. automodule:: reamber.algorithms.analysis.bpm.bpmActivity
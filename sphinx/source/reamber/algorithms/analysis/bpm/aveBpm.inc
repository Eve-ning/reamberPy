Average Bpm
===========

Example
-------

**Input**

.. code-block:: python
   :linenos:

    from reamber.algorithms.analysis.bpm.aveBpm import aveBpm
    from reamber.osu.OsuMap import OsuMap

    osu = OsuMap()
    osu.readFile("path/to/file.osu")
    ave = aveBpm(osu)
    print(ave)

**Output**

.. code-block:: python
   :linenos:

    172.6882379418763

Module Info
-----------

.. automodule:: reamber.algorithms.analysis.bpm.aveBpm
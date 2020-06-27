Average Bpm
===========

Example
-------

**Input**

.. code-block:: python
   :linenos:

    from reamber.algorithms.analysis.bpm.aveBpm import aveBpm
    from reamber.osu.OsuMapObj import OsuMapObj

    osu = OsuMapObj()
    osu.readFile("../rsc/maps/osu/Caravan.osu")
    ave = aveBpm(osu)
    print(ave)

**Output**

.. code-block:: python
   :linenos:

    172.6882379418763

.. automodule:: reamber.algorithms.analysis.bpm.aveBpm
Bpm Beat Offsets
================

Example
-------

**Input**

.. code-block:: python
   :linenos:

   from reamber.algorithms.analysis.bpm.bpmBeatOffsets import bpmBeatOffsets
   from reamber.osu.OsuMapObj import OsuMapObj

   osu = OsuMapObj()
   osu.readFile("../rsc/maps/osu/LEG.osu")
   print(bpmBeatOffsets(osu.bpms, 4, 1000))

**Output**

Outputs all 1/4 snap offsets, starting from the first bpm.

.. code-block:: python
   :linenos:

    [-24.0, 62.206896551724256, 148.4137931034485, 234.62068965517278, 320.827586206897, 407.03448275862127,
    493.2413793103455, 579.4482758620697, 665.655172413794, 751.8620689655183, 838.0689655172426, 924.275862068967]

Module Info
-----------

.. automodule:: reamber.algorithms.analysis.bpm.bpmBeatOffsets
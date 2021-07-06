###
Bpm
###

************
Snap Offsets
************

**Input**

.. code-block:: python
   :linenos:

   from reamber.osu.OsuMap import OsuMap

   osu = OsuMap.read_file("path/to/file.osu")
   print(osu.bpms.snapOffsets(nths=4, lastOffset=1000))

**Output**

Outputs all 1/4 snap offsets, starting from the first bpm.

.. code-block:: python
   :linenos:

   [-24.0, 62.206896551724256, 148.4137931034485, 234.62068965517278, 320.827586206897, 407.03448275862127,
   493.2413793103455, 579.4482758620697, 665.655172413794, 751.8620689655183, 838.0689655172426, 924.275862068967]

************
Scroll Speed
************

Gets the scroll speed and visualizes it on matplotlib

.. code-block:: python
   :linenos:

   from reamber.osu.OsuMap import OsuMap
   import matplotlib.pyplot as plt
   import pandas as pd

   m = OsuMap.read_file("path/to/file.osu")
   pd.DataFrame(m.scrollSpeed()).set_index('offset').plot()
   plt.show()

This function gets the resulting scroll speed from the map as a dictionary

::

    [{'offset': OFFSET, 'speed': SPEED}, {'offset': OFFSET, 'speed': SPEED}, ... ]

***********
Module Info
***********

.. automodule:: reamber.base.Bpm
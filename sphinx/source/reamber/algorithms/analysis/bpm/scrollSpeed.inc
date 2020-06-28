Scroll Speed
============

Example
-------

Gets the scroll speed and visualizes it on matplotlib

.. code-block:: python
   :linenos:

    from reamber.osu.OsuMapObj import OsuMapObj
    from reamber.algorithms.analysis.bpm.scrollSpeed import scrollSpeed
    import matplotlib.pyplot as plt
    import pandas as pd

    def test_osu(self):
        m = OsuMapObj()
        m.readFile("file.osu")
        pd.DataFrame(scrollSpeed(m)).set_index('offset').plot()
        plt.show()

This function gets the resulting scroll speed from the map as a dictionary

::

    [{'offset': OFFSET, 'speed': SPEED}, {'offset': OFFSET, 'speed': SPEED}, ... ]

Module Info
-----------

.. automodule:: reamber.algorithms.analysis.bpm.scrollSpeed
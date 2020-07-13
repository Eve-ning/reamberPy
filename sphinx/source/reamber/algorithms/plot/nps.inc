Notes Per Second (NPS) Plotting
===============================

Example
-------

**Input**

.. code-block:: python
   :linenos:

    from reamber.algorithms.plot.nps import npsPlot

    from reamber.osu.OsuMap import OsuMap
    import matplotlib.pyplot as plt

    m = OsuMap.readFile("path/to/file.osu")
    npsPlot(m, binSize=500)
    plt.show()

**Output**

.. plot::
   :align: center
   :width: 100%
   :include-source: False

    from reamber.algorithms.plot.nps import npsPlot
    from reamber.osu.OsuMap import OsuMap
    import matplotlib.pyplot as plt

    m = OsuMap.readFile("plot/PLANETSHAPER.osu")
    npsPlot(m, binSize=500)
    plt.show()

Module Info
-----------

.. automodule:: reamber.algorithms.plot.nps

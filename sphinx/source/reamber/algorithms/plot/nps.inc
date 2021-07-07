Notes Per Second (NPS) Plotting
===============================

Example
-------

**Input**

.. code-block:: python
   :linenos:

    from reamber.algorithms.plot.nps import nps_plot

    from reamber.osu.OsuMap import OsuMap
    import matplotlib.pyplot as plt

    m = OsuMap.read_file("path/to/file.osu")
    nps_plot(m, binSize=500)
    plt.show()

**Output**

.. plot::
   :align: center
   :width: 100%
   :include-source: False

    from reamber.algorithms.plot.nps import nps_plot
    from reamber.osu.OsuMap import OsuMap
    import matplotlib.pyplot as plt

    m = OsuMap.read_file("plot/PLANETSHAPER.osu")
    nps_plot(m, binSize=500)
    plt.show()

Module Info
-----------

.. automodule:: reamber.algorithms.plot.nps

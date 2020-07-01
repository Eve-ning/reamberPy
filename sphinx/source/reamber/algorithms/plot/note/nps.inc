Notes Per Second (NPS) Plotting
===============================

Example
-------

**Input**

.. code-block:: python
   :linenos:

    from reamber.algorithms.analysis.note.nps import nps, npsPlot

    from reamber.osu.OsuMap import OsuMap
    import matplotlib.pyplot as plt

    m = OsuMap()
    m.readFile("path/to/file.osu")
    df = nps(m, binSize=2000)
    npsPlot(m, binSize=500)
    plt.show()

**Output**

.. plot::
   :align: center
   :width: 100%
   :include-source: False

    from reamber.algorithms.analysis.note.nps import nps, npsPlot
    from reamber.osu.OsuMap import OsuMap
    import matplotlib.pyplot as plt

    m = OsuMap()
    m.readFile("note/PLANETSHAPER.osu")
    npsPlot(m, binSize=500)
    plt.show()

Module Info
-----------

.. automodule:: reamber.algorithms.analysis.note.nps

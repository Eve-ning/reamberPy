Notes per Second
================

Example
-------

**Input**

.. code-block:: python
   :linenos:

    from reamber.algorithms.analysis.note.nps import nps, npsPlot

    from reamber.osu.OsuMapObj import OsuMapObj
    import matplotlib.pyplot as plt

    m = OsuMapObj()
    m.readFile("path/to/file.osu")
    df = nps(m, binSize=2000)
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

.. plot::
   :align: center
   :width: 100%
   :include-source: False

    from reamber.algorithms.analysis.note.nps import nps, npsPlot
    from reamber.osu.OsuMapObj import OsuMapObj
    import matplotlib.pyplot as plt

    m = OsuMapObj()
    m.readFile("PLANETSHAPER.osu")
    npsPlot(m, binSize=500)
    plt.show()

Module Info
-----------

.. automodule:: reamber.algorithms.analysis.note.nps

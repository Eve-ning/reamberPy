Notes per Second
================

.. automodule:: reamber.algorithms.analysis.note.nps

Example
=======

``plt.style.use('dark_background')`` uses the dark mode plotting.

.. code-block:: python
   :linenos:

    from reamber.osu.OsuMapObj import OsuMapObj
    import matplotlib.pyplot as plt

    m = OsuMapObj()
    m.readFile("file.osu")
    plt.style.use('dark_background')
    df = nps(m, binSize=2000)
    npsPlot(m, "npsOsu.png", binSize=500)

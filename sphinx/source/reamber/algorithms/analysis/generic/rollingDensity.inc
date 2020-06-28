Rolling Density
===============

Example
-------

Plotting the rolling density

**Input**

.. code-block:: python
    :linenos:

    from reamber.osu.OsuMapObj import OsuMapObj
    import matplotlib.pyplot as plt

    from reamber.algorithms.analysis.generic.rollingDensity import rollingDensity
    import os

    m = OsuMapObj()
    m.readFile("../rsc/maps/osu/PLANETSHAPER.osu")

    rollingDensity(m.notes.hits().offsets(), rollingWindowS=2).plot()
    plt.show()

**Output**

.. plot::
   :context:
   :align: center
   :width: 100%
   :include-source: False

    from reamber.osu.OsuMapObj import OsuMapObj
    import matplotlib.pyplot as plt

    from reamber.algorithms.analysis.generic.rollingDensity import rollingDensity
    import os

    m = OsuMapObj()
    m.readFile("../../../../../rsc/maps/osu/PLANETSHAPER.osu")

    rollingDensity(m.notes.hits().offsets(), rollingWindowS=2).plot()
    plt.show()

Module Info
-----------
.. automodule:: reamber.algorithms.analysis.generic.rollingDensity
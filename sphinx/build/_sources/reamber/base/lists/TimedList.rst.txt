Timed List
==========

Rolling Density
---------------

Plotting the rolling density

**Input**

.. code-block:: python
    :linenos:

    from reamber.osu.OsuMap import OsuMap
    import matplotlib.pyplot as plt

    from reamber.algorithms.analysis.generic.rollingDensity import rollingDensity
    import os

    m = OsuMap()
    m.readFile("path/to/file.osu")

    rollingDensity(m.notes.hits().offsets(), rollingWindowS=2).plot()
    plt.show()

**Output**

.. plot::
   :context:
   :align: center   :width: 100%
   :include-source: False

    from reamber.osu.OsuMap import OsuMap
    import matplotlib.pyplot as plt

    from reamber.algorithms.analysis.generic.rollingDensity import rollingDensity

    m = OsuMap()
    m.readFile("lists/PLANETSHAPER.osu")

    rollingDensity(m.notes.hits().offsets(), rollingWindowS=2).plot()
    plt.show()

Module Info
-----------

.. automodule:: reamber.base.lists.TimedList
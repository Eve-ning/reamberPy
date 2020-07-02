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

    m.notes.hits().rollingDensity(2).plot()
    plt.show()

**Output**

.. plot::
   :context:
   :align: center
   :width: 100%
   :include-source: False

    from reamber.osu.OsuMap import OsuMap
    import matplotlib.pyplot as plt

    m = OsuMap()
    m.readFile("PLANETSHAPER.osu")

    m.notes.hits().rollingDensity(2).plot()
    plt.show()

Module Info
-----------

.. automodule:: reamber.base.lists.TimedList
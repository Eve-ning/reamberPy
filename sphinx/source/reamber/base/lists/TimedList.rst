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

    from reamber.algorithms.analysis.generic.rolling_density import rolling_density
    import os

    m = OsuMap.read_file("path/to/file.osu")

    density = m.notes.hits().rolling_density(window=5000, stride=2500)
    plt.plot(list(density.keys()), list(density.values()))
    plt.show()

**Output**

.. plot::
   :context:
   :align: center
   :width: 100%
   :include-source: False

    from reamber.osu.OsuMap import OsuMap
    import matplotlib.pyplot as plt

    m = OsuMap.read_file("PLANETSHAPER.osu")

    density = m.notes.hits().rolling_density(window=5000, stride=2500)
    plt.plot(list(density.keys()), list(density.values()))
    plt.show()

Module Info
-----------

.. automodule:: reamber.base.lists.TimedList
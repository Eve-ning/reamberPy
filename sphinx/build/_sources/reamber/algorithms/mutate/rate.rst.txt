Rate Changer
============

Example
-------

.. code-block:: python

    m = OsuMap()
    m.readFile("../rsc/maps/osu/Caravan.osu")
    rate(m, 2.0, inplace=True)
    m.writeFile("Caravan200.osu")

.. automodule:: reamber.algorithms.mutate.rate
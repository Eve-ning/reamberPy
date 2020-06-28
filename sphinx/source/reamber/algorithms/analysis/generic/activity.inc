Rolling Density
===============


Example Map Set
---------------

For a mapset, you must specify both the map and mapset as an input

.. code-block:: python
    :linenos:

    from reamber.sm.SMMapSetObj import SMMapSetObj
    from reamber.algorithms.analysis.describe.meta import mapMetadata

    s = SMMapSetObj()
    s.readFile("../rsc/maps/sm/Caravan.sm")

    print(mapMetadata(s.maps[0], s))

.. code-block::
    :linenos:

    John Wasson - Caravan, Easy (Evening)

Module Info
-----------
.. automodule:: reamber.algorithms.analysis.generic.rollingDensity
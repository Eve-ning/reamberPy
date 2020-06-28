Map Metadata
============

Example Map
-----------

.. code-block:: python
    :linenos:

    from reamber.osu.OsuMap import OsuMap
    from reamber.algorithms.analysis.describe.meta import mapMetadata

    m = OsuMap()
    m.readFile("path/to/file.osu")

    print(mapMetadata(m))

.. code-block::
    :linenos:

    Camellia - I Can Fly In The Universe, Schizophrenia (Evening)

Example Map Set
---------------

For a mapset, you must specify both the map and mapset as an input

.. code-block:: python
    :linenos:

    from reamber.sm.SMMapSet import SMMapSet
    from reamber.algorithms.analysis.describe.meta import mapMetadata

    s = SMMapSet()
    s.readFile("path/to/file.sm")

    print(mapMetadata(s.maps[0], s))

.. code-block::
    :linenos:

    John Wasson - Caravan, Easy (Evening)

Module Info
-----------
.. automodule:: reamber.algorithms.analysis.describe.meta
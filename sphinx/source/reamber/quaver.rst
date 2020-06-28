######
Quaver
######

********
Examples
********

1. Read and Write
=================

.. code-block:: python
   :linenos:

    from reamber.quaver.QuaMap import QuaMap

    q = QuaMap()
    q.readFile("file.qua")
    q.writeFile("fileOut.qua")

2. Prints all the SV Multipliers
================================

.. code-block:: python
   :linenos:

   from reamber.quaver.QuaMap import QuaMap

   q = QuaMap()
   q.readFile("file.qua")

   print(q.svs.multipliers())

3. Multiply all Bpms and Svs by 1.5
===================================

.. code-block:: python
   :linenos:

   from reamber.quaver.QuaMap import QuaMap

   q = QuaMap()
   q.readFile("file.qua")

   for sv in q.svs.data():
       sv.multiplier *= 1.5

   for bpm in q.bpms.data():
       bpm.bpm *= 1.5

***********
Module Info
***********

.. toctree::
    Lists <quaver/lists>

.. include:: quaver/Bpm.inc

.. include:: quaver/Hit.inc

.. include:: quaver/Hold.inc

.. include:: quaver/Map.inc

.. include:: quaver/MapMeta.inc

.. include:: quaver/NoteMeta.inc

.. include:: quaver/Sv.inc

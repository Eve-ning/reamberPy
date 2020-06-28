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

    from reamber.quaver.QuaMapObj import QuaMapObj

    q = QuaMapObj()
    q.readFile("file.qua")
    q.writeFile("fileOut.qua")

2. Prints all the SV Multipliers
================================

.. code-block:: python
   :linenos:

   from reamber.quaver.QuaMapObj import QuaMapObj

   q = QuaMapObj()
   q.readFile("file.qua")

   print(q.svs.multipliers())

3. Multiply all Bpms and Svs by 1.5
===================================

.. code-block:: python
   :linenos:

   from reamber.quaver.QuaMapObj import QuaMapObj

   q = QuaMapObj()
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

.. include:: quaver/BpmObj.inc

.. include:: quaver/HitObj.inc

.. include:: quaver/HoldObj.inc

.. include:: quaver/MapObj.inc

.. include:: quaver/MapObjMeta.inc

.. include:: quaver/NoteObjMeta.inc

.. include:: quaver/SvObj.inc

######
Quaver
######

********
Examples
********

1. Read and Write
=================

.. code-block:: python

    from reamber.quaver.QuaMap import QuaMap

    q = QuaMap.read_file("file.qua")
    q.write_file("file_out.qua")

2. Prints all the SV Multipliers
================================

.. code-block:: python

   from reamber.quaver.QuaMap import QuaMap

   q = QuaMap.read_file("file.qua")

   print(q.svs.multipliers)

3. Multiply all Bpms and Svs by 1.5
===================================

.. code-block:: python

   from reamber.quaver.QuaMap import QuaMap

   q = QuaMap.read_file("file.qua")

   for sv in q.svs.data():
       sv.multiplier *= 1.5

   for bpm in q.bpm.data():
       bpm.bpm *= 1.5

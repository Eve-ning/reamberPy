#####
O2Jam
#####

**OJM is not supported, hence the following will not be supported.**

- Writing to O2Jam (OJN, OJM)
- Reading OJN
- Reading the Music File
- Exporting to MP3
- Exporting to Keysounds

********
Examples
********

Not many examples since this is not writable.

1. Read
=======

Writing is not supported. However, you can convert it to other formats.

.. code-block:: python
   :linenos:

    from reamber.o2jam.O2JMapSet import O2JMapSet
    o2j = O2JMapSet.read_file("file.ojn")

2. Get the number of Notes of the Easy Map
==========================================

.. code-block:: python
   :linenos:

   from reamber.o2jam.O2JMapSet import O2JMapSet

   o2j = O2JMapSet.read_file("file.ojn")

   # Gets the first difficulty: o2j.maps[0]
   # Gets the Note Package: .notes
   # As a dictionary: .data()
   # Get the values of the dictionary only: .values()
   # For each value, we fetch the length of each of its data: len(lis.data())
   # We sum everything
   print(sum([len(lis.data()) for lis in o2j.maps[0].notes.data().values()]))

***********
Module Info
***********

.. toctree::
    Lists <o2jam/lists>

.. include:: o2jam/Bpm.inc

.. include:: o2jam/Hit.inc

.. include:: o2jam/Hold.inc

.. include:: o2jam/Map.inc

.. include:: o2jam/MapSet.inc

.. include:: o2jam/MapSetMeta.inc

.. include:: o2jam/NoteMeta.inc

.. include:: o2jam/EventPackage.inc
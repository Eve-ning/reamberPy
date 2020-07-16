###
BMS
###

********
Examples
********

1. Read and Write
=================

#TODO: Link to BMSChannel

There are different channel configurations for BMS-style maps. More info in the BMSChannel Page

.. code-block:: python
   :linenos:

    from reamber.quaver.BMSMap import BMSMap

    bms = BMSMap.readFile("path/to/file.bme", noteChannelConfig=BMSChannel.BME)
    bms.writeFile("fileOut.bme")

2. Prints all the BPMs
======================

.. code-block:: python
   :linenos:

   from reamber.bms.BMSMap import BMSMap

   bms = BMSMap.readFile("path/to/file.bme", noteChannelConfig=BMSChannel.BME)
   print(bms.bpms.bpms())

3. Move all columns to the right by 1
=====================================

.. code-block:: python
   :linenos:

   from reamber.bms.BMSMap import BMSMap

   bms = BMSMap.readFile("path/to/file.bme", noteChannelConfig=BMSChannel.BME)

   for hit in bms.notes.hits():
       hit.column += 1
   for hold in bms.notes.holds():
       hold.column += 1

***********
Module Info
***********

.. toctree::
    Lists <bms/lists>
    BMS Channel Configurations <bms/Channel>

.. include:: bms/Bpm.inc

.. include:: bms/Hit.inc

.. include:: bms/Hold.inc

.. include:: bms/Map.inc

.. include:: bms/MapMeta.inc

.. include:: bms/NoteMeta.inc

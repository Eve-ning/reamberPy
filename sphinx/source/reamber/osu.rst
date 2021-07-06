####
Osu!
####

We support the osu! file format except for the following:

- Storyboard Elements
- Standard, Catch, Taiko

This package supports most operations for osu! To better understand how to use this package here are some examples

********
Examples
********

1. Read and Write
=================

.. code-block:: python
   :linenos:

    from reamber.osu.OsuMap import OsuMap

    osu = OsuMap.read_file("file.osu")
    osu.write_file("fileOut.osu")

2. Print all LN Lengths
=======================

.. code-block:: python
   :linenos:

    from reamber.osu.OsuMap import OsuMap

    osu = OsuMap.read_file("file.osu")
    print(osu.notes.holds().lengths())

3. Set all notes' volume to 0
=============================

Note how you need to grab data with ``data()``. This operation exports the current object as a primitive type.

This operation is by reference, that's why you can just do operations on the export.

.. code-block:: python
   :linenos:

   from reamber.osu.OsuMap import OsuMap

   osu = OsuMap.read_file("file.osu")

   for k, i in osu.notes.data().items():
       for obj in i.data():
           obj.volume = 0

***********
Module Info
***********

.. toctree::
   Lists <osu/lists>

.. include:: osu/Bpm.inc

.. include:: osu/Sv.inc

.. include:: osu/Hit.inc

.. include:: osu/Hold.inc

.. include:: osu/Map.inc

.. include:: osu/MapMeta.inc

.. include:: osu/NoteMeta.inc

.. include:: osu/Sample.inc

.. include:: osu/SampleSet.inc

.. include:: osu/TimingPointMeta.inc

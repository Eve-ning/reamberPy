#########
StepMania
#########

********
Examples
********

1. Read and Write
=================

.. code-block::
   :linenos:

    from reamber.sm.SMMapSet import SMMapSet
    sm = SMMapSet.read_file("file.sm")
    sm.write_file("fileOut.sm")

2. Print all Mine Offsets from First Difficulty
===============================================

.. code-block::
   :linenos:

    from reamber.sm.SMMapSet import SMMapSet
    sm = SMMapSet.read_file("file.sm")
    print(sm.maps[0].notes.mines().offset())

3. Swap Col 2 with 3 for First Difficulty
=========================================

.. code-block::
   :linenos:

    from reamber.sm.SMMapSet import SMMapSet
    sm = SMMapSet.read_file("file.sm")
    notes = sm.maps[0].notes  # By reference
    for k, i in notes.data().items():
        for obj in i.data():
            if obj.column == 2:  # Column starts from 0
                obj.column = 3
            elif obj.column == 3:
                obj.column = 2

***********
Module Info
***********

.. toctree::
    Lists <sm/lists>

.. include:: sm/Bpm.inc

.. include:: sm/Fake.inc

.. include:: sm/Hit.inc

.. include:: sm/Hold.inc

.. include:: sm/KeySound.inc

.. include:: sm/Lift.inc

.. include:: sm/Map.inc

.. include:: sm/MapMeta.inc

.. include:: sm/MapSet.inc

.. include:: sm/MapSetMeta.inc

.. include:: sm/Mine.inc

.. include:: sm/Roll.inc

.. include:: sm/Stop.inc

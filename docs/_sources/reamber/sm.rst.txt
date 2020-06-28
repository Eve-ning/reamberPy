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

    from reamber.sm.SMMapSetObj import SMMapSetObj
    sm = SMMapSetObj()
    sm.readFile("file.sm")
    sm.writeFile("fileOut.sm")

2. Print all Mine Offsets from First Difficulty
===============================================

.. code-block::
   :linenos:

    from reamber.sm.SMMapSetObj import SMMapSetObj
    sm = SMMapSetObj()
    sm.readFile("file.sm")
    print(sm.maps[0].notes.mines().offsets())

3. Swap Col 2 with 3 for First Difficulty
=========================================

.. code-block::
   :linenos:

    from reamber.sm.SMMapSetObj import SMMapSetObj
    sm = SMMapSetObj()
    sm.readFile("file.sm")
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

.. include:: sm/BpmObj.inc

.. include:: sm/FakeObj.inc

.. include:: sm/HitObj.inc

.. include:: sm/HoldObj.inc

.. include:: sm/KeySoundObj.inc

.. include:: sm/LiftObj.inc

.. include:: sm/MapObj.inc

.. include:: sm/MapObjMeta.inc

.. include:: sm/MapSetObj.inc

.. include:: sm/MapSetObjMeta.inc

.. include:: sm/MineObj.inc

.. include:: sm/RollObj.inc

.. include:: sm/StopObj.inc

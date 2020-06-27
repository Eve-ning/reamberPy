#########
StepMania
#########

.. code-block::
   :linenos:

    from reamber.sm.SMMapSetObj import SMMapSetObj
    sm = SMMapSetObj()
    sm.readFile("file.sm")
    sm.writeFile("fileOut.sm")

**Note that readFile will not clear previous data, so recreate a obj every time you load another file**

.. code-block::
   :linenos:

    sm = SMMapSetObj()
    sm.readFile("file.sm")
    # sm.readFile("file2.sm") # Don't do this
    # Do this
    sm2 = SMMapSetObj()
    sm2.readFile("file2.sm")

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

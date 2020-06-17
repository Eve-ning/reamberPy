StepMania
=========

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

.. toctree::
    Bpm Object <sm/BpmObj>
    Fake Object <sm/FakeObj>
    Hit Object <sm/HitObj>
    Hold Object <sm/HoldObj>
    KeySound Object <sm/KeySoundObj>
    Lift Object <sm/LiftObj>
    Map Object <sm/MapObj>
    Map Object Metadata <sm/MapObjMeta>
    MapSet Object <sm/MapSetObj>
    MapSet Object Metadata <sm/MapSetObjMeta>
    Mine Object <sm/MineObj>
    Roll Object <sm/RollObj>
    Stop Object <sm/StopObj>
    Lists <sm/lists>

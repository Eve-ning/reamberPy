Osu!
====

We support the osu! file format except for the following:

- Storyboard Elements
- Standard, Catch, Taiko

This package supports most operations for osu! To better understand how

Loading
-------

.. code-block:: python
   :linenos:

    from reamber.osu.OsuMapObj import OsuMapObj

    osu = OsuMapObj()
    osu.readFile("file.osu")
    osu.writeFile("fileOut.osu")

**Note that readFile will not clear previous data, so recreate a obj every time you load another file**

.. code-block:: python
   :linenos:

    osu = OsuMapObj()
    osu.readFile("file.osu")
    # osu.readFile("file2.osu") # Don't do this
    # Do this
    osu2 = OsuMapObj()
    osu2.readFile("file2.osu")

.. toctree::
    Bpm Object <osu/BpmObj>
    Hit Object <osu/HitObj>
    Hold Object <osu/HoldObj>
    Map Object <osu/MapObj>
    Map Object Metadata <osu/MapObjMeta>
    Note Object Metadata <osu/NoteObjMeta>
    Sample Object <osu/SampleObj>
    Sample Sets <osu/SampleSet>
    SV Object <osu/SvObj>
    Timing Point Metadata <osu/TimingPointMeta>
    Lists <osu/lists>
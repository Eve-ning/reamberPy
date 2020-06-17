O2Jam
=============

.. code-block:: python
   :linenos:

    from reamber.o2jam.O2JMapSetObj import O2JMapSetObj
    o2j = O2JMapSetObj()
    o2j.readFile("file.ojn")

**OJM is not supported, hence the following will not be supported.**

- Writing to O2Jam (OJN, OJM)
- Reading OJN
- Reading the Music File
- Exporting to MP3
- Exporting to Keysounds

**Note that readFile will not clear previous data, so recreate a obj every time you load another file**

.. code-block:: python
   :linenos:

    o2j = O2JMapSetObj()
    o2j.readFile("file.ojn")
    # sm.readFile("file2.ojn") # Don't do this
    # Do this
    o2j2 = O2JMapSetObj()
    o2j2.readFile("file2.ojn")

.. toctree::
    Bpm Object <o2jam/BpmObj>
    Hit Object <o2jam/HitObj>
    Hold Object <o2jam/HoldObj>
    Map Object <o2jam/MapObj>
    MapSet Object <o2jam/MapSetObj>
    MapSet Object Metadata <o2jam/MapSetObjMeta>
    Note Object Metadata <o2jam/NoteObjMeta>
    Event Package <o2jam/EventPackage>
    Lists <o2jam/lists>
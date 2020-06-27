#####
O2Jam
#####

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

***********
Module Info
***********

.. toctree::
    Lists <o2jam/lists>

.. include:: o2jam/BpmObj.inc

.. include:: o2jam/HitObj.inc

.. include:: o2jam/HoldObj.inc

.. include:: o2jam/MapObj.inc

.. include:: o2jam/MapSetObj.inc

.. include:: o2jam/MapSetObjMeta.inc

.. include:: o2jam/NoteObjMeta.inc

.. include:: o2jam/EventPackage.inc
Quaver
======

.. code-block:: python
   :linenos:

    from reamber.quaver.QuaMapObj import QuaMapObj

    q = QuaMapObj()
    q.readFile("file.qua")
    q.writeFile("fileOut.qua")

**Note that readFile will not clear previous data, so recreate a obj every time you load another file**

.. code-block:: python
   :linenos:

    qua = QuaMapObj()
    qua.readFile("file.qua")
    # qua.readFile("file2.qua") # Don't do this
    # Do this
    qua2 = QuaMapObj()
    qua2.readFile("file2.qua")

.. toctree::
    Bpm Object <quaver/BpmObj>
    Hit Object <quaver/HitObj>
    Hold Object <quaver/HoldObj>
    Map Object <quaver/MapObj>
    Map Object Metadata <quaver/MapObjMeta>
    Note Object Metadata <quaver/NoteObjMeta>
    SV Object <quaver/SvObj>
    Lists <quaver/lists>
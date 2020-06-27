######
Quaver
######

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

***********
Module Info
***********

.. toctree::
    Lists <quaver/lists>

.. include:: quaver/BpmObj.inc

.. include:: quaver/HitObj.inc

.. include:: quaver/HoldObj.inc

.. include:: quaver/MapObj.inc

.. include:: quaver/MapObjMeta.inc

.. include:: quaver/NoteObjMeta.inc

.. include:: quaver/SvObj.inc

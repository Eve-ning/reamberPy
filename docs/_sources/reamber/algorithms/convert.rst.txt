###########
Conversions
###########

******
Quaver
******

To osu!
=======

.. code-block:: python
   :linenos:

    qua = QuaMapObj()
    qua.readFile("file.qua")
    osu = QuaToOsu.convert(qua)
    osu.writeFile("file.osu")

To SM
=====

.. code-block:: python
   :linenos:

    qua = QuaMapObj()
    qua.readFile("file.qua")
    sm = QuaToSM.convert(qua)
    sm.writeFile("file.sm")

*****
O2Jam
*****

To osu!
=======

.. code-block:: python
   :linenos:

    o2j = O2JMapSetObj()
    o2j.readFile("file.ojn")
    osu = O2JToOsu.convert(o2j)
    osu.writeFile("file.osu")

To Qua
======

.. code-block:: python
   :linenos:

    o2j = O2JMapSetObj()
    o2j.readFile("file.ojn")
    qua = O2JToQua.convert(o2j)
    qua.writeFile("file.qua")

To SM
=====

.. code-block:: python
   :linenos:

    o2j = O2JMapSetObj()
    o2j.readFile("file.ojn")
    sm = O2JToSM.convert(o2j)
    sm.writeFile("file.sm")

*********
StepMania
*********

To osu!
=======

.. code-block:: python
   :linenos:

    sm = SMMapSetObj()
    sm.readFile("file.sm")
    osuMapSet = SMToOsu.convert(sm)
    for i, osuMap in enumerate(osuMapSet):
        osuMap.writeFile(f"fileOut{i}.osu")

- Note that SM files are always mapsets, therefore a conversion will result in a list of `osuMap` s

- I can guarantee the offset will be wrong, fix it manually

To Quaver
=========

.. code-block:: python
   :linenos:

    sm = SMMapSetObj()
    sm.readFile("file.sm")
    quaMapSet = SMToOsu.convert(sm)
    for i, quaMap in enumerate(quaMapSet):
        quaMap.writeFile(f"fileOut{i}.qua")

****
osu!
****

To Stepmania
============

.. code-block:: python
   :linenos:

    osu = OsuMapObj()
    osu.readFile("file.osu")
    sm = OsuToSM.convert(osu)
    sm.writeFile("file.sm", alignBpms=True) # Unless your map only has 1 BPM, always use alignBpms = True

- Note that SM files are always mapsets, this conversion will result in multiple mapsets regardless

- I can guarantee the offset will be wrong, fix it manually

To Quaver
=========

.. code-block:: python
   :linenos:

    osu = OsuMapObj()
    osu.readFile("file.osu")
    qua = OsuToQua.convert(osu)
    qua.writeFile("file.qua")

*****
Annex
*****

These are FYI, if it doesn't make sense, it's normal.

BEAT_ERROR_THRESHOLD
====================

- For your knowledge, don't change unless you know what is going on.

Default = 5.0

This the amount of beats searched before the current misaligned BPM to check for an existing BPM to amend instead of append.

BEAT_CORRECTION_FACTOR
======================

- For your knowledge, don't change unless you know what is going on.

Default = 0.001

This is the largest amount of positive beat error before an append happens.

***********
Module Info
***********

.. include:: convert/O2JToOsu.inc

.. include:: convert/O2JToQua.inc

.. include:: convert/O2JToSM.inc

.. include:: convert/OsuToQua.inc

.. include:: convert/OsuToSM.inc

.. include:: convert/QuaToOsu.inc

.. include:: convert/QuaToSM.inc

.. include:: convert/SMToOsu.inc

.. include:: convert/SMToQua.inc

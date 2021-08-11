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

    qua = QuaMap.read_file("file.qua")
    osu = QuaToOsu.convert(qua)
    osu.write_file("file.osu")

To SM
=====

.. code-block:: python
   :linenos:

    qua = QuaMap.read_file("file.qua")
    sm = QuaToSM.convert(qua)
    sm.write_file("file.sm")

*****
O2Jam
*****

To osu!
=======

.. code-block:: python
   :linenos:

    o2j = O2JMapSet.read_file("file.ojn")
    osu = O2JToOsu.convert(o2j)
    osu.write_file("file.osu")

To Qua
======

.. code-block:: python
   :linenos:

    o2j = O2JMapSet.read_file("file.ojn")
    qua = O2JToQua.convert(o2j)
    qua.write_file("file.qua")

To SM
=====

.. code-block:: python
   :linenos:

    o2j = O2JMapSet.read_file("file.ojn")
    sm = O2JToSM.convert(o2j)
    sm.write_file("file.sm")

*********
StepMania
*********

To osu!
=======

.. code-block:: python
   :linenos:

    sm = SMMapSet.read_file("file.sm")
    osuMapSet = SMToOsu.convert(sm)
    for i, osuMap in enumerate(osuMapSet):
        osuMap.write_file(f"fileOut{i}.osu")

- Note that SM files are always mapsets, therefore a conversion will result in a list of `osuMap` s

- I can guarantee the offset will be wrong, fix it manually

To Quaver
=========

.. code-block:: python
   :linenos:

    sm = SMMapSet.read_file("file.sm")
    quaMapSet = SMToOsu.convert(sm)
    for i, quaMap in enumerate(quaMapSet):
        quaMap.write_file(f"fileOut{i}.qua")

****
osu!
****

To Stepmania
============

.. code-block:: python
   :linenos:

    osu = OsuMap.read_file("file.osu")
    sm = OsuToSM.convert(osu)
    sm.write_file("file.sm", align_bpms=True) # Unless your map only has 1 BPM, always use align_bpms = True

- Note that SM files are always mapsets, this conversion will result in multiple mapsets regardless

- I can guarantee the offset will be wrong, fix it manually

To Quaver
=========

.. code-block:: python
   :linenos:

    osu = OsuMap.read_file("file.osu")
    qua = OsuToQua.convert(osu)
    qua.write_file("file.qua")

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

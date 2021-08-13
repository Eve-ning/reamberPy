###########
Conversions
###########

******
Syntax
******

The syntax is always consistent.

.. code-block::

    from_map = From.read_file("path/to/file_from")
    to_map = FromToTo.convert(from_map)
    to_map.write_file("path/to/file_to")

For example, if you want to convert Quaver to SM

.. code-block:: python

    qua = QuaMap.read_file("file.qua")
    sm = QuaToSM.convert(qua)
    sm.write_file("file.sm")

******************
Syntax for Mapsets
******************

Some map types are mapsets, such as StepMania, where each ``.sm`` is a mapset, which may contain multiple or one map.

For example, if you want to convert a SM Mapset to a Osu Map.

.. code-block:: python

    sm = SMMapSet.read_file("file.sm")
    osus = SMToOsu.convert(sm)
    for i, osu in enumerate(osus):
        osu.write_file(f"fileOut{i}.osu")

By convention, if a map is a mapset, we just call it ``<map>s``. Where ``SMMapset`` is ``sms`` if ``SMMap`` is ``sm``.

*************
Special Cases
*************

Most conversions will yield a bad offset, please do check them.

If you're unsure if it yields multiple maps, or just one, please consider using the type-hinting in the IDE.

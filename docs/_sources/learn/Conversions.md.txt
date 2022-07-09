# Conversions

## Syntax

The syntax is always consistent.

```
from_map = <FROM>.read_file("path/to/file_from")
to_map = <FROM>To<TARGET>.convert(from_map)
to_map.write_file("path/to/file_to")
```
For example, if you want to convert Quaver to SM

```py
from reamber.quaver.QuaMap import QuaMap
from reamber.algorithms.convert import QuaToSM
qua = QuaMap.read_file("file.qua")
sm = QuaToSM.convert(qua)
sm.write_file("file.sm")
```

## Syntax for Mapsets

For mapsets, such as StepMania

```py
from reamber.sm.SMMapSet import SMMapSet
from reamber.algorithms.convert import SMToOsu
sm = SMMapSet.read_file("file.sm")
osus = SMToOsu.convert(sm)
for i, osu in enumerate(osus):
    osu.write_file(f"fileOut{i}.osu")
```

By convention, if a map is a mapset. We name it ``<map>s``. 

Where ``SMMapset`` is ``sms`` if ``SMMap`` is ``sm``.

## Special Cases

Most conversions will yield a bad offset, please do check them.

If you're unsure if it yields multiple maps, or just one, consider using the type-hinting in the IDE.

# Play Field

## Recipes

### Osu

```py
from reamber.osu.OsuMap import OsuMap
from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import *

m = OsuMap.read_file("path/to/file.osu")
pf = PlayField(m, padding=70)\
     + PFDrawColumnLines()\
     + PFDrawBeatLines()\
     + PFDrawBpm(xOffset=30, yOffset=0)\
     + PFDrawSv(yOffset=0)\
     + PFDrawNotes()
pf.export_fold(maxHeight=1000).save("osu.png")
```

### SM

```py
from reamber.sm.SMMapSet import SMMapSet
from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import *

s = SMMapSet.read_file("path/to/file.sm")
pf = PlayField(s.maps[0])\
     + PFDrawBeatLines([1])\
     + PFDrawNotes()
pf.export_fold(maxHeight=2000).save("sm.png")
```

### Quaver

```py
from reamber.quaver.QuaMap import QuaMap
from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import *

m = QuaMap.read_file("path/to/file.qua")
pf = PlayField(m)\
     + PFDrawColumnLines()\
     + PFDrawBeatLines([1,3,6])\
     + PFDrawNotes()
pf.export_fold(maxHeight=2000).save("qua.png")
```

### O2Jam

```py
from reamber.o2jam.O2JMapSet import O2JMapSet
from reamber.algorithms.playField import PlayField
from reamber.algorithms.playField.parts import *

s = O2JMapSet.read_file("path/to/file.ojn")
pf = PlayField(s.maps[2], padding=40)\
     + PFDrawColumnLines()\
     + PFDrawBeatLines([1])\
     + PFDrawBpm()\
     + PFDrawNotes()
pf.export_fold(maxHeight=2000).save("o2j.png")
```

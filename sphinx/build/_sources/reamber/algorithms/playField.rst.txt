##########
Play Field
##########

.. toctree::
    Parts <playField/parts>

***********
Example Osu
***********

.. code-block:: python

    from reamber.osu.OsuMap import OsuMap
    from reamber.algorithms.playField import PlayField
    from reamber.algorithms.playField.parts import *

    m = OsuMap()
    m.readFile("path/to/file.osu")
    pf = PlayField(m, padding=70)\
         + PFDrawColumnLines()\
         + PFDrawBeatLines()\
         + PFDrawBpm(xOffset=30, yOffset=0)\
         + PFDrawSv(yOffset=0)\
         + PFDrawNotes()
    pf.exportFold(maxHeight=1000).save("osu.png")

**********
Example SM
**********

.. code-block:: python

    from reamber.sm.SMMapSet import SMMapSet
    from reamber.algorithms.playField import PlayField
    from reamber.algorithms.playField.parts import *

    s = SMMapSet()
    s.readFile("path/to/file.sm")
    pf = PlayField(s.maps[0])\
         + PFDrawBeatLines([1])\
         + PFDrawNotes()
    pf.exportFold(maxHeight=2000).save("sm.png")

**************
Example Quaver
**************

.. code-block:: python

    from reamber.quaver.QuaMap import QuaMap
    from reamber.algorithms.playField import PlayField
    from reamber.algorithms.playField.parts import *

    m = QuaMap()
    m.readFile("path/to/file.qua")
    pf = PlayField(m)\
         + PFDrawColumnLines()\
         + PFDrawBeatLines([1,3,6])\
         + PFDrawNotes()
    pf.exportFold(maxHeight=2000).save("qua.png")

*************
Example O2Jam
*************

.. code-block:: python

    from reamber.o2jam.O2JMapSet import O2JMapSet
    from reamber.algorithms.playField import PlayField
    from reamber.algorithms.playField.parts import *

    s = O2JMapSet()
    s.readFile("path/to/file.ojn")
    pf = PlayField(s.maps[2], padding=40)\
         + PFDrawColumnLines()\
         + PFDrawBeatLines([1])\
         + PFDrawBpm()\
         + PFDrawNotes()
    pf.exportFold(maxHeight=2000).save("o2j.png")


***********
Module Info
***********

.. include:: playField/PlayField.inc

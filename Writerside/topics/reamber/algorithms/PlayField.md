# Play Field

<tldr>
    <p><code>PlayField</code> generates an image from a map.</p>
</tldr>

![PlayFieldImg.png](PlayFieldImg.png)

The `playField` implements image layers: notes, column lines, etc. separately.

This means you can pick & choose the elements to include

- `PFDrawBpm()`
- `PFDrawBeatLines()`
- `PFDrawColumnLines()`
- `PFDrawNotes()`
- `PFDrawOffsets()`

## Usage

Firstly initialize the `PlayField` with a map

```python
from reamber.algorithms.playField import PlayField
from reamber.osu.OsuMap import OsuMap

m = OsuMap.read_file("...")

pf = PlayField(m=m, duration_per_px=5, padding=40) 
```

Then, **add** layers on top of it

```python
pf = (
    PlayField(m=m, duration_per_px=5, padding=40) +
    PFDrawBpm() +
    PFDrawBeatLines() +
    PFDrawColumnLines() +
    PFDrawNotes() +
    PFDrawOffsets()
)
```

Finally, once you're done, export it as an image.

```python
pf.export_fold(max_height=2000).save("saved_img.png")
```

- `export_fold` folds the image, so that it's not an extremely long image.
- `export` exports as is.

## Recipes

<tabs>
    <tab title="osu!mania">
        <code-block lang="python">
        from reamber.osu.OsuMap import OsuMap
        from reamber.algorithms.playField import PlayField
        from reamber.algorithms.playField.parts import *&#xA;
        m = OsuMap.read_file(&quot;path/to/file.osu&quot;)
        pf = (
        PlayField(m, padding=70)
        + PFDrawColumnLines()
          + PFDrawBeatLines()
          + PFDrawBpm(x_offset=30, y_offset=0)
          + PFDrawSv(y_offset=0)
          + PFDrawNotes()
          ) 
        pf.export_fold(maxHeight=1000).save(&quot;osu.png&quot;)
        </code-block>
    </tab>
    <tab title="StepMania">
        <code-block lang="python">
        from reamber.sm.SMMapSet import SMMapSet
        from reamber.algorithms.playField import PlayField
        from reamber.algorithms.playField.parts import *&#xA;
        s = SMMapSet.read_file(&quot;path/to/file.sm&quot;)
        pf = (
        PlayField(s.maps[0])
        + PFDrawBeatLines([1])
          + PFDrawNotes()
          )
        pf.export_fold(max_height=2000).save(&quot;sm.png&quot;)
        </code-block>
    </tab>
    <tab title="Quaver">
        <code-block lang="python">
        from reamber.quaver.QuaMap import QuaMap
        from reamber.algorithms.playField import PlayField
        from reamber.algorithms.playField.parts import *&#xA;
        m = QuaMap.read_file(&quot;path/to/file.qua&quot;)
        pf = (
        PlayField(m)
        + PFDrawColumnLines()
          + PFDrawBeatLines([1, 3, 6])
          + PFDrawNotes()
          )
        pf.export_fold(max_height=2000).save(&quot;qua.png&quot;)
        </code-block>
    </tab>
    <tab title="O2Jam">
        <code-block lang="python">
        from reamber.o2jam.O2JMapSet import O2JMapSet
        from reamber.algorithms.playField import PlayField
        from reamber.algorithms.playField.parts import *&#xA;
        s = O2JMapSet.read_file(&quot;path/to/file.ojn&quot;)
        pf = (
        PlayField(s.maps[2], padding=40)
        + PFDrawColumnLines()
          + PFDrawBeatLines([1])
          + PFDrawBpm()
          + PFDrawNotes()
          )
        pf.export_fold(max_height=2000).save(&quot;o2j.png&quot;)
        </code-block>
    </tab>
</tabs>


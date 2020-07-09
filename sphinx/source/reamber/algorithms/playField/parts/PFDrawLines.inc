Play Field Draw Lines
=====================

Pattern API
-----------

Understanding this fully requires knowledge about the **Pattern** package.

**Input**

We firstly group by ``hits`` and ``holds`` of the read osu map with a **Vertical Window** of 50.

Using that group, we construct lines for **Chordstreams**.

The first chordstream template looks for all pairs that are ``[3, 2], [2, 3], [2, 2], [2, 1], [1, 2], [1, 1]``::

    PFDrawLines.templateChordStream(primary=3, secondary=2, ...)

The second one looks for all pairs that are ``[2, 1], [1, 2], [1, 1]``::

    PFDrawLines.templateChordStream(primary=2, secondary=1, ...)

The third locates all jacks that are at least a minimum length of 2 (all jacks in other words)::

    PFDrawLines.templateJacks(minimumLength=2, ...)

Note that the chordstream template will not look for jacks unless specifically stated.

The last line folds the image so that it's more squary then saves it as ``osu.png``::

    pf.exportFold(maxHeight=1750, stageLineWidth=0).save("osu.png")

.. code-block::python
    :linenos:

    from reamber.osu.OsuMap import OsuMap
    from reamber.algorithms.playField import PlayField
    from reamber.algorithms.playField.parts import *
    from reamber.algorithms.pattern.Pattern import Pattern

    osu = OsuMap()
    osu.readFile("path/to/file.osu")

    ptn = Pattern.fromPkg([osu.notes.hits(), osu.notes.holds()])
    grp = ptn.group(hwindow=None, vwindow=50, avoidJack=True)

    key = osu.notes.maxColumn() + 1

    pf = PlayField(m=osu, durationPerPx=5) \
         + PFDrawLines.templateChordStream(primary=3,
                                           secondary=2,
                                           keys=keys,
                                           groups=grp,
                                           **PFDrawLines.Colors.BLUE, fromWidth=3) \
         + PFDrawLines.templateChordStream(primary=2,
                                           secondary=1,
                                           keys=keys,
                                           groups=grp,
                                           **PFDrawLines.Colors.PURPLE, fromWidth=3) \
         + PFDrawLines.templateJacks(minimumLength=2,
                                     keys=keys,
                                     groups=grp,
                                     **PFDrawLines.Colors.RED, fromWidth=2)

    pf.exportFold(maxHeight=1750, stageLineWidth=0).save("osu.png")



.. automodule:: reamber.algorithms.playField.parts.PFDrawLines




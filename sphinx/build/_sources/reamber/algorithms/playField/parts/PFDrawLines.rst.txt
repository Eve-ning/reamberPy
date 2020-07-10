#####################
Play Field Draw Lines
#####################

***********
Pattern API
***********

Understanding this fully requires knowledge about the **Pattern** package.

I added a 2 templates to easily generate the filters, however you can create filters of your own. Instructions are in
the ``combinations`` **docstring**.

**Input**

.. code-block:: python
    :linenos:

    from reamber.osu.OsuMap import OsuMap
    from reamber.algorithms.playField import PlayField
    from reamber.algorithms.playField.parts import *
    from reamber.algorithms.pattern.Pattern import Pattern

    osu = OsuMap()
    osu.readFile(OSU_BOOGIE)

    ptn = Pattern.fromPkg([osu.notes.hits(), osu.notes.holds()])
    grp = ptn.group(hwindow=None, vwindow=50, avoidJack=True)

    keys = osu.notes.maxColumn() + 1

    pf = PlayField(m=osu, durationPerPx=5) \
         + PFDrawLines.fromCombo(keys=keys, **PFDrawLines.Colors.RED,
        combo=PtnCombo(grp).templateChordStream(primary=3, secondary=2, keys=keys, andLower=True)) \
         + PFDrawLines.fromCombo(keys=keys, **PFDrawLines.Colors.BLUE,
        combo=PtnCombo(grp).templateChordStream(primary=2, secondary=1, keys=keys, andLower=True)) \
         + PFDrawLines.fromCombo(keys=keys, **PFDrawLines.Colors.PURPLE,
        combo=PtnCombo(grp).templateJacks(minimumLength=2, keys=keys))

    pf.exportFold(maxHeight=1750, stageLineWidth=0).save("osu.png")

We firstly group by ``hits`` and ``holds`` of the read osu map with a **Vertical Window** of 50.

Using that group, we construct lines for **Chordstreams**.

The first chordstream template looks for all pairs that are ``[3, 2], [2, 3], [2, 2], [2, 1], [1, 2], [1, 1]``::

    PFDrawLines.fromCombo(...,
        combo=PtnCombo(grp).templateChordStream(primary=3, secondary=2, keys=keys, andLower=True))

The second one looks for all pairs that are ``[2, 1], [1, 2], [1, 1]``::

    PFDrawLines.fromCombo(...,
        combo=PtnCombo(grp).templateChordStream(primary=2, secondary=1, keys=keys, andLower=True))

The third locates all jacks that are at least a minimum length of 2 (all jacks in other words)::

    PFDrawLines.fromCombo(..., combo=PtnCombo(grp).templateJacks(minimumLength=2, keys=keys))

Note that the chordstream template will not look for jacks unless specifically stated.

The last line folds the image so that it's more squary then saves it as ``osu.png``::

    pf.exportFold(maxHeight=1750, stageLineWidth=0).save("osu.png")

Template Chord Stream
=====================

The underlying algorithm uses this lower-level interface. This part requires knowledge about how ``PtnFilter``
creates its filter.

.. code-block:: python
    :linenos:

    combo = Pattern.combinations(...,
        chordFilter=PtnFilterChord.create(
            [[primary, secondary]], keys=keys,
            method=PtnFilterChord.Method.ANY_ORDER | PtnFilterChord.Method.AND_LOWER if andLower else 0,
            invertFilter=False).filter,
        comboFilter=PtnFilterCombo.create(
            [[0, 0]], keys=keys,
            method=PtnFilterCombo.Method.REPEAT,
            invertFilter=True).filter if not includeJack else None,
        typeFilter=PtnFilterType.create(
            [[HoldTail, object]],
            method=PtnFilterType.Method.ANY_ORDER,
            invertFilter=True).filter)

As you can see here, we define the detection to be ``size=2``, so it only looks for pairs.

The ``chordFilter`` will filter **in** anything that matches the ``primary`` and ``secondary`` parameters and below. (
this is made possible by the ``PtnFilterChord.Method.AND_LOWER`` argument.)

The ``comboFilter`` excludes any jacks. ``[0, 0], [1, 1], ...`` is rejected. (Using the ``invertFilter=True`` argument.)

the ``typeFilter`` excludes the ``HoldTail`` being included in any pair. (Using the ``invertFilter=True`` argument.)

Template Jacks
==============

.. code-block:: python
    :linenos:

    combo = Pattern.combinations(...,
        comboFilter=PtnFilterCombo.create(
            [[0] * minimumLength], keys=keys,
            method=PtnFilterCombo.Method.REPEAT,
            invertFilter=False).filter,
        typeFilter=PtnFilterType.create(
            [[HoldTail, object]],
            method=PtnFilterType.Method.ANY_ORDER,
            invertFilter=True).filter)

The ``comboFilter`` include any jacks. ``[0, 0], [1, 1], ...`` is accepted.

the ``typeFilter`` excludes the ``HoldTail`` being included in any pair. (Using the ``invertFilter=True`` argument.)

***********
Module Info
***********

.. automodule:: reamber.algorithms.playField.parts.PFDrawLines




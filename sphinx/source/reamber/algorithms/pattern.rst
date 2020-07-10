#################
Pattern Detection
#################

The aim of this package is to ease the way to find occurrence of specific patterns. See PtnCombo on how to detect
patterns/combinations after grouping.

**Input**

The ``Pattern.__init__()`` takes in ``cols: List[int], offsets: List[float], types: List[Type]``. However if you are
using ``Map`` objects, you can extract from the ``NoteList``s with ``fromPkg`` like such.

.. code-block:: python

    osu = OsuMap()
    osu.readFile("path/to/file.osu")

    Pattern.fromPkg(osu.notes.hits() + osu.notes.holds())

This initializes the class with required lists for you to use ``group()``

********
Grouping
********

The grouping algorithm looks at every note and tries to group them with other notes according to conditions specified.

All details can be found in the module info at the bottom. It will show examples on how it's done


You could directly use groups for your own packages or pivot off these other sub-packages.

.. toctree::
    Pattern Combinations <pattern/PtnCombo>
    Pattern Filters <pattern/PtnFilter>

Module Info
-----------

.. automodule:: reamber.algorithms.pattern.Pattern


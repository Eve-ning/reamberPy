################
Development Info
################

This article outlines the crucial parts of how reamberPy works behind the scenes.

.. toctree::
    :maxdepth: 1

    Type Hinting <TypeHinting>
    Properties <Props>

******
Basics
******

The package uses a common foundation, called ``base``, that all other VSRGs stem from.

In other words, ``OsuMap`` inherits from ``base.Map`` class, so the inherited methods propagate forward.

Base
====

Base contains a few **item** classes

- ``Timed``
- ``Bpm``
- ``Note``
- ``Hit``
- ``Hold``

These are different from the **item list** classes

- ``TimedList``
- ``BpmList``
- ``NoteList``
- ``HitList``
- ``HoldList``

The reason for separating them is so that we can custom implement list methods that Python ``list`` class does not
provide.

**Each Item** uses a ``pd.Series``. **Each List** uses a ``pd.DataFrame``.

``Item.data`` will yield a ``pd.Series``.

``ItemList.df`` will yield a ``pd.DataFrame``.

We use ``pd`` because it helps in optimization and provides abundant functionalities to extend from.

Item Structure
==============

**Bolded** elements are new properties introduced in the child class.

Timed
-----

Props: **offset**

Note(Timed)
-----------

Props: **column**, offset

Hit(Note)
---------

Props: column, offset

Hold(Note)
----------

Props: **length**, column, offset

Bpm(Timed)
----------

Props: **bpm**, **metronome**, offset

Item List Structure
===================

For each corresponding **Item**, there is its list part, which provides additional functionality

- ``TimedList``
- ``NoteList(TimedList)``
- ``HitList(NoteList)``
- ``HoldList(NoteList)``
- ``BpmList(TimedList)``

Map Structure
=============

Every map is a ``@dataclass``.

For each map, it has an ``objs`` dictionary of ``TimedList`` children. This is the default.

.. code-block:: python

    objs = dict(hits=HitList([]), holds=HoldList([]), bpms=BpmList([]))

In other words, it always initializes with these classes, but inheriting classes can override ``objs``.

Overriding updates the classes, where it should opt for ``OsuHoldList`` instead of ``HoldList``.

MapSet Structure
================

A ``MapSet`` is simply a list of ``Map`` s.

.. code-block:: python

    maps = []


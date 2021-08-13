###############
Getting Started
###############

**Installation**

If you haven't installed reamber you can just run

``pip install reamber``

in your terminal

************
Requirements
************

If pip doesn't install extra dependencies for you, you also require these libraries.

- Python >=3.7
- numpy - For common mathematical operations and the numpy.Series
- pyyaml - To handle Quaver files easily
- pandas - To facilitate some algorithms and allow conversion to pandas.DataFrame
- matplotlib - To allow plotting on some algorithms (e.g. nps_plot)
- pillow - To enable drawing on some algorithms (e.g. PlayField)

***************
Recommendations
***************

Most Python IDEs should have auto-fill for accessible methods and properties. I highly recommend using those to boost
your productivity.

This library is made that in mind, so most things should be easy to auto-fill :)

***********
Conventions
***********

There are important conventions to note due to different games having different terms. This package will consistently
apply the same terms to all games.

**Note Object**: This means all playable objects, inclusive of Hit, Hold, Mine, Roll, etc.

**Hit Object**: This means any note that is just a single tap.

**Bpm Point/Object**: These are aliases.

**Map/Map Set**: A Map Set contains a list of Maps.
Some games will put multiple maps in a single file, hence they will load as a Mapset instead of a Map.

********
Examples
********

Loading a map file is simple, note that you **cannot** load it with ``OsuMap("file.osu")`` due to underlying design
issues.

Note that ``read_file`` will read a file, ``read`` is reserved for string inputs only.

Loading a Map
=============

.. code-block:: python

   from reamber.osu.OsuMap import OsuMap

   m = OsuMap.read_file("path/to/file.osu")

Loading a Mapset
================

Sometimes a game will put multiple maps in a single file, hence you get a mapset.
Here's how to grab maps from a set.

.. code-block:: python

   from reamber.sm.SMMapSet import SMMapSet

   sms = SMMapSet.read_file("path/to/file.sm")

   sm = sms[0]

Grabbing Properties
===================

All maps are guaranteed to have 3 core properties:

- Hit Objects
- Hold Objects
- Bpm Objects

Depending on the map type, you can grab different properties, it'll show up on auto-fill on most modern IDEs.

**Example: Get the first 5 hit offset in the file**

*input:*

.. code-block:: python

   from reamber.osu.OsuMap import OsuMap

   m = OsuMap.read_file("path/to/file.osu")

   print(m.hits.offset[:5])

*output:*

.. code-block::

   [4113, 4113, 4142, 4200, 4631]

   Process finished with exit code 0

Converting
==========

Almost all games here have conversions.

**Example: Read a osu file and export as a quaver file**

*input:*

.. code-block:: python

   from reamber.osu.OsuMap import OsuMap
   from reamber.algorithms.convert.OsuToQua import OsuToQua

   m = OsuMap.read_file("path/to/file.osu")

   qua = OsuToQua.convert(m)
   qua.write_file("out.qua")


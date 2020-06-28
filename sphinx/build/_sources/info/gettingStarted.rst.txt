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
- matplotlib - To allow plotting on some algorithms (e.g. npsPlot)
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

**Package**: This means a class that holds multiple lists.

**Map/Map Set**: A Map Set contains a list of Maps.
Some games will put multiple maps in a single file, hence they will load as a Mapset instead of a Map.

********
Examples
********

**Note 1: Example files can be found in the /rsc/maps/ folder, you may need to download it locally**

**Note 2: Most examples work with all types of maps, however, we'll mostly use osu! since it's popular.**

Loading a map file is simple, note that you **cannot** load it with ``OsuMapObj("file.osu")`` due to underlying design
issues.

Loading a Map
=============

.. code-block:: python
   :linenos:

   from reamber.osu.OsuMapObj import OsuMapObj

   m = OsuMapObj()
   m.readFile("path/to/file.osu")

Loading a Mapset
================

Sometimes a game will put multiple maps in a single file, hence you get a mapset.
Here's how to grab maps from a set.

.. code-block:: python
   :linenos:

   from reamber.sm.SMMapSetObj import SMMapSetObj

   s = SMMapSetObj()
   s.readFile("path/to/file.sm")

   m_0 = s.maps[0]

Grabbing Properties
===================

All maps are guaranteed to have 2 core properties:

- Note Objects
- Bpm Objects

Depending on the map type, you can grab different properties, it'll show up on auto-fill on most modern IDEs.

**Example: Get the first 5 hit offsets in the file**

*input:*

.. code-block:: python
   :linenos:

   from reamber.osu.OsuMapObj import OsuMapObj

   m = OsuMapObj()
   m.readFile("path/to/file.osu")

   print(m.notes.hits().offsets()[:5])

*output:*

.. code-block::
   :linenos:

   [4113, 4113, 4142, 4200, 4631]

   Process finished with exit code 0

Converting
==========

Almost all games here have conversions.

**Example: Read a osu file and export as a quaver file**

*input:*

.. code-block:: python
   :linenos:

   from reamber.osu.OsuMapObj import OsuMapObj
   from reamber.algorithms.convert.OsuToQua import OsuToQua

   m = OsuMapObj()
   m.readFile("path/to/file.osu")

   qua = OsuToQua.convert(m)
   qua.writeFile("out.qua")

Algorithms
==========

There are lots of algorithms to use to quickly perform certain operations.

**Example: Using a custom algorithm, describe**

*input:*

.. code-block:: python
   :linenos:

   from reamber.osu.OsuMapObj import OsuMapObj
   from reamber.algorithms.analysis.describe.describe import describe

   m = OsuMapObj()
   m.readFile("path/to/file.osu")

   describe(m)

*output:*

.. code-block::
   :linenos:

   Average BPM: 174.0
   Map Length: 0:08:07.931000
   Camellia - Looking for Edge of Ground, System.NullReferenceExceptionExtend (Evening)
   ==== NPS ====
   All:  Count: 7871, 50% (Median): 15.00, 75%: 18.00, 100% (Max): 28.00
   Col0: Count: 2026, 50% (Median): 5.00, 75%: 6.00, 100% (Max): 9.00
   Col1: Count: 1930, 50% (Median): 6.00, 75%: 7.00, 100% (Max): 9.00
   Col2: Count: 2069, 50% (Median): 6.00, 75%: 7.00, 100% (Max): 10.00
   Col3: Count: 1846, 50% (Median): 6.00, 75%: 6.00, 100% (Max): 10.00

   Process finished with exit code 0

*************
Going Further
*************

There are many algorithms that you can use to perform analysis on. You can look through the rest of the pages to
find other algorithms provided.

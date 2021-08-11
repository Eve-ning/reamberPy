########
Stacking
########

**Stacking is Joining All DataFrames together regardless of type.**

If you're not familiar with `pd.DataFrame`, it's good to take a look at how it represent 2D Data.

*******
Example
*******

An example of a Hit List::

   offset column
   1000   2
   2000   3
   4000   1

An example of a Hold List::

   offset column length
   1000   3      100
   2000   2      200
   3500   3      500

An example of a Bpm List::

   offset bpm metronome
   1000   200 4

If we stacked them, we yield::

   offset column length bpm metronome
   1000   3      100
   2000   2      200
   3500   3      500
   1000   2
   2000   3
   4000   1
   1000                 200 4

This allows us to modify all matching properties at one go. Note that empty cells are `NaN`.

If you're familiar with `pd.DataFrame`, the operations work similar here.

Here's how to use stack to add offset to everything.

.. code-block:: python

   from reamber.osu.OsuMap import OsuMap

   m = OsuMap.read_file("path/to/file.osu")
   stack = m.stack

   stack.offset += 1000

   m.write_file("path/to/out.osu")

**********
Properties
**********

Generally, if there exists a property, then it'll be included via the type-hint provided by your IDE.

For example, if your map has SVs, then `m.stack.multiplier` should be a valid call.

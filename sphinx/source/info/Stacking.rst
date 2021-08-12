########
Stacking
########

**Stacking is Joining All DataFrames together regardless of type.**

If you're not familiar with `pd.DataFrame`, it's good to take a look at how it represent 2D Data.

*******
Example
*******

An example of a Hit List::

   offset | column
   1000   | 2
   2000   | 3
   4000   | 1

An example of a Hold List::

   offset | column | length
   1000   | 3      | 100
   2000   | 2      | 200
   3500   | 3      | 500

An example of a Bpm List::

   offset | bpm | metronome
   1000   | 200 | 4

If we stacked them, we yield::

   offset | column | length | bpm | metronome
   1000   | 3      | 100    |     |
   2000   | 2      | 200    |     |
   3500   | 3      | 500    |     |
   1000   | 2      |        |     |
   2000   | 3      |        |     |
   4000   | 1      |        |     |
   1000   |        |        | 200 | 4

This allows us to modify all matching properties at one go. Note that empty cells are `NaN`.

If you're familiar with `pd.DataFrame`, basic operations such as `+=`, `/=` work here.

Here's how to use stack to add offset to everything.

.. code-block:: python

   from reamber.osu.OsuMap import OsuMap

   m = OsuMap.read_file("path/to/file.osu")
   stack = m.stack()

   stack.offset += 1000

   m.write_file("path/to/out.osu")

**********
Properties
**********

Generally, if there exists a property, then it'll be included via the type-hint provided by your IDE.

For example, if your map has SVs, then `m.stack().multiplier` should be a valid call.

********************
Conditional Stacking
********************

If you're familiar with `pd.DataFrame`, you can do something like

.. code-block:: python

    df.loc[df.offset < 1000, 'column'] += 1

This adds column by 1 where ``df.offset`` is less than 1000.

For stacking, you can, and **MUST** do it similarly.

.. code-block:: python

    stack = m.stack()
    stack.loc[stack.offset < 1000, 'column'] += 1

Note that the following is **invalid**

.. code-block:: python

    stack = m.stack()
    stack.column[stack.offset < 1000] += 1

This will throw a ``SettingWithCopy`` warning! This means, it might not have updated the ``stack`` by reference.

=======================
SettingWithCopy Warning
=======================

*If you're running into this issue, see above.*

`This is due to chained indexing <https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy>`_

In short, when we write

.. code-block:: python

    stack = m.stack()
    stack.column

It expands to

.. code-block:: python

    stack = m.stack()
    stack_copy = stack.__getitem__('column')
    stack_copy[stack.offset < 1000] += 1

Notice that ``stack_copy`` may or may not be a copy, thus, it may not update the ``stack``.


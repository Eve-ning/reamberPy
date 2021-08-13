##########
Properties
##########

reamberPy uses decorators that create "properties", I will explain its process and uses here.

******
Basics
******

As outlined in the :doc:`Development Info <DevInfo>`, most objects use a ``pd.Series`` or ``pd.DataFrame`` data source.

Note that you get its columns with attributes and indexing.

.. code-block:: python

    srs: pd.Series
    srs.offset == srs['offset']

    df: pd.DataFrame
    df.offset == df['offset']

This is crucial in creating decorators to index these as **properties**

==========
Why Pandas
==========

Pandas is an extension of NumPy with useful column-based operations, suitable for this. While I could've customized my
own library, it'll be too much of a liability of maintenance.

It provides excellent functions, on top of its indexing, with good performance on correct usage.

====================
Item Prop Decorators
====================

The custom ``Property`` decorators grabs the class' attribute ``_props`` and generates useful functions.

For example

.. code-block:: python

    @item_props()
    class OsuSv(OsuTimingPointMeta, Timed):

        _props = dict(multiplier=['float', 1.0])

In this case ``@item_props()`` grabs ``_props`` and generates the following functions

.. code-block:: python

    class OsuSv(OsuTimingPointMeta, Timed):
        @property
        def multiplier(self) -> pd.Series:
            return self.data['multiplier']
        @multiplier.setter
        def multiplier(self, val) -> None:
            self.data[k_] = val

Looking at ``OsuSv.pyi``, you can see the stub implementations, which type hints these without its body.

.. code-block:: python

    class OsuSv(OsuTimingPointMeta, Timed):
        @property
        def multiplier(self) -> pd.Series: ...
        @multiplier.setter
        def multiplier(self, val) -> None: ...

====================
List Prop Decorators
====================

Similar to Item Prop Decorators, this affects lists

For example,

.. code-block:: python

    from reamber.osu.OsuSv import OsuSv

    @list_props(OsuSv)
    class OsuSvList(TimedList[OsuSv]):
        ...

This doesn't require ``_props`` as it extracts from ``OsuSv``.

It will generate the following class.

.. code-block:: python

    from reamber.osu.OsuSv import OsuSv
    class OsuSvList(TimedList[OsuSv]):

        @property
        def multiplier(self) -> pd.Series:
            return self.df['multiplier']
        @multiplier.setter
        def multiplier(self, val) -> None:
            self.df['multiplier'] = val

Without meta-programming decorators, this would have caused many consistency issues.

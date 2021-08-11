Hit Sound Copy
--------------

Visualization
^^^^^^^^^^^^^

::

    e.g. < (C)lap (F)inish (W)histle >

    C F W  Vol | == Copier ==> | C F W  Vol
    1 0 0  20  | == Copier ==> | 1 1 1  20
    0 1 0  20  | == Copier ==> | 1 0 0  30
    0 0 1  20  | == Copier ==> | 0 1 1  40
    1 0 0  30  | == Copier ==> | CUSTOM 20
    0 1 1  40  | == Copier ==> |
    CUSTOM 20  | == Copier ==> |

Example
^^^^^^^

*you can import logging to get an event log on what happens during copying*


.. code-block:: python
   :linenos:

    import logging
    logging.basicConfig(filename="event.log", filemode="w+", level=logging.DEBUG)

    from reamber.osu.OsuMap import OsuMap
    from reamber.algorithms.mutate.hitSoundCopy import hitsound_copy

    mFrom = OsuMap.read_file("hitsound.osu")

    mTo = OsuMap.read_file("hitsoundable.osu")

    mOut = hitsound_copy(mFrom=mFrom, mTo=mTo)

    mOut.write_file("fileOut.osu")


- Note that if you have excess amounts of default hitsounds (Clap, Finish, Whistle), the algorithm will drop them.
  You can find out which are dropped using the logging method.

- If you have excess **named** samples (e.g. "clap.wav", "sub.wav"), the algorithm will push it as an event sample.
  This can also be found with the logger.

- This algorithm uses a packing method for hitsound copying.
  Hence, it'll try to group as many hitsounds together as possible while maintaining their integrity.

Algorithm
^^^^^^^^^

1. Drop all non-hitsound notes
2. Group by offset and loop through them
3. For each offsetGroup, we group them by volume. * This is where packing comes in *
4. For each volumeGroup, we attempt to slot them into available notes in our target map. This process separates default hitsounds and samples
5. If there are no slots:

   1. The algorithm will drop any default hitsounds
   2. The algorithm will sample any named samples

6. Return the map

Module Info
^^^^^^^^^^^

.. automodule:: reamber.algorithms.mutate.hitSoundCopy

###################################
Osu Measure Lines Multi Dimensional
###################################

This measure line algorithm is made to handle multiple ``svOsuMeasureLineB`` on different timestamps. Merging all of them
together to create an optimized output.

********
Features
********

As stated above, this algorithm will help you by:

- Minimizing the dependent BPM value
- Reducing the required amount of lines by clipping out ``< minimum`` and ``> maximum`` values
- Easy stacking of multiple events
- Allow variable ``X`` and ``Y`` ranges for each event.
- Allows integration of python list comprehension & lambda creation in tandem with events.

*******
Example
*******

.. code-block:: python
   :linenos:

   events = [
     SvOsuMeasureLineEvent(firstOffset=10000 + i,
                           lastOffset=20000 + i,
                           funcs=[lambda x: x],
                           startX=0, endX=1, startY=0, endY=1)
            for i in range(0, 10000, 250)
   ]

We firstly create events, this is slightly different from ``svOsuMeasureLineB`` because we get to declare **stackable**
animations.

Notice that ``events`` occur on ``[10000 -> 20000, 10250 -> 20250, 10500 -> 20500, ..., 19750 -> 29750]``

.. code-block:: python
   :linenos:

   svs, bpms = svOsuMeasureLineMD(events,
                                  firstOffset=10000,
                                  lastOffset=20000,
                                  endBpm=200,
                                  scalingFactor=1.55,
                                  paddingSize=10)

To evaluate all events and join them together, we need to call the main algorithm.

This ``firstOffset`` and ``lastOffset`` is different from the events, this will strictly cut out events that don't occur
within this range. This is useful to just cut out some animations, however, it may occur as a "gotcha".

The other parameters are derived from ``svOsuMeasureLineB`` so I won't repeat them.

Note that you cannot stack ``MDs`` on top of ``MDs``, you can only do ``MDEvents`` with ``MDEvents``. That is, if you
were to generate 2 ``MDs`` on top of each other, unexpected behavior will occur.

***********
Map Example
***********

This function is extensively used in **LeaF - Aleph-0 (Evening) [Boundless]**, I uploaded the script as a repository,
feel free to have a look!

This is a short example from that map

.. code-block:: python

   import numpy as np

   from aleph.consts import *
   from reamber.algorithms.generate.sv.generators.svOsuMeasureLineMD import svOsuMeasureLineMD, SvOsuMeasureLineEvent
   from reamber.osu.OsuMap import OsuMap

   def f002(m: OsuMap):
       events = [SvOsuMeasureLineEvent(
                 firstOffset=937 + i, lastOffset=6637 + i,
                 startX=2.5, endX=35,
                 startY=-0.5, endY=0.5,
                 funcs=[
                     lambda x:   1 / np.log(x ** 2) - .13,
                     lambda x: - 1 / np.log(x ** 2) + .13
                 ]) for i in np.linspace(0, 6637 - 937, 10)]

       f = svOsuMeasureLineMD(events,
                              scalingFactor=SCALE,
                              firstOffset=937,
                              lastOffset=6637,
                              paddingSize=PADDING,
                              endBpm=250)

       m.svs.extend(f[0])
       m.bpms.extend(f[1])

- Firstly, the event creation pivots on a list comprehension with ``np.linspace(0, 6637 - 837, 10)``. This will create
  10 events evenly spread between ``0`` and ``6637 - 837``.
- Each event has **2 exp functions** (hint: ``np.log`` is :math:`\ln`, so it's essentially exp)
- Each event depends on the list comprehension element as it's offset by the offsets of the event.
- Every event will run from domain :math:`[2.5, 35]` and range :math:`[-0.5, 0.5]`
- ``SCALE`` and ``PADDING`` is manually calculated.

***********
Module Info
***********

.. automodule:: reamber.algorithms.generate.sv.generators.svOsuMeasureLineMD

###################
Checklist / Roadmap
###################

Listed by Priority. If not **High Priority**, reason is stated.

*************
High Priority
*************

Plotting
========

To provide simple plotting for common analytics. To pivot off of ``matplotlib`` or ``plotly``.

************
Mid Priority
************

PlayField Note Snap Coloring
============================

Similar idea as StepMania, maybe we can make this ``DrawNotes`` extended API.

Reason
------

Doesn't seem important now, I'd do everything else in High Priority first.

************
Low Priority
************

UI
==

Having a UI could be useful, we can work on a separate front-end with PyQt.

Reason
------

Worked with CppQt before, never tried PyQt, could take some time to relearn some concepts.

From my experience, it's easy to use but I believe that technical debt can be big problem if I develop it while this is
still in early alpha.

Will consider once it's beta / stable alpha.

OJN + OJM Writing
=================

To enable O2J writing.

Reason
------

OJM is unnecessarily complicated to write, it could take a few weeks of delay to write this algorithm. It'll be much
more efficient if we can get someone knowledgeable to write this algorithm.

BMS Sampling
============

To enable Sample extraction and easy input.

Reason
------

Not many players use hitsounds, and it may prove to be a hard task to extract the sounds and map them correctly.

BMS Mines
=========

To enable mine loading and writing.

Reason
------

Don't have any files that use it, I'll consider it along with Sampling.

*************
Zero Priority
*************

BMS BGA
=======

To enable extraction of BMS BGAs

Reason
------

The time sunk into this will not be worth it.

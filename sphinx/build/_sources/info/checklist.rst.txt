###################
Checklist / Roadmap
###################

Listed by Priority. If not **High Priority**, reason is stated.

*************
High Priority
*************

Pattern Analytics
=================

To provide any users of the package a simple way to detect patterns.

The interface should contain:

- Pattern Detection
- Pattern Detections as Probability/Confidence
- Supporting multiple Note Type pattern Detection.
- Possibly rethinking on how we can restructure, redefine a ``NotePkg``.

Plotting
========

To provide simple plotting for common analytics. To pivot off of ``matplotlib`` or ``plotly``.


************
Mid Priority
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

************
Low Priority
************

OJN + OJM Writing
=================

To enable O2J writing.

Reason
------

OJM is unnecessarily complicated to write, it could take a few weeks of delay to write this algorithm. It'll be much
more efficient if we can get someone knowledgeable to write this algorithm.

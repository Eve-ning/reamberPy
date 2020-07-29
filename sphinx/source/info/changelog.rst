Changelog
=========

0.0.17
------
- Add ``svOsuMeasureLineMD`` Multidimensional SV generation.
- Add SV Collapsing Support. SVs close enough will now be merged.
- Remove old info about **SDF** in SV Primer
- Fix issue with negative Y in SV Generation causing incorrect error mitigation
- Attempt fixing ``OsuToSM`` and ``SMToOsu`` interconversion offset issue (again).

0.0.16
------
- Add ``BMS`` Support
- Attempt fixing ``OsuToSM`` and ``SMToOsu`` interconversion offset issue.
- ``Map.readFile("path.map")`` is now static. e.g. Initialization is now ``m = OsuMap.readFile("path.osu")``

0.0.15
------
- Add ``Dummy`` class
- Add ``PlayField`` API for new ``Pattern`` package.
- Implement ``reamber.algorithms.pattern`` package.
- Convert all ``Hold`` classes to have a separate ``HoldTail`` class.
    - All ``Hold`` classes now have to initialize with ``_length`` instead of ``length``. However, length is still an
      accessible property
- Drop ``Obj`` Suffix for most classes
- Deprecate ``analysis`` package for in-built base class functions
- Create ``plot`` package for plotting only
- Move HitsoundCopy to under ``mutate``, deprecate ``meta``

0.0.14
------
- Add SvSequence, SvPkg, and other related functions
- Change SV definition to Scroll Velocity

0.0.13
------
- Add Documentation

0.0.12
------
- Add PlayField

0.0.11
------
- Add O2J ojn support

0.0.10
------
- Overhaul structure
    - Shorten class names
    - Make implementations much easier
    - Clarify class usages

0.0.9
------
- Add piping/chaining functionality

0.0.8
------
- Fix Quaver Loading Speed issues

0.0.7
------
- Add Quaver Support

0.0.6
------
- Fix Encoding issue with loading and writing unicode

0.0.5
------
- First Working Prototype
Changelog
=========

0.1.1
-----

Simply fixes the .pyi not being uploaded.

0.1.0
-----
**Major**

Massive changes to codebase, from naming schemes, architecture and flexibility. The full release notes can be found
in the GitHub Release.

- Changed ``CamelCase`` to ``snake_case``
- Revamped how values can be modified, more easily understood with **Stacking**.
- Dropped ``inplace``
- Data storage is now using ``pd.DataFrame`` and ``pd.Series``, so it's easier to upscale.
- Dropped ``@dataclass`` for non-map classes in favor of custom props.
- Less-used and hard-to-maintain algorithms are dropped.
- Tests are now more extensive, allowing me to have a more stable codebase

**Minor**

- Some plural names are converted to singular for consistency with the property type name.
- Dropped Dummy Class
- Add basic osu! Replay Parsing with ``osrparse==5.0.0``

0.0.20
------

- Fix issue with rates breaking #36
- Add reading from string for all types
- Fix BMS BPM integer issue #20

0.0.19
------

- Fixes minor bugs in ``OsuAPI``
- Add failsafe for missing ``Qua`` Multiplier loading
- Add failsafe for bad ``Osu`` value/code loading

0.0.18
------
- Add ``OsuAPIV1`` and ``OsuAPIV2``

0.0.17
------
- Add ``sv_osu_measure_line_md`` Multidimensional SV generation.
- Add SV Collapsing Support. SVs close enough will now be merged.
- Remove old info about **SDF** in SV Primer
- Fix issue with negative Y in SV Generation causing incorrect error mitigation
- Attempt fixing ``OsuToSM`` and ``SMToOsu`` interconversion offset issue (again).

0.0.16
------
- Add ``BMS`` Support
- Attempt fixing ``OsuToSM`` and ``SMToOsu`` interconversion offset issue.
- ``Map.read_file("path.map")`` is now static. e.g. Initialization is now ``m = OsuMap.read_file("path.osu")``

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
- Move HitsoundCopy to under ``stack``, deprecate ``meta``

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
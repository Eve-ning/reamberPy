import unittest
from math import sin, pi

from reamber.algorithms.generate.sv.generators.svOsuMeasureLineA import sv_osu_measure_line_a
from reamber.algorithms.generate.sv.generators.svOsuMeasureLineC import sv_osu_measure_line_c
from reamber.algorithms.generate.sv.generators.svOsuMeasureLineMD import sv_osu_measure_line_md,SvOsuMeasureLineEvent
from reamber.algorithms.generate.sv.generators.svOsuMeasureLineB import sv_osu_measure_line_b
import numpy as np


class TestMeasureLine(unittest.TestCase):

    def testA(self):

        seq = sv_osu_measure_line_a(first_offset=5000,
                                    last_offset=20000,
                                    funcs=[lambda x: 0.5 * sin(x * pi * 2),
                                       lambda x: 0.5 * sin(x * pi * 2 + pi)],
                                    fill_bpm=200, start_x=0, end_x=4, end_bpm=200, reference_bpm=200,
                                    padding_size=20).combine()

        # with open("out.txt", "w+") as f:
        #     f.writelines([i.writeString() + "\n" for i in seq.writeAsBpm(OsuBpm)])

    def testB(self):

        lis = sv_osu_measure_line_b(first_offset=0,
                                    last_offset=40000,
                                    funcs=[lambda x: 0.5 * sin(x * pi * 2),
                                       lambda x: 0.5 * sin(x * pi * 2 + pi)],
                                    fill_bpm=200, start_x=0, end_x=4, end_bpm=100,
                                    padding_size=20)

        # with open("out.txt", "w+") as f:
        #     f.writelines([i.writeString() + "\n" for i in lis])

    def testMD(self):
        # Grabbed from Cross Shutter.

        events = [SvOsuMeasureLineEvent(10000, 20000,
                                        [lambda x, i=i, z=z: (z + (x + i / 5000)) % 1],
                                        start_x=0, end_x=1, start_y=0, end_y=1)
                  for i in range(0, 10000, 250) for z in np.linspace(0, 0.03, 5)]

        svs, bpms = sv_osu_measure_line_md(events, first_offset=10000, last_offset=20000, end_bpm=200, scaling_factor=1.55,
                                           padding_size=10)

        events = [
           SvOsuMeasureLineEvent(first_offset=10000,
                                 last_offset=20000,
                                 funcs=[lambda x, i=i: x + i],
                                 start_x=0, end_x=1, start_y=0, end_y=1)
                  for i in range(0, 10000, 250)
        ]

        svs, bpms = sv_osu_measure_line_md(events, first_offset=10000, last_offset=20000, end_bpm=200, scaling_factor=1.55,
                                           padding_size=10)


if __name__ == '__main__':
    unittest.main()

"""
# Bounce

```
svOsuMeasureLineC(
    10000, 20000,
    [lambda x: abs(sin(4*x))],
    200, startY=-1, endY=1, startX=0, endX=4 * pi)
```

# Delay Sine Wave

```
svOsuMeasureLineC(
    10000, 20000,
    [*[lambda x, i=i: sin(x + i) for i in np.linspace(0, pi/2, 5)]],
    200, startY=-1, endY=1, startX=0, endX=4 * pi)
```

# 1 Point Collapse

```
svOsuMeasureLineC(
    10000, 20000,
    [*[lambda x, i=i :  i/x -  0.05 for i in np.linspace(0, 100, 15)],
     *[lambda x, i=i : -i/x +  0.05 for i in np.linspace(0, 100, 15)],
    200, startY=-10, endY=10, startX=0.01, endX=2000)
```
# 3 Point Collapse

```
svOsuMeasureLineC(
    10000, 20000,
    [*[lambda x, i=i :  i/x -  0.05 for i in np.linspace(0, 100, 15)],
     *[lambda x, i=i : -i/x +  0.05 for i in np.linspace(0, 100, 15)],
     *[lambda x, i=i :  i/x +  3.95 for i in np.linspace(0, 100, 15)],
     *[lambda x, i=i : -i/x +  4.05 for i in np.linspace(0, 100, 15)],
     *[lambda x, i=i :  i/x + -4.05 for i in np.linspace(0, 100, 15)],
     *[lambda x, i=i : -i/x + -3.95 for i in np.linspace(0, 100, 15)]],
    200, startY=-10, endY=10, startX=0.01, endX=2000)
```

# Sine Bound Delay Modulus

```
svOsuMeasureLineC(
    10000, 20000,
    [*[lambda x, i=i: 0.5 * (x + i) % 1 + sin(x) for i in np.linspace(0, 1, 10)],
     lambda x: sin(x),
     lambda x: sin(x) + 1],
    200, startY=-1, endY=2, startX=0, endX=4 * pi)
```

# Vaporwave Intro

The lag is due to the high padding size.

```
events = [
    *[SvOsuMeasureLineEvent(10000 + i, 11000 + i, [lambda x, i=i: x ** 2 + np.sin(i * pi / 1250) * 0.5],
                            startX=0.6, endX=2, startY=-3, endY=3)
      for i in range(0, 10000, 50)],
    *[SvOsuMeasureLineEvent(10000 + i, 11000 + i, [lambda x, i=i: - (x ** 2) + np.sin(i * pi / 1250) * 0.5],
                            startX=0.6, endX=2, startY=-3, endY=3)
      for i in range(0, 10000, 50)]
]

svs, bpms = svOsuMeasureLineMD(events, first_offset=10000, last_offset=20000, endBpm=200, scalingFactor=1.55,
                               paddingSize=100)
```                               

# Stacking Bounce

```
events = [
    *[SvOsuMeasureLineEvent(10000 + i, 20000 + i,
                            [lambda x, i=i, d=d: abs(np.cos(x ** 1.2)) * 50 / (x ** 3 + 2) + i / 500 + d],
                            startX=0, endX=30, startY=0, endY=15)
            for i in range(0, 10000, 500) for d in np.linspace(0, 1, 4)]
]
svs, bpms = svOsuMeasureLineMD(events, first_offset=10000, last_offset=20000, endBpm=200, scalingFactor=1.55,
                               paddingSize=10)
```                               

# Cross Shutter

```
events = [
    *[SvOsuMeasureLineEvent(10000, 20000,
                            [lambda x, i=i, z=z: (z + (x + i / 5000)) % 1], startX=0, endX=1, startY=0, endY=1)
            for i in range(0, 10000, 250) for z in np.linspace(0, 0.03, 5)],
    *[SvOsuMeasureLineEvent(10000, 20000,
                            [lambda x, i=i: -(2 * x + i / 2500) % 1], startX=0, endX=1, startY=0, endY=1)
      for i in range(0, 10000, 250)]
]
svs, bpms = svOsuMeasureLineMD(events, first_offset=10000, last_offset=20000, endBpm=200, scalingFactor=1.55,
                               paddingSize=10)
```

"""
#####################
SV Function Sequencer
#####################

The function sequencer is inspired by most music production Digital Audio Workstations (DAWs), like FLStudio, Ableton.

The purpose of the function sequencer is to help create repeating patterns quickly without having to go through
multiple steps.

**********
Parameters
**********

Think of it as funcs setting the x-axis, offset being the y-axis like so

Let's say the functions produce the outputs here as per the x-axis input::

    X      | 0,    0.25, 0.5,  0.75, 1.0
    ------------------------------------
    FUNC 1 | 1,    2,    3,    4,    5
    FUNC 2 | 1,    1,    1,    1,    1
    FUNC 3 | 0,    4,    2,    3,    7

We can specify the ``offset`` gap with an integer, offset will be separated by that value, starting from 0.

``repeatGap`` is the gap between each repetition.

``repeats`` is the number of repetitions.

If we use ``func=[FUNC_1,FUNC_2,FUNC_3], offset=2, repeatGap=1, repeat=4``

The repetition would be::

    REPEAT 1   | REPEAT 2   | REPEAT 3   | REPEAT 4   | REPEAT 5   |
    ----------------------------------------------------------------
    OFFSET MUL | OFFSET MUL | OFFSET MUL | OFFSET MUL | OFFSET MUL |
    0      1   | 5      2   | 10     3   | 15     4   | 20     5   |
    2      1   | 7      1   | 12     1   | 17     1   | 22     1   |
    4      0   | 9      4   | 14     2   | 19     3   | 24     7   |

***********
Func Inputs
***********

You could call the above by (only `funcs` parameter shown)::

    sv_func_sequencer(funcs=[[1, 2, 3, 4, 5], [1, 1, 1, 1, 1], [0, 4, 2, 3, 7]], ...)

However, if you can simplify ``[1,2,3,4,5]`` as a lambda, as such ``lambda x: 1 + x * 4``.
If you input x as ``[0, 0.25, 0.5, 0.75, 1]`` it should return the original list.

You can also simplify ``[1,1,1,1,1]`` as just ``1``, the function will just repeat that value for the whole sequence.

These are especially useful if you have a very long func list to generate based on the X value.

Hence this is equivalent::

    sv_func_sequencer(funcs=[[lambda x: 1 + x * 4, 1, [0, 4, 2, 3, 7]], ...)

*************
Customizing X
*************

`X` always runs from 0 to 1 linearly, both ends included. You could simply adjust it with `startX` and `endX`.

**************
Skipping Slots
**************

If you are creating a long ``funcs`` list like so ``funcs=[1, 2, lambda x: x, 3]`` but need to just leave a slot empty::

    OFFSET 0     1     2     3     4
    FUNC   1     2     LMBDA       3

You could manually specify ``offset=[0,1,2,4]`` or leave a slot as None in ``funcs=[1, 2, lambda x: x, None, 3]``.

This way you don't have to manually specify the offset.

***********
Module Info
***********

.. automodule:: reamber.algorithms.generate.sv.generators.sv_func_sequencer
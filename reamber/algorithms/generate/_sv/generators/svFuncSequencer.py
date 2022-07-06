from typing import Callable, List, Union

from numpy import arange

from reamber.algorithms.generate.sv.SvPkg import SvPkg
from reamber.algorithms.generate.sv.SvSequence import SvSequence


def sv_func_sequencer(funcs: List[Union[float, Callable[[float], float], None]],
                      offsets: Union[List[float], float, None] = None,
                      repeats: int = 1,
                      repeat_gap: float = 0,
                      start_x: float = 0,
                      end_x: float = 1
                      ):
    """ Sets up a sequence using functions.

    Args:
        funcs: Funcs to generate values. \
            If List, values will be used directly. \
            If Callable, values will be called with the X. \
            If None, this will leave a gap in the sequence.
        offsets: Offsets to use on functions. \
            If List, offsets will be used to map the funcs. \
            If Float, all funcs are assumed to be separated by {float} ms. Starting from 0. \
            If None, all funcs are assumed to be separated by 1 ms. Starting from 0.
    :param repeats: The amount of repeats. This affects the increment of the X argument passed to the Callables. \
        If 0, only endX will be used.
    :param repeat_gap: The gap between the repeats.
    :param start_x: The starting X.
    :param end_x: The ending X.
    """

    length = len(funcs)

    if offsets is None: offsets = list(range(0, length))
    # We use [:length] because sometimes arange will create too many for some reason (?)
    elif isinstance(offsets, (float, int)): offsets = list(arange(0, length * offsets, offsets))[:length]

    assert length == len(offsets)

    seq = SvSequence()

    for i, (offset, func) in enumerate(zip(offsets, funcs)):
        if isinstance(func, Callable): seq.append_init([(offset, 0)])
        elif isinstance(func, (float, int)): seq.append_init([(offset, func)])
        elif func is None: pass

    pkg = SvPkg.repeat(seq=seq, times=repeats, gap=repeat_gap)

    nones = 0
    for funcI, func in enumerate(funcs):
        if func is None: nones += 1
        if isinstance(func, Callable):
            pkg.apply_nth(func, funcI - nones, start_x, end_x)

    return pkg

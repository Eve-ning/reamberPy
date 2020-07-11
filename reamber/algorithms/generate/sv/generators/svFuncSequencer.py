from typing import Callable, List, Union

from numpy import arange

from reamber.algorithms.generate.sv.SvPkg import SvPkg
from reamber.algorithms.generate.sv.SvSequence import SvSequence


def svFuncSequencer(funcs: List[Union[float, Callable[[float], float], None]],
                    offsets: Union[List[float], float, None] = None,
                    repeats: int = 1,
                    repeatGap: float = 0,
                    startX: float = 0,
                    endX: float = 1
                    ):
    """ Sets up a sequence using functions.

    :param funcs: Funcs to generate values. \
        If List, values will be used directly. \
        If Callable, values will be called with the X. \
        If None, this will leave a gap in the sequence.
    :param offsets: Offsets to use on functions. \
        If List, offsets will be used to map the funcs. \
        If Float, all funcs are assumed to be separated by {float} ms. Starting from 0. \
        If None, all funcs are assumed to be separated by 1 ms. Starting from 0.
    :param repeats: The amount of repeats. This affects the increment of the X argument passed to the Callables. \
        If 0, only endX will be used.
    :param repeatGap: The gap between the repeats.
    :param startX: The starting X.
    :param endX: The ending X.
    """

    length = len(funcs)

    if offsets is None: offsets = list(range(0, length))
    # We use [:length] because sometimes arange will create too many for some reason (?)
    elif isinstance(offsets, (float, int)): offsets = list(arange(0, length * offsets, offsets))[:length]

    assert length == len(offsets)

    seq = SvSequence()

    for i, (offset, func) in enumerate(zip(offsets, funcs)):
        if isinstance(func, Callable): seq.appendInit([(offset, 0)])
        elif isinstance(func, (float, int)): seq.appendInit([(offset, func)])
        elif func is None: pass

    pkg = SvPkg.repeat(seq=seq, times=repeats, gap=repeatGap)

    nones = 0
    for funcI, func in enumerate(funcs):
        if func is None: nones += 1
        if isinstance(func, Callable):
            pkg.applyNth(func, funcI - nones, startX, endX)

    return pkg

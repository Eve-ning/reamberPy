from reamber.osu.OsuMapObj import OsuMapObj, OsuSvObj, OsuBpmObj
from reamber.sm.SMMapSetObj import SMMapObj, SMBpmObj
from reamber.o2jam.O2JMapObj import O2JMapObj, O2JBpmObj
from reamber.quaver.QuaMapObj import QuaMapObj, QuaSvObj, QuaBpmObj
from reamber.algorithms.analysis.bpm.scrollSpeed import scrollSpeed
from reamber.algorithms.generate.sv.SvObj import SvObj
from typing import Union, List, Type, overload
from abc import abstractmethod, ABC


class SvIO(ABC):
    """ SV IO handles the input output functions for SvSequence.

    We don't integrate it like in PlayField because SvSequence can also be initialized very quickly with primitives.

    """

    @abstractmethod
    def __init__(self, _): ...
    @abstractmethod
    def data(self) -> List[SvObj]: ...

    @overload
    def writeAsSv(self, singularType: Type[OsuSvObj], **kwargs) -> List: ...
    @overload
    def writeAsSv(self, singularType: Type[QuaSvObj], **kwargs) -> List: ...
    def writeAsSv(self, singularType: Type, **kwargs) -> List:
        """ Writes the sequence as a List[singularType(offset=sv.offset, multiplier=sv.multiplier)]

        Must be able to accept 'offset' and 'multiplier' as argument.

        Allows **kwargs to input in every singularType during writing.

        Example::

            seq.writeAsSv(OsuSvObj, volume=20, kiai=True)

        :param singularType: A Type to specify, recommended to follow the overloaded Types."""
        return [singularType(offset=sv.offset, multiplier=sv.multiplier, **kwargs) for sv in self.data()]

    @overload
    def writeAsBpm(self, singularType: Type[OsuBpmObj]) -> List: ...
    @overload
    def writeAsBpm(self, singularType: Type[QuaBpmObj]) -> List: ...
    @overload
    def writeAsBpm(self, singularType: Type[SMBpmObj]) -> List: ...
    @overload
    def writeAsBpm(self, singularType: Type[O2JBpmObj]) -> List: ...
    def writeAsBpm(self, singularType: Type) -> List:
        """ Writes the sequence as a List[singularType(offset=sv.offset, bpm=sv.multiplier)]

        Must be able to accept 'offset' and 'bpm' as argument.

        Allows **kwargs to input in every singularType during writing.

        Example::

            seq.writeAsBpm(OsuBpmObj, volume=20, kiai=True)

        :param singularType: A Type to specify, recommended to follow the overloaded Types."""
        return [singularType(offset=sv.offset, bpm=sv.multiplier) for sv in self.data()]

    def readSvFromMap(self,
                      m: Union[OsuMapObj, QuaMapObj]):
        """ Reads the scroll velocities from maps.

        Inplace operation, doesn't return anything

        Only some map types have scroll velocities

        :param m: The map to read
        """
        self.__init__([(sv.offset, sv.multiplier) for sv in m.svs])

    def readTrueSvFromMap(self,
                          m: Union[OsuMapObj, O2JMapObj, SMMapObj, QuaMapObj],
                          centerBpm: float = None):
        """ Reads the true Scroll Velocity. That is, if present, SVs will be multiplied by the BPM.

        i.e. 200 Bpm and 2.0x SV -> 400.0x SV

        Inplace operation, doesn't return anything.

        :param m: The map to read
        :param centerBpm: The bpm to zero calculations on. If None, it'll just be the multiplication of bpm and sv.
        """
        self.__init__([(scroll['offset'], scroll['speed']) for scroll in scrollSpeed(m, centerBpm)])

from abc import abstractmethod, ABC
from typing import Union, List, Type, overload

from reamber.algorithms.generate.sv.SvObj import SvObj
from reamber.o2jam.O2JMap import O2JMap, O2JBpm
from reamber.osu.OsuMap import OsuMap, OsuSv, OsuBpm
from reamber.quaver.QuaMap import QuaMap, QuaSv, QuaBpm
from reamber.sm.SMMapSet import SMMap, SMBpm


class SvIO(ABC):
    """ SV IO handles the input output functions for SvSequence.

    We don't integrate it like in PlayField because SvSequence can also be initialized very quickly with primitives.

    """

    @abstractmethod
    def __init__(self, _): ...
    @abstractmethod
    def data(self) -> List[SvObj]: ...

    @overload
    def write_as_sv(self, singular_type: Type[OsuSv], **kwargs) -> List: ...
    @overload
    def write_as_sv(self, singular_type: Type[QuaSv], **kwargs) -> List: ...
    def write_as_sv(self, singular_type: Type, **kwargs) -> List:
        """ Writes the sequence as a List[singularType(offset=sv.offset, multiplier=sv.multiplier)]

        Must be able to accept 'offset' and 'multiplier' as argument.

        Allows **kwargs to input in every singularType during writing.

        Example::

            seq.writeAsSv(OsuSv, volume=20, kiai=True)

        :param singular_type: A Type to specify, recommended to follow the overloaded Types."""
        return [singular_type(offset=sv.offset, multiplier=sv.multiplier, **kwargs) for sv in self.data()]

    @overload
    def write_as_bpm(self, singular_type: Type[OsuBpm], multiplication: float = 1.0, **kwargs) -> List: ...
    @overload
    def write_as_bpm(self, singular_type: Type[QuaBpm], multiplication: float = 1.0, **kwargs) -> List: ...
    @overload
    def write_as_bpm(self, singular_type: Type[SMBpm], multiplication: float = 1.0, **kwargs) -> List: ...
    @overload
    def write_as_bpm(self, singular_type: Type[O2JBpm], multiplication: float = 1.0, **kwargs) -> List: ...
    def write_as_bpm(self, singular_type: Type, multiplication: float = 1.0, **kwargs) -> List:
        """ Writes the sequence as a List[singularType(offset=sv.offset, bpm=sv.multiplier)]

        Must be able to accept 'offset' and 'bpm' as argument.

        Allows **kwargs to input in every singularType during writing.

        Multiplication multiplies the multiplier before exporting.

        Example::

            seq.writeAsBpm(OsuBpm, volume=20, kiai=True)

        :param singular_type: A Type to specify, recommended to follow the overloaded Types.
        :param multiplication: The value to multiply before exporting the sv as a BPM.
        """
        return [singular_type(offset=sv.offset, bpm=sv.multiplier * multiplication, **kwargs) for sv in self.data()]

    def read_sv_from_map(self,
                         m: Union[OsuMap, QuaMap]):
        """ Reads the scroll velocities from maps.

        Inplace operation, doesn't return anything

        Only some map types have scroll velocities

        :param m: The map to read
        """
        self.__init__([(sv.offset, sv.multiplier) for sv in m.svs])

    def read_true_sv_from_map(self,
                              m: Union[OsuMap, O2JMap, SMMap, QuaMap],
                              centerBpm: float = None):
        """ Reads the true Scroll Velocity. That is, if present, SVs will be multiplied by the BPM.

        i.e. 200 Bpm and 2.0x SV -> 400.0x SV

        Inplace operation, doesn't return anything.

        :param m: The map to read
        :param centerBpm: The bpm to zero calculations on. If None, it'll just be the multiplication of bpm and sv.
        """
        self.__init__([(scroll['offset'], scroll['speed']) for scroll in m.scroll_speed(centerBpm)])

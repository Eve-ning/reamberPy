from reamber.base.lists.NotePkg import NotePkg
from reamber.base.lists.BpmList import BpmList
from abc import ABC, abstractmethod
from typing import Dict, TYPE_CHECKING, Tuple, List
from reamber.base.lists.TimedList import TimedList
import pandas as pd

import datetime

if TYPE_CHECKING:
    from reamber.base.Bpm import Bpm


class Map(ABC):
    """ This class should be inherited by all Map Objects

    They must inherit the data method, which extracts all data they hold.
    They are also assumed to be a TimedList.
    """

    notes: NotePkg
    bpms: BpmList

    @abstractmethod
    def data(self) -> Dict[str, TimedList]:
        """ Gets the data as a dictionary """
        ...

    def addOffset(self, by: float):
        """ Move all by a specific ms """

        for k, i in self.data().items():
            i.addOffset(by)

    def activity(self, lastOffset: float or None = None) -> List[Tuple['Bpm', float]]:
        """ Calculates how long the Bpm is active. Implicitly sorts BPM

        For example

        The algorithm calculates this::

            SEC 1   2   3   4   5   6   7   8   9
            BPM 100 ------> 200 --> 300 -------->

        returns [(BPMPoint<100>, 3000), (BPMPoint<200>, 2000), (BPMPoint<300>, 3000)]

        :param lastOffset: If not None, then this offset will be used to terminate activity, else last offset will\
            be used.
        :return: A List of Tuples in the format [(BPMPoint, Activity In ms), ...]
        """
        return self.bpms.activity(lastOffset) if lastOffset else self.bpms.activity(self.notes.lastOffset())

    def aveBpm(self, lastOffset: float = None) -> float:
        """ Calculates the average Bpm.

        :param lastOffset: If not None, then this offset will be used to terminate activity, else last note offset will\
            be used.
        """
        activitySum = 0
        sumProd = 0
        for bpm, activity in self.activity(lastOffset if lastOffset else self.notes.lastOffset()):
            activitySum += activity
            sumProd += bpm.bpm * activity
        return sumProd / activitySum

    def scrollSpeed(self, referenceBpm: float = None) -> List[Dict[str, float]]:
        """ Evaluates the scroll speed based on mapType

        e.g. if BPM == 200.0 and CenterBPM == 100.0, it'll return {'offset': X, 'speed': 2.0}

        :param referenceBpm: The bpm to zero calculations on. If None, it'll just be the multiplication of bpm and sv.
        :return: Returns a list dict of keys offset and speed
        """

        # This automatically calculates the center BPM
        # Bpm Activity implicitly sorts
        if referenceBpm is None: referenceBpm = 1
        return [dict(offset=bpm.offset, speed=bpm.bpm/referenceBpm) for bpm in self.bpms]

    @abstractmethod
    def metadata(self, unicode=True, **kwargs) -> str:
        """ Grabs the map metadata

        :param unicode: Whether to try to find the unicode or non-unicode. \
            This doesn't try to convert unicode to ascii, it just looks for if there's an available translation.
        :return:
        """

        raise NotImplementedError

    def describe(self, rounding: int = 2, unicode: bool = False, **kwargs) -> None:
        """ Describes the map's attributes as a short summary

        :param rounding: The decimal rounding
        :param unicode: Whether to attempt to get the non-unicode or unicode. \
            Doesn't attempt to translate.
        """
        print(f"Average BPM: {round(self.aveBpm(), rounding)}")

        first, last = self.notes.firstLastOffset()
        print(f"Map Length: {datetime.timedelta(milliseconds=last - first)}")
        print(self.metadata(unicode=unicode, **kwargs))
        print("---- NPS ----")
        self.notes.describeNotes()

    def nps(self, binSize: int = 1000) -> pd.DataFrame:
        """ Gets the NPS as a DataFrame

        :param binSize: The size of the binning in milliseconds
        """

        dfMaster = None

        for k, l in self.notes.data().items():
            if len(l.data()) == 0: continue
            # Fence post issue, last offset will be cut short, so we add a bin to cover the end
            dfCut = pd.cut(l.df()['offset'], bins=list(range(0, int(l.lastOffset()) + binSize, binSize)))
            dfCut = dfCut.groupby(dfCut).count()
            df = pd.DataFrame({f"{k}": dfCut.values / (binSize / 1000)})
            df = df.reset_index(inplace=False).rename(columns={'index': 'offset'}, inplace=False)
            df['offset'] *= binSize
            if dfMaster is None:
                dfMaster = df
            else:
                dfMaster = dfMaster.merge(df)

        return dfMaster

from __future__ import annotations

from abc import ABC
from typing import List, Type, overload, Any, Union, Generator, TypeVar

import pandas as pd

from reamber.base import Timed
from reamber.base.Property import list_props
from reamber.base.lists.notes.NoteList import NoteList
from reamber.osu import OsuHit
from reamber.osu.OsuNoteMeta import OsuNoteMeta

Item = TypeVar('Item')

@list_props(OsuHit)
class OsuNoteList(NoteList[Item], ABC):

    @staticmethod
    def _init_empty() -> dict:
        """ Initializes the DataFrame if no objects are passed to init. """
        return dict(**NoteList._init_empty(),
                    hitsound_set=pd.Series([], dtype='int'),
                    sample_set=pd.Series([], dtype='int'),
                    addition_set=pd.Series([], dtype='int'),
                    custom_set=pd.Series([], dtype='int'),
                    volume=pd.Series([], dtype='float'),
                    hitsound_file=pd.Series([], dtype='object'))

    @property
    def volumes(self) -> Union[pd.Series, Any]:
        # The return type is Any to prevent Type Checking during comparison
        return self.df['volume']

    @volumes.setter
    def volumes(self, val):
        self.df['volume'] = val

    @property
    def hitsound_files(self) -> Union[pd.Series, Any]:
        return self.df['hitsound_file']

    @hitsound_files.setter
    def hitsound_files(self, val):
        self.df['hitsound_file'] = val

    @property
    def sample_sets(self) -> Union[pd.Series, Any]:
        return self.df['sample_set']

    @sample_sets.setter
    def sample_sets(self, val):
        self.df['sample_set'] = val

    @property
    def hitsound_sets(self) -> Union[pd.Series, Any]:
        return self.df['hitsound_set']

    @hitsound_sets.setter
    def hitsound_sets(self, val):
        self.df['hitsound_set'] = val

    @property
    def custom_sets(self) -> Union[pd.Series, Any]:
        return self.df['custom_set']

    @custom_sets.setter
    def custom_sets(self, val):
        self.df['custom_set'] = val

    @property
    def addition_sets(self) -> Union[pd.Series, Any]:
        return self.df['addition_set']

    @addition_sets.setter
    def addition_sets(self, val):
        self.df['addition_set'] = val



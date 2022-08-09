from typing import Type

from reamber.base.lists.TimedList import TimedList


class ConvertBase:
    @staticmethod
    def cast(src: TimedList, target: Type[TimedList], mapping: dict):
        """A helper function to recast dfs, not for use outside conversions

        Notes:
            It renames the TimedList df to cast to the new type

        Args:
            src: Source Timed List
            target: Target Timed List
            mapping: Renaming Mapping
        """

        buffer = target.empty(len(src))
        for to_, from_ in mapping.items():
            buffer.__setattr__(
                to_, src.__getattribute__(from_)
                if isinstance(from_, str) else from_
            )
        return buffer

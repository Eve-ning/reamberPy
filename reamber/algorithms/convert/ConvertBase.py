from typing import Type

from reamber.base.lists.TimedList import TimedList


class ConvertBase:
    @staticmethod
    def cast(src: TimedList, target: Type[TimedList], mapping: dict):
        """ A helper function to recast dfs, not recommended for use outside conversions

        How it works is that renames the df of the TimedList such that it can be correctly casted
        to the new type

        :param src:
        :param target:
        :param mapping:
        :return:
        """

        buffer = target.empty(len(src))
        for to_, from_ in mapping.items():
            buffer.__setattr__(
                to_, src.__getattribute__(from_)
                if isinstance(from_, str) else from_
            )
        return buffer

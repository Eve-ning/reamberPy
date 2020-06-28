from dataclasses import dataclass


@dataclass
class Timed:
    """ This is the base class where all timed objects must stem from. """

    offset: float = 0.0

from reamber.base.Note import Note


class Hit(Note):
    """ A Hit Object is a timed object that is just a single tap

    Do not get confused with Note Object, which describes both hit and holds.
    """

    def __init__(self, offset: float, column: int, **kwargs):
        super(Hit, self).__init__(offset=offset, column=column, **kwargs)

    @staticmethod
    def _from_series_allowed_names():
        return Note._from_series_allowed_names()

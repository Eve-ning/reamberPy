from reamber.base.Timed import Timed


class Note(Timed):
    """ A Note Object is a playable timed object

    Do not get confused with Hit Object, which is just a single hit/tap.

    The naming convention is done this way to make it clear on what is a note, hit and hold.
    """

    def __init__(self, offset: float, column: int, **kwargs):
        super(Note, self).__init__(offset=offset, column=column, **kwargs)

    @property
    def column(self):
        return self.data['column']

    @column.setter
    def column(self, value: int):
        self.data['column'] = value

    @staticmethod
    def _from_series_allowed_names():
        return [*Timed._from_series_allowed_names(), 'column']

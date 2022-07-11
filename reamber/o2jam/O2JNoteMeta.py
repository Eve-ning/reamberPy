from reamber.base import item_props


@item_props()
class O2JNoteMeta:
    """Metadata of a O2Jam Note. """

    _props = dict(volume=['int', 0],
                  pan=['int', 8])

from __future__ import annotations


def item_props(*args: str):
    """ This decorator automatically creates the props needed to inherit.

    This is a custom decorator (unlike dataclass) because we intercept setter
    and getter to call our self.data pd.Series.

    This also generates the _from_series_allowed_names safety catch.
    """
    def gen_props(cl: type, props_:tuple=args):
        for k in props_:
            def setter(self, val, k_=k):
                self.data[k_] = val

            def getter(self, k_=k):
                return self.data[k_]

            setattr(cl, k, property(getter, setter))

        @staticmethod
        def _from_series_allowed_names():
            return [*cl.__bases__[0]._from_series_allowed_names(), *props_]

        cl._from_series_allowed_names = _from_series_allowed_names

        return cl
    return gen_props


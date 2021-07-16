from __future__ import annotations

#%%
def create_props(cl: type):
    for k, v in cl.props.items():
        def setter(self, val, k=k):
            self.data[k] = val

        def getter(self, k=k):
            return self.data[k]

        setattr(cl, k, property(getter, setter))

    return cl



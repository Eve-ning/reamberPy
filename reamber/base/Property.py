"""Property Decorators

This is the class that upholds the infrastructure of the whole package.

There are 4 main Property Decorators

1) Item Properties
2) Class Properties
3) Map Properties
4) Stack Properties

The main purpose of these decorators is to generate properties that
otherwise would flood the Python code bases.

As per the name, they are decorators of specific classes.

"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, Dict, List, Union, Any

import pandas as pd

@dataclass
class Properties:
    _props: Dict[str, List[Union[str, Any]]]
    @property
    def names(self):
        return list(self._props.keys())
    @property
    def dtypes(self):
        return [i[0] for i in self._props.values()]
    @property
    def defaults(self):
        return [i[1] for i in self._props.values()]

def item_props(prop_name='_props'):
    """This decorator automatically creates the props needed to inherit.

    The format of the input MUST follow this strictly.

    SINGULAR<str> = TYPE<str>

    This is a custom decorator (unlike dataclass) because we intercept setter
    and getter to call our self.data pd.Series.

    This also generates the _from_series_allowed_names safety catch.
    """

    # noinspection PyShadowingNames
    # noinspection DuplicatedCode
    def gen_props(cl: type, prop_name: str = prop_name):
        # Recursively finds all props and gathers them
        props_list = [getattr(cl, prop_name)]

        def get_prop(cl_: type):
            if cl_.__bases__ == type:
                return
            else:
                for b in cl_.__bases__:
                    if hasattr(b, prop_name):
                        props_list.append(getattr(b, prop_name))
                    get_prop(b)
        get_prop(cl)
        props = {k: v for i in props_list for k, v in i.items()}
        setattr(cl, prop_name, props)

        props: Dict[str, Tuple[str, str]]
        for k in props.keys():
            def setter(self, val, k_=k):
                self.data[k_] = val

            def getter(self, k_=k):
                return self.data[k_]

            setattr(cl, k, property(getter, setter))

        # noinspection PyDecorator
        @staticmethod
        def _from_series_allowed_names():
            names = []
            for b in cl.__bases__:
                if hasattr(b, '_from_series_allowed_names'):
                    # noinspection PyProtectedMember
                    names = [*names, *b._from_series_allowed_names()]
            return [*names, *props.keys()]

        cl._from_series_allowed_names = _from_series_allowed_names
        return cl
    return gen_props

def list_props(item_class: type, prop_name='_props'):
    """This decorator automatically creates the props needed to inherit.

    This is a custom decorator (unlike dataclass) because we intercept setter
    and getter to call our self.data pd.DataFrame.

    This also generates the _from_series_allowed_names safety catch.
    """
    # noinspection PyShadowingNames
    def gen_props(cl: type, item_class_: type = item_class,
                  prop_name:str = prop_name):
        props = getattr(item_class_, prop_name)
        for k, v in props.items():

            def setter(self, val, k_=k):
                self.df[k_] = val

            def getter(self, k_=k):
                return self.df[k_]

            setattr(cl, k, property(getter, setter))

        # noinspection PyDecorator, PyShadowingNames
        @staticmethod
        def _default(props:dict = props) -> dict:
            return {k: pd.Series(v[1], dtype=v[0]) for k, v in props.items()}

        cl._default = _default

        # noinspection PyDecorator, PyShadowingNames
        @staticmethod
        def props(item_class__=item_class_) -> Properties:
            # noinspection PyUnresolvedReferences
            return item_class__.props()

        cl.props = props

        # noinspection PyDecorator
        @staticmethod
        def _item_class(i=item_class_) -> type:
            return i

        cl._item_class = _item_class

        return cl
    return gen_props

def stack_props(prop_name='_props'):
    """This decorator automatically creates the props needed to inherit.

    This is a custom decorator (unlike dataclass) because we intercept setter
    and getter to call our self.data pd.DataFrame.

    The stack props must just be a string list

    This also generates the _from_series_allowed_names safety catch.
    """

    # noinspection PyShadowingNames
    def gen_props(cl: type, prop_name:str = prop_name):
        props = getattr(cl, prop_name)
        props: List[str]
        for k in props:
            def setter(self, val, k_=k):
                self[k_] = val

            def getter(self, k_=k):
                return self[k_]

            setattr(cl, k, property(getter, setter))
        return cl
    return gen_props

def map_props(prop_name='_props'):
    """This decorator automatically creates the props needed to inherit.

    This is a custom decorator (unlike dataclass) because we intercept setter
    and getter to call our self.data pd.DataFrame.

    """
    # noinspection PyShadowingNames
    # noinspection DuplicatedCode
    def gen_props(cl: type, prop_name:str = prop_name):
        props_list = [getattr(cl, prop_name)]

        def get_prop(cl_: type):
            if cl_.__bases__ == type:
                return
            else:
                for b in cl_.__bases__:
                    if hasattr(b, prop_name):
                        props_list.append(getattr(b, prop_name))
                    get_prop(b)
        get_prop(cl)
        props = {k: v for i in props_list for k, v in i.items()}
        setattr(cl, prop_name, props)

        for k in props.keys():
            def setter(self, val, k_=k):
                self.objs[k_].df = val.df

            def getter(self, k_=k):
                return self.objs[k_]

            setattr(cl, k, property(getter, setter))

        return cl
    return gen_props

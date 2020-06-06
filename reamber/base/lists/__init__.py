""" The purpose of having separate classes for these objects is to facilitate functions that deal with the whole list

Note: If it's possible to classify a certain object under notes or

E.g.
Instead of having to do a for loop to shift offset ...
    for obj in map:
        obj.offset += 100

We can just call a function
    map.notes.addOffset(100)

There are also other helper classifiers such as MapObjDataFrame, which indicates that the class can be coerced into
a pandas DataFrame.

Convention
When inheriting from this, place everything in lists package.
Names inheriting should be plural, to be clear
Also, inherit from the List[Obj] with the appropriate __init__

E.g. class BpmList(List[BpmObj], TimedList, ...)
        def __init__(self, *args):
            list.__init__(self, *args)

Unlike most things in the repository, this is not a @dataclass

"""

from reamber.base.lists.BpmList import BpmList
from reamber.base.lists.TimedList import TimedList
from reamber.base.lists.NotePkg import NotePkg

__all__ = ['BpmList', 'TimedList', 'NotePkg']

""" Instructions on subclassing

Whenever you want to create a class that inherits from this, there are a few things to take note of

1.1 Inherit from List[Obj]
1.2 You need to declare the def __init__ for initialization of List
    This is the generic way to do it
        def __init__(self, *args):
            list.__init__(self, *args)

2.1 Union of List
    Consider this
    svs: Union[OsuSvList, List[OsuSvObj]] = field(default_factory=lambda: OsuSvList())
    
    Union here is required else PyCharm will complain that you cannot allocate a List[OsuSvObj] to svs
    
    Of course it's not valid, that's where _recast comes into play
    
2.2 _recast
    In the base class, __post_init__ will call _recast after initializing.
    You just need to override _recast.
    I made it a separate function because there may be multiple super().__post_init__ s
    
    def _recast(self) -> None:
        super()._recast()  # Remember to call the super
        self.svs = OsuSvList(self.svs)

"""

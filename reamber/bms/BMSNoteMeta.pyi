class BMSNoteMeta:
    @property
    def sample(self) -> bytes: ...
    @sample.setter
    def sample(self, val) -> None: ...

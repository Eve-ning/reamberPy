from typing import List


class QuaNoteMeta:
    @property
    def keysounds(self) -> List[str]: ...

    @keysounds.setter
    def keysounds(self, val) -> None: ...

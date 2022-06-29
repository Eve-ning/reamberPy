from typing import Dict, Any

from reamber.base.Bpm import Bpm


class QuaBpm(Bpm):
    def to_yaml(self) -> Dict[str, Any]: ...

    @staticmethod
    def from_yaml(d: Dict[str, Any]) -> QuaBpm: ...

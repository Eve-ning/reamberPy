from typing import Dict, Any

from reamber.base.Bpm import Bpm


class QuaBpm(Bpm):
    def to_yaml_dict(self) -> Dict[str, Any]: ...
    @staticmethod
    def from_yaml_dict(d: Dict[str, Any]): ...

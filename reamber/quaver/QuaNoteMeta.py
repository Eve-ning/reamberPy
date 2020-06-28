from dataclasses import dataclass, field
from typing import List


@dataclass
class QuaNoteMeta:
    keySounds: List[str] = field(default_factory=lambda: [])

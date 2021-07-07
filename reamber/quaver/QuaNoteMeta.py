from dataclasses import dataclass, field
from typing import List


@dataclass
class QuaNoteMeta:
    key_sounds: List[str] = field(default_factory=lambda: [])

from __future__ import annotations

import math
from typing import NamedTuple


class Point(NamedTuple):
    x: int = 0
    y: int = 0

    def get_squared_distance_to(self, that: Point) -> float:
        return math.pow(self.x - that.x, 2) + math.pow(self.y - that.y, 2)

    def get_distance_to(self, that: Point) -> float:
        return math.sqrt(math.pow(self.x - that.x, 2) + math.pow(self.y - that.y, 2))

from __future__ import annotations

import math


class Point():
    x: int = 0
    y: int = 0

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def get_squared_distance_to(self, that: Point) -> float:
        return math.pow(self.x - that.x, 2) + math.pow(self.y - that.y, 2)

    def get_distance_to(self, that: Point) -> float:
        return math.sqrt(math.pow(self.x - that.x, 2) + math.pow(self.y - that.y, 2))

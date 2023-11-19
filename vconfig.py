from __future__ import annotations


class Config():
    height: int
    width: int
    number_of_seeds: int
    seed_size: int

    def __init__(self, height: int, width: int, number_of_seeds: int, seed_size: int) -> None:
        self.height = height
        self.width = width
        self.number_of_seeds = number_of_seeds
        self.seed_size = seed_size


def get_config():
    factor = 50
    return Config(
        height=factor*9,
        width=factor*16,
        number_of_seeds=16,
        seed_size=15,
    )

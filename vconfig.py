from __future__ import annotations

from typing import NamedTuple


class Config(NamedTuple):
    height: int = 0
    width: int = 0
    number_of_seeds: int = 0
    seed_size: int = 0


def get_config():
    factor = 100 
    return Config(
        height=factor*9,
        width=factor*16,
        number_of_seeds=16,
        seed_size=5,
    )

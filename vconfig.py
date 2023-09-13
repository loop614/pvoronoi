from __future__ import annotations

from typing import NamedTuple


class VoronoiConfig(NamedTuple):
    height: int = 0
    width: int = 0
    number_of_seeds: int = 0
    seed_size: int = 0


def get_config():
    factor = 20
    return VoronoiConfig(
        height=factor*9,
        width=factor*16,
        number_of_seeds=8,
        seed_size=5,
    )

from __future__ import annotations

from bisect import bisect_left
from typing import NamedTuple

from vpoint import Point as VoronoiPoint


class Color(NamedTuple):
    r: int = 0
    g: int = 0
    b: int = 0


def generate_colors(seeds: list[VoronoiPoint]) -> list[Color]:
    colors = []
    # TODO: remove + 1
    seed_len = len(seeds) + 1
    r, g, b = generate_rgb_diversity_arrays(seed_len)
    for i in range(seed_len):
        if not (r[i] == 0 and g[i] == 0 and b[i] == 0):
            colors.append(Color(r=r[i], g=g[i], b=b[i]))

    return colors


def generate_rgb_diversity_arrays(
    n: int,
) -> tuple[list[int], list[int], list[int]]:
    red = []
    green = []
    blue = []
    go_red = True
    go_green = False
    go_blue = False
    red_value = 0
    green_value = 0
    blue_value = 0
    diversity_numbers = diversity_numbers_for_colors()

    for i in range(n):
        red.append(red_value)
        green.append(green_value)
        blue.append(blue_value)

        if go_red:
            red_value = get_next_color_value(red_value, diversity_numbers)
            go_red, go_green, go_blue = False, True, False
        elif go_green:
            green_value = get_next_color_value(green_value, diversity_numbers)
            go_red, go_green, go_blue = False, False, True
        elif go_blue:
            blue_value = get_next_color_value(blue_value, diversity_numbers)
            go_red, go_green, go_blue = True, False, False

    return red, green, blue


def diversity_numbers_for_colors() -> list[int]:
    pivot: list[int] = [0, 255]
    pair: list[int] = []
    to_be_added: list[int] = []
    res: list[int] = [0, 255]
    while len(pivot) < 255:
        for one in pivot:
            if len(pair) != 2:
                pair.append(one)
            if len(pair) == 2:
                next_one = (pair[0] + pair[1]) // 2
                to_be_added.append(next_one)
                pair.pop(0)

        pair = []
        for next_one in to_be_added:
            index = bisect_left(pivot, next_one)
            pivot.insert(index, next_one)
            res.append(next_one)
            to_be_added = []

    return res


def get_next_color_value(color_value: int, diversity_colors: list[int]) -> int:
    current_index = diversity_colors.index(color_value)
    if current_index + 1 < len(diversity_colors):
        return diversity_colors[current_index + 1]

    return diversity_colors[0]

from __future__ import annotations

from collections import defaultdict

import vconfig
import vpoint
import vseed


def fill_voronoi_diagrams(
    image,
    config: vconfig.Config,
    seeds: list[vseed.Seed],
):
    filled = {}
    for i in range(config.height):
        filled[i] = {j: False for j in range(config.width)}

    dots = config.width * config.height
    iteration_break = 0.9 * dots

    filled = fill_by_circles(
        config, image, seeds,
        filled, iteration_break, dots,
    )
    fill_by_calculating_distance(config, image, seeds, filled)

    return image


def fill_by_circles(
    config: vconfig.Config,
    image,
    seeds: list[vseed.Seed],
    filled: dict,
    iteration_break: float,
    dots: int,
) -> dict:
    """
    do circles around seeds in color
    stop at iteration_break since big circles cost too much
    fill only once per dot
    """
    index_per_pivot: defaultdict = defaultdict(lambda: 1)
    pivot = 0

    while True:
        circle_center = seeds[pivot]
        circle_size = index_per_pivot[pivot]
        index_per_pivot[pivot] += 1

        left_upper, right_upper, square_size = get_square(
            config, index_per_pivot[pivot], seeds[pivot],
        )
        for y in range(left_upper.y, min(left_upper.y + square_size, config.height)):
            for x in range(left_upper.x, min(right_upper.x, config.width)):
                if not filled[y][x]:
                    if circle_center.p.get_distance_to(vpoint.Point(x, y)) < circle_size:
                        image[y][x] = (
                            seeds[pivot].color.r,
                            seeds[pivot].color.g,
                            seeds[pivot].color.b,
                        )
                        filled[y][x] = True
                        dots -= 1

        pivot = get_next_pilot(config, pivot)
        if dots <= iteration_break:
            return filled


def get_square(
    config: vconfig.Config,
    index: int,
    seed_point: vseed.Seed,
) -> tuple[vpoint.Point, vpoint.Point, int]:
    """
    square around the seed
    grows every iteration
    """
    left_upper_x = max(0, seed_point.p.x - index)
    left_upper_y = max(0, seed_point.p.y - index)
    left_upper = vpoint.Point(x=left_upper_x, y=left_upper_y)
    right_upper_x = min(config.width - 1, seed_point.p.x + index)
    right_upper_y = min(config.height - 1, seed_point.p.y - index)
    right_upper = vpoint.Point(x=right_upper_x, y=right_upper_y)
    square_size = index * 2

    return left_upper, right_upper, square_size


def get_next_pilot(config: vconfig.Config, pivot: int) -> int:
    pivot += 1
    if pivot > config.number_of_seeds - 1:
        pivot = 0
    return pivot


def fill_by_calculating_distance(
    config: vconfig.Config,
    image,
    seeds: list[vseed.Seed],
    filled: dict,
) -> None:
    """
    leftover empties need to be calculated one by one
    its less expensive than circles
    """
    for x in range(config.width):
        for y in range(config.height):
            if filled[y][x]:
                continue

            closest_seed = vseed.get_closest_seed(
                vpoint.Point(x=x, y=y), seeds,
            )
            image[y][x] = (
                closest_seed.color.r,
                closest_seed.color.g,
                closest_seed.color.b,
            )

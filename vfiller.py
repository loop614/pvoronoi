from __future__ import annotations

from collections import defaultdict
import math

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

    filled = fill_by_circles(config, image, seeds, filled, dots_ratio=0.1)
    fill_by_calculating_distance(config, image, seeds, filled)

    return image


def fill_by_circles(
    config: vconfig.Config,
    image,
    seeds: list[vseed.Seed],
    filled: dict,
    dots_ratio: float
) -> dict:
    """
    do circles around seeds that are far apart in color
    we can not circle seeds that are close
    stop at iteration_break
    """
    close_neighbour_distance = int(config.height / 5)
    dots = config.width * config.height
    circle_seeds = find_seeds_circle_method(seeds, close_neighbour_distance);

    dots_per_seed = (dots_ratio * dots) / len(seeds)
    iteration_break = dots_per_seed * len(circle_seeds)

    filled = fill_selected_by_circles(
        config, image, circle_seeds,
        filled, iteration_break, close_neighbour_distance
    )

    return filled


def find_seeds_circle_method(
    seeds: list[vseed.Seed],
    close_neighbour_distance: int
) -> list[vseed.Seed]:
    possible_seeds: list[vseed.Seed] = []
    for seed in seeds:
        has_really_close_neighbour = False
        for seed2 in seeds:
            if (id(seed) == id(seed2)):
                continue

            neighbour_distance = seed.p.get_distance_to(seed2.p)
            if (neighbour_distance < close_neighbour_distance):
                has_really_close_neighbour = True
                break

        if not has_really_close_neighbour:
            possible_seeds.append(seed)

    return possible_seeds;


def fill_selected_by_circles(
    config: vconfig.Config,
    image,
    seeds: list[vseed.Seed],
    filled: dict,
    iteration_break: float,
    close_neighbour_distance: int,
) -> dict:
    index_per_pivot: defaultdict = defaultdict(lambda: 1)
    dots_painted = 0
    pivots_out: list[int] = []

    while dots_painted <= iteration_break and len(pivots_out) < len(seeds):
        for pivot, seed in enumerate(seeds):
            circle_center = seed
            circle_radius = index_per_pivot[pivot]
            index_per_pivot[pivot] += 1
            if index_per_pivot[pivot] > close_neighbour_distance / 2:
                pivots_out.append(pivot)
                continue

            left_upper_x = max(0, circle_center.p.x - circle_radius)
            left_upper_y = max(0, circle_center.p.y - circle_radius)
            right_upper_x = min(config.width - 1, circle_center.p.x + circle_radius)

            for y in range(left_upper_y, min(left_upper_y + 2 * circle_radius, config.height)):
                for x in range(left_upper_x, min(right_upper_x, config.width)):
                    if filled[y][x]:
                        continue
                    if circle_center.p.get_squared_distance_to(vpoint.Point(x, y)) > math.pow(circle_radius, 2):
                        continue
                    image[y][x] = (seed.color.r, seed.color.g, seed.color.b)
                    filled[y][x] = True
                    dots_painted += 1

    return filled


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

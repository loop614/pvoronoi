from __future__ import annotations

import numpy as np

import vconfig
import vpoint
import vseed


def fill_voronoi_diagrams(
    image_matrix: np.array[np.array],
    config: vconfig.Config,
    seeds: list[vseed.Seed],
):
    filled = [[False for j in range(config.width)] for i in range(config.height)]
    filled = fill_by_circles(config, image_matrix, seeds, filled)
    fill_by_calculating_distance(config, image_matrix, seeds, filled)

    return image_matrix


def fill_by_circles(
    config: vconfig.Config,
    image_matrix: np.array[np.array],
    seeds: list[vseed.Seed],
    filled: list[list[bool]],
) -> list[list[bool]]:
    """
    do circles around seeds that are far apart in color
    we can not circle seeds that are close
    stop at iteration_break
    """
    seeds = add_circle_size_to_seeds(seeds)
    for seed in seeds:
        fill_seed_circles(config, image_matrix, seed, filled)

    return filled


def add_circle_size_to_seeds(seeds: list[vseed.Seed]) -> list[vseed.Seed]:
    for seed in seeds:
        min_distance_neighbour = float('inf')
        for seed2 in seeds:
            if (id(seed) == id(seed2)):
                continue

            neighbour_distance = seed.p.get_distance_to(seed2.p)
            if (neighbour_distance < min_distance_neighbour):
                min_distance_neighbour = neighbour_distance

        seed.set_circle_size(int(min_distance_neighbour / 2))

    return seeds


def fill_seed_circles(
    config: vconfig.Config,
    image_matrix: np.array[np.array],
    seed: vseed.Seed,
    filled: list[list[bool]],
) -> None:
    left_upper_x = max(0, seed.p.x - seed.circle_size)
    left_upper_y = max(0, seed.p.y - seed.circle_size)
    right_upper_x = min(
        config.width - 1, seed.p.x + seed.circle_size,
    )

    for y in range(left_upper_y, min(left_upper_y + 2 * seed.circle_size, config.height)):
        for x in range(left_upper_x, min(right_upper_x, config.width)):
            if filled[y][x]:
                continue
            if seed.p.get_squared_distance_to(vpoint.Point(x, y)) > seed.circle_size ** 2:
                continue
            image_matrix[y][x] = (seed.color.r, seed.color.g, seed.color.b)
            filled[y][x] = True



def fill_by_calculating_distance(
    config: vconfig.Config,
    image_matrix: np.array[np.array],
    seeds: list[vseed.Seed],
    filled: list[list[bool]],
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
            image_matrix[y][x] = (
                closest_seed.color.r,
                closest_seed.color.g,
                closest_seed.color.b,
            )
            filled[y][x] = True

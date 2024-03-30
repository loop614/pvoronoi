from __future__ import annotations

import math
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
    fill_by_circles(config, image_matrix, seeds, filled)
    fill_by_calculating_distance(config, image_matrix, seeds, filled)

    return image_matrix


def fill_by_circles(
    config: vconfig.Config,
    image_matrix: np.array[np.array],
    seeds: list[vseed.Seed],
    filled: list[list[bool]],
) -> list[list[bool]]:
    seeds = add_circle_radius_to_seeds(seeds)
    for seed in seeds:
        fill_seed_circles(config, image_matrix, seed, filled)

    return filled


def add_circle_radius_to_seeds(seeds: list[vseed.Seed]) -> list[vseed.Seed]:
    for seed in seeds:
        min_distance_neighbour = float('inf')
        for seed2 in seeds:
            if (id(seed) == id(seed2)):
                continue

            neighbour_distance = seed.p.get_distance_to(seed2.p)
            if (neighbour_distance < min_distance_neighbour):
                min_distance_neighbour = neighbour_distance

        seed.set_circle_radius(int(min_distance_neighbour / 2))

    return seeds


def fill_seed_circles(
    config: vconfig.Config,
    image_matrix: np.array[np.array],
    seed: vseed.Seed,
    filled: list[list[bool]],
) -> None:
    """
    Check circle_with_square_inside_and_outside.png
    Every circle has a rectangle on the outside, with 4 sides of the rectangle touching the circle on the side halfs
    Every circle can fit a rectangle inside, with its four tips on the circle
    When drawing the outside rectangle we need to check if the point is in the circle by calculating distance
    When drawing the inside rectangle we can 'safely' fill the color
    """
    left_upper_x = seed.p.x - seed.circle_radius
    upper_y = seed.p.y - seed.circle_radius
    left_upper_point = vpoint.Point(left_upper_x, upper_y)
    right_upper_x = seed.p.x + seed.circle_radius
    right_upper_point = vpoint.Point(right_upper_x, upper_y)

    big_square_a = left_upper_point.get_distance_to(right_upper_point)
    big_square_diagonal = big_square_a * math.sqrt(2)
    square_diagnonal_diff = (big_square_diagonal - seed.circle_diameter) / 2

    safe_rect_diag = big_square_diagonal - 2 * square_diagnonal_diff
    safe_rect_a_half = math.floor((safe_rect_diag / math.sqrt(2)) / 2)

    fill_rectangle_inside_of_circle(config, image_matrix, seed, filled, safe_rect_a_half)
    fill_rectangle_outside_of_circle(config, image_matrix, seed, filled, left_upper_point, right_upper_point, square_diagnonal_diff)


def fill_rectangle_inside_of_circle(
    config: vconfig.Config,
    image_matrix: np.array[np.array],
    seed: vseed.Seed,
    filled: list[list[bool]],
    safe_rect_a_half: int
) -> None:
    for y in range(max(0, seed.p.y - safe_rect_a_half), min(seed.p.y + safe_rect_a_half, config.height)):
        for x in range(max(0, seed.p.x - safe_rect_a_half), min(seed.p.x + safe_rect_a_half, config.width)):
            image_matrix[y][x] = (seed.color.r, seed.color.g, seed.color.b)
            filled[y][x] = True


def fill_rectangle_outside_of_circle(
    config: vconfig.Config,
    image_matrix: np.array[np.array],
    seed: vseed.Seed,
    filled: list[list[bool]],
    left_upper_point: vpoint.Point,
    right_upper_point: vpoint.Point,
    square_diagnonal_diff: float
) -> None:
    """
    The outside rectangle is devided into 4 rectangles, so we skip the inside rectangle space
    """
    z = math.floor(square_diagnonal_diff / math.sqrt(2))
    circle_radius_square = seed.circle_radius ** 2

    for y in range(max(0, left_upper_point.y), min(left_upper_point.y + z, config.height)):
        for x in range(max(0, left_upper_point.x), min(right_upper_point.x, config.width)):
            if filled[y][x]:
                continue
            if seed.p.get_squared_distance_to(vpoint.Point(x, y)) > circle_radius_square:
                continue
            image_matrix[y][x] = (seed.color.r, seed.color.g, seed.color.b)
            filled[y][x] = True

    for y in range(max(0, left_upper_point.y), min(left_upper_point.y + seed.circle_diameter, config.height)):
        for x in range(max(0, left_upper_point.x), min(left_upper_point.x + z, config.width)):
            if filled[y][x]:
                continue
            if seed.p.get_squared_distance_to(vpoint.Point(x, y)) > circle_radius_square:
                continue
            image_matrix[y][x] = (seed.color.r, seed.color.g, seed.color.b)
            filled[y][x] = True

    for y in range(max(0, left_upper_point.y + seed.circle_diameter - z), min(left_upper_point.y + seed.circle_diameter, config.height - 1)):
        for x in range(max(0, left_upper_point.x), min(right_upper_point.x, config.width)):
            if filled[y][x]:
                continue
            if seed.p.get_squared_distance_to(vpoint.Point(x, y)) > circle_radius_square:
                continue
            image_matrix[y][x] = (seed.color.r, seed.color.g, seed.color.b)
            filled[y][x] = True

    for y in range(max(0, left_upper_point.y), min(left_upper_point.y + seed.circle_diameter, config.height)):
        for x in range(max(0, right_upper_point.x) - z, min(right_upper_point.x, config.width)):
            if filled[y][x]:
                continue
            if seed.p.get_squared_distance_to(vpoint.Point(x, y)) > circle_radius_square:
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

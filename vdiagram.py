from __future__ import annotations

import math
from collections import defaultdict

import numpy as np
from PIL import Image

import vcolor
import vseed as seed
from vconfig import get_config
from vconfig import VoronoiConfig
from vpoint import Point as VoronoiPoint


def generate_image():
    config = get_config()
    assert math.sqrt(
        config.number_of_seeds,
    ) % 10 != 0, 'seeds needs to be a factor of 4 for now'
    assert config.height * config.width / 4 > config.number_of_seeds, \
        'this many seeds wont fit to this small image'
    seeds = seed.generate_seeds(config)
    # seeds = generate_seeds_random_by_square()
    colors = vcolor.generate_colors(seeds)
    image = np.zeros((config.height, config.width, 3), np.uint8)
    image = add_voronoi_diagrams(config, image, seeds, colors)
    image = seed.add_seeds_to_image(config, image, seeds, colors)
    im = Image.fromarray(image).convert('RGB')
    im.save('out.png')


def add_voronoi_diagrams(config: VoronoiConfig, image, seeds, colors: list[vcolor.Color]):
    filled = fill_by_circles(colors, config, image, seeds)
    fill_by_calculating_distance(colors, config, image, seeds, filled)

    return image


def fill_by_circles(colors, config, image, seeds):
    """
    do circles around seeds in color
    stop at iteration_break since big circles cost too much
    fill only once per dot
    """
    filled = {}
    for i in range(config.height):
        filled[i] = {j: False for j in range(config.width)}

    index_per_pivot: defaultdict = defaultdict(lambda: 1)
    pivot = 0
    dots = config.width * config.height
    iteration_break = 0.8 * dots

    while True:
        left_upper, right_upper, square_size = get_square(
            config, index_per_pivot[pivot], seeds[pivot],
        )
        index_per_pivot[pivot] += 1
        for y in range(left_upper.y, min(left_upper.y + square_size, config.height)):
            for x in range(left_upper.x, min(right_upper.x, config.width)):
                if not filled[y][x]:
                    image[y][x] = (
                        colors[pivot].r,
                        colors[pivot].g,
                        colors[pivot].b,
                    )
                    filled[y][x] = True
                    dots -= 1

        pivot = get_next_pilot(config, pivot)
        if dots <= iteration_break:
            return filled


def get_square(config: VoronoiConfig, index: int, seed_point: VoronoiPoint) -> tuple[VoronoiPoint, VoronoiPoint, int]:
    """
    square around the seed
    grows every iteration
    """
    left_upper_x = max(0, seed_point.x - index)
    left_upper_y = max(0, seed_point.y - index)
    left_upper = VoronoiPoint(x=left_upper_x, y=left_upper_y)
    right_upper_x = min(config.width - 1, seed_point.x + index)
    right_upper_y = min(config.height - 1, seed_point.y - index)
    right_upper = VoronoiPoint(x=right_upper_x, y=right_upper_y)
    square_size = index * 2 + 1

    return left_upper, right_upper, square_size


def get_next_pilot(config, pivot):
    pivot += 1
    if pivot > config.number_of_seeds - 1:
        pivot = 0
    return pivot


def fill_by_calculating_distance(colors, config, image, seeds, filled):
    """
    leftover empties need to be calculated one by one
    its less expensive than circles
    """
    for x in range(config.width):
        for y in range(config.height):
            if filled[y][x]:
                continue

            closest_seed_index = seed.get_closest_seed(
                VoronoiPoint(x=x, y=y), seeds,
            )
            image[y][x] = (
                colors[closest_seed_index].r,
                colors[closest_seed_index].g,
                colors[closest_seed_index].b,
            )

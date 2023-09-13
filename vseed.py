from __future__ import annotations

import math
import random

from vconfig import VoronoiConfig
from vpoint import Point as VoronoiPoint


def generate_seeds(config: VoronoiConfig) -> list[VoronoiPoint]:
    seeds = []
    while True:
        pos_x = random.randint(0, config.width)
        pos_y = random.randint(0, config.height)
        seeds.append(VoronoiPoint(x=pos_x, y=pos_y))

        if len(seeds) == config.number_of_seeds:
            break

    return seeds


def generate_seeds_random_by_square(config: VoronoiConfig) -> list[VoronoiPoint]:
    seeds = []
    division_number = math.sqrt(config.number_of_seeds)
    width_box = math.ceil(config.width / division_number)
    height_box = math.ceil(config.height / division_number)

    for i in range(0, config.width - 1, width_box):
        for j in range(0, config.height - 1, height_box):
            if j + height_box - 1 < config.height:
                max_y = j + height_box - 1
            else:
                max_y = config.height - 1

            if i + width_box - 1 < config.width:
                max_x = i + width_box - 1
            else:
                max_x = config.width - 1

            pos_x = random.randint(i, max_x)
            pos_y = random.randint(j, max_y)
            if pos_x < config.width and pos_y < config.height:
                seeds.append(VoronoiPoint(x=pos_x, y=pos_y))
            else:
                print('not taken')

    return seeds


def add_seeds_to_image(config: VoronoiConfig, image, seeds, colors):
    seed_size_range = range(
        -math.floor(config.seed_size / 2),
        math.floor(config.seed_size / 2),
    )
    for (index, seed) in enumerate(seeds):
        for size_x in seed_size_range:
            for size_y in seed_size_range:
                x = min(seed.x + size_x, config.width - 1)
                y = min(seed.y + size_y, config.height - 1)
                seed_color = 0x000000
                if colors[index].r == 0 and colors[index].g == 0 and colors[index].b == 0:
                    seed_color = 0xffffff

                image[y][x] = seed_color

    return image


def get_closest_seed(needle, seeds):
    min_dis = float('inf')
    i = 0
    for index, seed in enumerate(seeds):
        dis = needle.get_squared_distance_to(seed)
        if dis < min_dis:
            min_dis = dis
            i = index

    return i

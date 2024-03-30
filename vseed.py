from __future__ import annotations

import math
import random

import vcolor
import vconfig
import vpoint


class Seed():
    p: vpoint.Point
    color: vcolor.Color
    circle_radius: int

    def __init__(self, p: vpoint.Point, color: vcolor.Color):
        self.p = p
        self.color = color
        self.circle_radius = 0

    def set_circle_radius(self, circle_radius: int) -> None:
        self.circle_radius = circle_radius
        self.circle_diameter = 2 * circle_radius


def generate_seeds(config: vconfig.Config, colors: list[vcolor.Color]) -> list[Seed]:
    seeds = []
    for i in range(config.number_of_seeds):
        pos_x = random.randint(
            config.seed_size, config.width - config.seed_size,
        )
        pos_y = random.randint(
            config.seed_size, config.height - config.seed_size,
        )
        seeds.append(Seed(p=vpoint.Point(x=pos_x, y=pos_y), color=colors[i]))

    return seeds


def generate_seeds_random_by_square(config: vconfig.Config) -> list[vpoint.Point]:
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
                seeds.append(vpoint.Point(x=pos_x, y=pos_y))
            else:
                print('not taken')

    return seeds


def add_seeds_to_image(config: vconfig.Config, image_matrix, seeds: list[Seed]):
    seed_size_range = range(
        -math.floor(config.seed_size / 2),
        math.floor(config.seed_size / 2),
    )
    for (index, seed) in enumerate(seeds):
        for size_x in seed_size_range:
            for size_y in seed_size_range:
                x = min(seed.p.x + size_x, config.width - 1)
                y = min(seed.p.y + size_y, config.height - 1)
                seed_color = 0x000000
                if seeds[index].color.r == 0 and seeds[index].color.g == 0 and seeds[index].color.b == 0:
                    seed_color = 0xffffff

                image_matrix[y][x] = seed_color

    return image_matrix


def get_closest_seed(needle: vpoint.Point, seeds) -> Seed:
    min_dis = float('inf')
    min_seed = Seed(color=vcolor.Color(r=0, g=0, b=0), p=vpoint.Point(0, 0))

    for index, seed in enumerate(seeds):
        dis = needle.get_squared_distance_to(seed.p)
        if dis < min_dis:
            min_seed = Seed(
                color=vcolor.Color(
                    r=seed.color.r, g=seed.color.g, b=seed.color.b,
                ),
                p=vpoint.Point(seed.p.x, seed.p.y),
            )
            min_dis = dis

    return min_seed

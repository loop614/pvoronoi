from __future__ import annotations

import math
import random
from bisect import bisect_left
from typing import NamedTuple

import numpy as np
from PIL import Image

factor = 100
height = factor * 9
width = factor * 16
number_of_seeds = 16
seed_size = 10


class Point(NamedTuple):
    x: float = 0
    y: float = 0

    def get_squared_distance_to(self, that) -> float:
        return math.pow(self.x - that.x, 2) + math.pow(self.y - that.y, 2)


class Color(NamedTuple):
    r: int = 0
    g: int = 0
    b: int = 0


def generate_seeds() -> list[Point]:
    seeds = []
    while True:
        pos_x = random.randint(0, width)
        pos_y = random.randint(0, height)
        seeds.append(Point(x=pos_x, y=pos_y))

        if len(seeds) == number_of_seeds:
            break

    return seeds


def generate_seeds_random_by_square() -> list[Point]:
    seeds = []
    division_number = math.sqrt(number_of_seeds)
    width_box = math.ceil(width / division_number)
    height_box = math.ceil(height / division_number)

    for i in range(0, width - 1, width_box):
        for j in range(0, height - 1, height_box):
            if j + height_box - 1 < height:
                max_y = j + height_box - 1
            else:
                max_y = height - 1

            if i + width_box - 1 < width:
                max_x = i + width_box - 1
            else:
                max_x = width - 1

            pos_x = random.randint(i, max_x)
            pos_y = random.randint(j, max_y)
            if pos_x < width and pos_y < height:
                seeds.append(Point(x=pos_x, y=pos_y))
            else:
                print('not taken')

    return seeds


def add_seeds_to_image(image, seeds):
    seed_size_range = range(
        -math.floor(seed_size / 2),
        math.floor(seed_size / 2),
    )
    for seed in seeds:
        for size_x in seed_size_range:
            for size_y in seed_size_range:
                x = seed.x + size_x
                y = seed.y + size_y
                if image[y][x] is not None:
                    image[y][x] = 0x000000

    return image


def get_next_color_value(color_value: int, diversity_colors: list[int]) -> int:
    current_index = diversity_colors.index(color_value)
    if current_index + 1 < len(diversity_colors):
        return diversity_colors[current_index + 1]

    return diversity_colors[0]


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


def generate_colors(seeds: list[Point]) -> list[Color]:
    colors = []
    r, g, b = generate_rgb_diversity_arrays(len(seeds))
    for i in range(len(seeds)):
        colors.append(Color(r=r[i], g=g[i], b=b[i]))

    return colors


def get_closest_seed(needle, seeds):
    min_dis = float('inf')
    i = 0
    for index, seed in enumerate(seeds):
        dis = needle.get_squared_distance_to(seed)
        if dis < min_dis:
            min_dis = dis
            i = index

    return i


def add_voronoi_diagrams(image, seeds, colors: list[Color]):
    # TODO: circle about the seeds one by one, until you hit color
    for x in range(width):
        for y in range(height):
            closest_seed_index = get_closest_seed(Point(x=x, y=y), seeds)
            image[y][x] = (
                colors[closest_seed_index].r,
                colors[closest_seed_index].g,
                colors[closest_seed_index].b,
            )

    return image


def main():
    assert math.sqrt(
        number_of_seeds,
    ) % 10 != 0, 'seeds needs to be a factor of 4 for now'
    assert height * width / 4 > number_of_seeds, \
        'this many seeds wont fit to this small image'
    seeds = generate_seeds()
    # seeds = generate_seeds_random_by_square()
    colors = generate_colors(seeds)
    image = np.zeros((height, width, 3), np.uint8)
    image = add_voronoi_diagrams(image, seeds, colors)
    image = add_seeds_to_image(image, seeds)
    im = Image.fromarray(image).convert('RGB')
    im.save('output.png')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

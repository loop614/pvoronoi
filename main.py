import math
import random
from typing import NamedTuple, List, Tuple
from PIL import Image
import numpy as np

factor = 100
height = factor * 9
width = factor * 16
number_of_seeds = 16


class Point(NamedTuple):
    x: float = 0
    y: float = 0

    def get_squared_distance_to(self, that) -> float:
        return math.pow(self.x - that.x, 2) + math.pow(self.y - that.y, 2)


class Color(NamedTuple):
    r: int = 0
    g: int = 0
    b: int = 0


def generate_seeds() -> List[Point]:
    # TODO: consider going full random
    seeds = []
    division_number = math.sqrt(number_of_seeds)
    width_box = math.ceil(width / division_number)
    height_box = math.ceil(height / division_number)

    for i in range(0, width - 1, width_box):
        for j in range(0, height - 1, height_box):
            max_y = j + height_box - 1 if j + height_box - 1 < height else height - 1
            max_x = i + width_box - 1 if i + width_box - 1 < width else width - 1

            pos_x = random.randint(i, max_x)
            pos_y = random.randint(j, max_y)
            if pos_x < width and pos_y < height:
                seeds.append(Point(x=pos_x, y=pos_y))
            else:
                print('not taken')

    return seeds


def add_seeds_to_image(image, seeds):
    for seed in seeds:
        if image[seed.y][seed.x] is not None:
            image[seed.y][seed.x] = 0xFFFFFF

    return image


def get_next_color_value(color_value: int, start: int = 255, tick=True) -> int:
    # TODO: finish the distinct color generator, like binary search just go both ways
    if color_value == 0:
        return 255

    if color_value == 255:
        return 127

    if color_value == 127:
        return 169

    if color_value == 169:
        return 64

    return 0


def generate_rgb_diversity_arrays(n: int) -> Tuple[List[int], List[int], List[int]]:
    red = []
    green = []
    blue = []
    go_red = True
    go_green = False
    go_blue = False
    red_value = 0
    green_value = 0
    blue_value = 0

    for i in range(n):
        red.append(red_value)
        green.append(green_value)
        blue.append(blue_value)

        if go_red:
            red_value = get_next_color_value(red_value)
            go_red, go_green, go_blue = False, True, False
        elif go_green:
            green_value = get_next_color_value(green_value)
            go_red, go_green, go_blue = False, False, True
        elif go_blue:
            blue_value = get_next_color_value(blue_value)
            go_red, go_green, go_blue = True, False, False

    return red, green, blue


def generate_colors(seeds: List[Point]) -> List[Color]:
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


def add_voronoi_diagrams(image, seeds, colors: List[Color]):
    # TODO: circle about the seeds one by one, until you hit color
    for x in range(width):
        for y in range(height):
            closest_seed_index = get_closest_seed(Point(x=x, y=y), seeds)
            image[y][x] = (colors[closest_seed_index].r, colors[closest_seed_index].g, colors[closest_seed_index].b)

    return image


def main():
    assert math.sqrt(number_of_seeds) % 10 != 0, 'seeds needs to be a factor of 4 for now, its more pretty that way'
    assert height * width / 4 > number_of_seeds, 'this many seeds wont fit to this small image'
    seeds = generate_seeds()
    colors = generate_colors(seeds)
    image = np.zeros((height, width, 3), np.uint8)
    image = add_seeds_to_image(image, seeds)
    image = add_voronoi_diagrams(image, seeds, colors)
    im = Image.fromarray(image).convert('RGB')
    im.save("output.png")

    return 0


if __name__ == '__main__':
    raise SystemExit(main())

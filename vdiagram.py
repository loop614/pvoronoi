from __future__ import annotations

import math

import numpy as np
import imageio

import vcolor
import vconfig
import vfiller
import vseed


def generate_image():
    config = vconfig.get_config()
    assert math.sqrt(
        config.number_of_seeds,
    ) % 10 != 0, 'seeds needs to be a factor of 4 for now'
    assert config.height * config.width / 4 > config.number_of_seeds, \
        'this many seeds wont fit to this small image'
    colors = vcolor.generate_colors(config.number_of_seeds)
    seeds = vseed.generate_seeds(config, colors)
    # seeds = vseed.generate_seeds_random_by_square()
    image_matrix = np.zeros((config.height, config.width, 3), np.uint8)
    image_matrix = vfiller.fill_voronoi_diagrams(image_matrix, config, seeds)
    image_matrix = vseed.add_seeds_to_image(config, image_matrix, seeds)
    imageio.imwrite('out.png', image_matrix)

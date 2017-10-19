#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import logging
from math import sqrt

from npgameworld.world import World


def get_hero_actions(enemies, hero_x, hero_y):
    hero_actions = []

    if not enemies:
        return hero_actions

    distances = []  # to enemies
    for e in enemies:
        t = (sqrt((e['x']-hero_x)**2 + (e['y']-hero_y)**2), e['enemy_id'])
        distances.append(t)

    nearest_enemy = sorted(distances)[0][1]
    for e in enemies:
        if e['enemy_id'] == nearest_enemy:
            enemy_x = e['x']
            enemy_y = e['y']

    # Shoot to nearest enemy
    hero_actions.append({'cmd': 'shoot', 'x': enemy_x, 'y': enemy_y})

    # Move into reversed direction from nearest enemy
    # xd - x direction, yd - y direction
    if enemy_x > hero_x:
        xd = -1
    elif enemy_x < hero_x:
        xd = 1
    else:
        xd = 0

    if enemy_y > hero_y:
        yd = -1
    elif enemy_y < hero_y:
        yd = 1
    else:
        yd = 0

    hero_actions.append({'cmd': 'move', 'xd': xd, 'yd': yd})

    return hero_actions


def main():

    # Init game world
    world = World(conf_path=os.path.realpath('config-example.json'))

    world.logger.setLevel(logging.DEBUG)

    # Start world generator
    wg = world.world_gen()
    wg.send(None)

    while not world.game_over:

        # Hero actions
        hero_actions = get_hero_actions(world.world_stat['enemies'],
                                        world.hero_x, world.hero_y)

        try:
            wg.send(hero_actions)
        except StopIteration:
            continue

    print(world.world_stat)


if __name__ == '__main__':
    main()

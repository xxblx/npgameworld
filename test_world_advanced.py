#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
    world = World(screen_width=1280, screen_height=1024, start_enemies=5)

    world.init_hero()

    world.add_enemy_type(unlock_iter=0, radius=15, spd=1, power=2, hp=1)
    world.add_enemy_type(unlock_iter=2500, radius=25, spd=0.7, power=1, hp=1)
    world.add_enemy_type(unlock_iter=5000, radius=15, spd=1, power=0, hp=1)
    world.add_enemy_type(unlock_iter=6000, radius=15, spd=0.5, power=1, hp=1)
    world.add_enemy_type(unlock_iter=6000, radius=10, spd=0.25, power=0.5,
                         hp=3)
    world.add_enemy_type(unlock_iter=8000, radius=15, spd=3, power=0, hp=1)
    world.add_enemy_type(unlock_iter=10000, radius=15, spd=2, power=2, hp=1)
    world.add_enemy_type(unlock_iter=15000, radius=25, spd=0.3, power=3, hp=3)
    world.add_enemy_type(unlock_iter=15000, radius=10, spd=5, power=0, hp=1)
    world.add_enemy_type(unlock_iter=17500, radius=15, spd=3, power=2, hp=1)
    world.add_enemy_type(unlock_iter=20000, radius=10, spd=4, power=1, hp=1)
    world.add_enemy_type(unlock_iter=22500, radius=8, spd=3, power=1, hp=1)
    world.add_enemy_type(unlock_iter=27500, radius=10, spd=4, power=2, hp=1)
    world.add_enemy_type(unlock_iter=30000, radius=20, spd=4, power=2, hp=2)
    world.add_enemy_type(unlock_iter=31000, radius=15, spd=6, power=0.1, hp=5)
    world.add_enemy_type(unlock_iter=32500, radius=25, spd=2, power=5, hp=1)
    world.add_enemy_type(unlock_iter=35000, radius=12, spd=0.5, power=1, hp=10)
    world.add_enemy_type(unlock_iter=40000, radius=15, spd=6, power=1, hp=2)
    world.add_enemy_type(unlock_iter=50000, radius=10, spd=6, power=3, hp=3)
    world.add_enemy_type(unlock_iter=70000, radius=5, spd=9, power=5, hp=5)

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

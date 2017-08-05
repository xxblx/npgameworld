#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

from npgameworld.world import World


def main():
    world = World()
    world.init_hero()
    world.add_enemy_type()

    world.logger.setLevel(logging.DEBUG)

    wg = world.world_gen()
    wg.send(None)

    while not world.game_over:
        try:
            wg.send(1)
        except StopIteration:
            print('game over', world.game_over)
            print(world.world_stat)


if __name__ == '__main__':
    main()

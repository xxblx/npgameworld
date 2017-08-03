#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from npgameworld.world import NpGameWorld


def main():
    world = NpGameWorld()
    world.init_hero()
    world.add_enemy_type()

    wg = world.world_gen()

    while True:
        wg.send(None)
        try:
            wg.send(1)
        except StopIteration:
            print('game over')


if __name__ == '__main__':
    main()

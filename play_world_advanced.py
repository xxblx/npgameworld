#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

import pygame

from npgameworld.world import World
from test_world import get_hero_actions


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

    # pygame used for circles drawing only
    screen = pygame.display.set_mode((world.screen_width, world.screen_height))
    clock = pygame.time.Clock()
    fps = 60
    pygame.init()
    pygame.display.init()

    hero_color = (255, 255, 255)
    hero_bullet_color = (239, 0, 255)

    # Start world generator
    wg = world.world_gen()
    wg.send(None)

    # Run pygame loop with world generator
    while not world.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                world.gameover = True

        screen.fill((0, 0, 0))

        # Hero actions
        hero_actions = get_hero_actions(world.world_stat['enemies'],
                                        world.hero_x, world.hero_y)

        try:
            wg.send(hero_actions)
        except StopIteration:
            continue

        # Draw hero
        pygame.draw.circle(screen, hero_color,
                           (int(world.hero_x), int(world.hero_y)),
                           world.hero_radius)

        # Draw enemies
        for e in world.world_stat['enemies']:
            color = (e['power'] + e['hp'] + e['spd']**2 + e['radius']) * 4

            if color > 255:
                color = 255

            pygame.draw.circle(screen, (color, color, 255),
                               (int(e['x']), int(e['y'])), e['radius'])

        # Draw bullets
        for b in world.hero_bullets:
            pygame.draw.circle(screen, hero_bullet_color,
                               (int(b['x']), int(b['y'])), b['radius'])

        pygame.display.flip()
        clock.tick(fps)

    print(world.world_stat)
    pygame.display.quit()
    pygame.quit()


if __name__ == '__main__':
    main()

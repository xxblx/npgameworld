#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

import pygame

from npgameworld.world import World
from test_world import get_hero_actions


def main():

    # Init game world
    world = World()
    world.init_hero()
    world.add_enemy_type()
    world.logger.setLevel(logging.DEBUG)

    # pygame used for circles drawing only
    screen = pygame.display.set_mode((world.screen_width, world.screen_height))
    clock = pygame.time.Clock()
    fps = 120
    pygame.init()
    pygame.display.init()

    hero_color = (255, 255, 255)
    hero_bullet_color = (239, 0, 255)
    enemy_color = (51, 222, 32)

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
        for e in world.enemies:
            pygame.draw.circle(screen, enemy_color,
                               (int(e.x), int(e.y)), e.radius)

        # Draw bullets
        for b in world.hero_bullets:
            pygame.draw.circle(screen, hero_bullet_color, (int(b.x), int(b.y)),
                               b.radius)

        pygame.display.flip()
        clock.tick(fps)

    print(world.world_stat)
    pygame.display.quit()
    pygame.quit()


if __name__ == '__main__':
    main()

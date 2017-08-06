#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

import pygame

from npgameworld.world import World


def main():

    # Init game world
    world = World()
    world.init_hero()
    world.add_enemy_type()
    world.logger.setLevel(logging.DEBUG)

    screen = pygame.display.set_mode((world.screen_width, world.screen_height))
    clock = pygame.time.Clock()
    fps = 30
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

        try:
            wg.send(1)
        except StopIteration:
            break

        # Draw hero
        pygame.draw.circle(screen, hero_color, (world.hero_x, world.hero_y),
                           world.hero_radius)

        # Draw enemies
        for e in world.enemies:
            pygame.draw.circle(screen, enemy_color, (e.x, e.y), e.radius)

        # Draw bullets
        for b in world.hero_bullets:
            pygame.draw.circle(screen, hero_bullet_color, (b.x, b.y), b.radius)

        pygame.display.flip()
        clock.tick(fps)

    pygame.display.quit()
    pygame.quit()


if __name__ == '__main__':
    main()

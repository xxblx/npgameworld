#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from math import sqrt

import pygame

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

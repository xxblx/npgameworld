# -*- coding: utf-8 -*-

import logging
from math import sqrt
from random import randint

from .npc import Hero, Enemy


class World:

    def __init__(self, screen_width=1024, screen_height=768, start_enemies=3,
                 enemies_max_iter_step=100, spawn_dst=150):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Every <enemies_max_iter_step> +1 max enemies
        self.enemies_max_iter_step = enemies_max_iter_step
        self.enemies_max = start_enemies
        self.enemies_locked = {}  # key is unlock level
        self.enemies_types = []  # available unlocked enemies configs
        self.enemy_id = 0

        self.enemies = set()  # alive enemies objects
        self.hero_bullets = set()  # alive hero's bullets objects

        # Minimal possible distance between hero and enemy centres
        # on enemies spawns
        self.spawn_dst = spawn_dst

        self.world_stat = {
            'status': {'game_state': 0},
            'hero': {},
            'enemies': [],
            'bullets': []
        }
        self.game_over = False
        self.iter_count = 0  # completed iterations counter
        self.enemies_killed = 0

        self.logger = WorldLogger(self)
        self.logger.debug('World init')

    def init_hero(self, hp=100, radius=15, spd=3, bullet_radius=3,
                  bullet_spd=6, bullet_power=1, reload_iters=15):
        """ Setup and add hero to world """

        self.hero_hp = hp
        self.hero_radius = radius
        self.hero_spd = spd
        self.hero_move_directions = (-1, 0, 1)
        # How many iterations hero reloads after one shot
        self.hero_reload_iters = reload_iters

        self.herp_bul_radius = bullet_radius
        self.hero_bul_spd = bullet_spd
        self.hero_bul_power = bullet_power

        self.hero_x = int(self.screen_width / 2)
        self.hero_y = int(self.screen_height / 2)

        self.hero = Hero(self, self.hero_x, self.hero_y, self.hero_radius,
                         self.hero_spd, self.herp_bul_radius,
                         self.hero_bul_spd, self.hero_bul_power)

    def add_enemy_type(self, unlock_iter=0, radius=15, spd=1, power=2, hp=1):
        if unlock_iter not in self.enemies_locked:
            self.enemies_locked[unlock_iter] = []

        self.enemies_locked[unlock_iter].append(
            {'radius': radius, 'spd': spd, 'power': power, 'hp': hp}
        )

    def update_world_stat(self):
        """ Place world info into self.world_stat dict """

        self.world_stat['hero'] = {
            'x': self.hero_x,
            'y': self.hero_y,
            'hp': self.hero_hp,
            'reload_wait': self.hero.reload_wait
        }

        self.world_stat['status'] = {
            'game_state': 1,
            'iter_num': self.iter_count,
            'enemies': len(self.enemies),
            'enemies_killed': self.enemies_killed,
            'max_enemies': self.enemies_max,
            'bullets': len(self.hero_bullets),
        }

        enemies_list = []
        for e in self.enemies:
            enemies_list.append({
                'x': e.x,
                'y': e.y,
                'radius': e.radius,
                'spd': e.spd,
                'power': e.power,
                'hp': e.hp,
                'enemy_id': e.enemy_id
            })

        bullets_list = []
        for b in self.hero_bullets:
            bullets_list.append({
                'x': b.x,
                'y': b.y,
                'radius': b.radius,
                'spd': b.spd,
                'power': b.power,
                'x_spawn': b.x_spawn,
                'y_spawn': b.y_spawn,
                'x_target': b.x_target,
                'y_target': b.y_target
            })

        self.world_stat['enemies'] = enemies_list
        self.world_stat['bullets'] = bullets_list

    def world_gen(self):
        """ Generator for world loop """

        hero_actions = None

        while not self.game_over:

            hero_iter_damage = 0
            rm_bullets = set()
            rm_enemies = set()

            hero_actions = yield hero_actions
            if hero_actions:
                hero_moved = False
                hero_shot = False

                if self.hero.reload_wait > 0:
                    hero_shot = True

                for action in hero_actions:
                    action_bad = False

                    if action['cmd'] == 'move' and not hero_moved:
                        # Check does action command correct
                        if action['xd'] not in self.hero_move_directions:
                            action_bad = True
                        elif action['yd'] not in self.hero_move_directions:
                            action_bad = True

                        if not action_bad:
                            self.hero.move(action['xd'], action['yd'])
                            hero_moved = True

                    elif action['cmd'] == 'shoot' and not hero_shot:
                        # Check does action command correct
                        if not (0 <= action['x'] <= self.screen_width):
                            action_bad = True
                        elif not (0 <= action['y'] <= self.screen_height):
                            action_bad = True

                        if not action_bad:
                            bullet = self.hero.shoot(action['x'], action['y'])
                            self.hero_bullets.add(bullet)
                            hero_shot = True
                            self.hero.reload_wait = self.hero_reload_iters+1

                    if action_bad:
                        logging.debug('Bad action: %s' % action)

            self.logger.debug('Hero actions: %s' % hero_actions)

            if self.hero.reload_wait > 0:
                self.hero.reload_wait -= 1

            self.hero_x = self.hero.x
            self.hero_y = self.hero.y
            self.logger.debug('Hero pos: %d,%d' % (self.hero_x, self.hero_y))

            # Bullets moving
            for bullet in self.hero_bullets:
                bullet.iter_process()
                if bullet.border_crossed:
                    rm_bullets.add(bullet)

            # Enemies moving
            for enemy in self.enemies:
                enemy.iter_process()

                if enemy.hit_hero:
                    hero_iter_damage += enemy.power

                if enemy.damaged_by is not None:
                    rm_bullets.add(enemy.damaged_by)

                if not enemy.alive:
                    rm_enemies.add(enemy)

            self.enemies_killed += len(rm_enemies)
            self.logger.debug('Killed enemies on iter: %d' % len(rm_enemies))

            self.logger.debug('Hero got %d damage' % hero_iter_damage)
            self.hero_hp -= hero_iter_damage
            self.logger.debug('Hero hp: %d' % self.hero_hp)

            if self.hero_hp <= 0:
                self.game_over = True
                self.update_world_stat()
                self.world_stat['status']['game_state'] = 2
                self.logger.debug('Gameover')
                return

            # Remove killed objects
            self.hero_bullets.difference_update(rm_bullets)
            self.enemies.difference_update(rm_enemies)

            self.logger.debug('Enemies killed: %d' % len(rm_enemies))
            self.logger.debug('Bullets killed: %d' % len(rm_bullets))

            # Unlock new enemies
            if self.enemies_locked and self.iter_count in self.enemies_locked:
                self.enemies_types += self.enemies_locked[self.iter_count]
                self.logger.debug(
                    'Enemies unlock: %s' % self.enemies_locked[self.iter_count]
                )
                del self.enemies_locked[self.iter_count]

            # Enemies spawn
            while len(self.enemies) < self.enemies_max:
                idx = randint(0, len(self.enemies_types)-1)
                enemy_conf = self.enemies_types[idx].copy()
                enemy_conf['world'] = self

                r = enemy_conf['radius']
                x = randint(r, self.screen_width-r)
                y = randint(r, self.screen_height-r)
                dst = sqrt((x - self.hero_x)**2 + (y - self.hero_y)**2)

                # Don't spawn enemies near to hero
                while dst <= self.spawn_dst:
                    x = randint(r, self.screen_width-r)
                    y = randint(r, self.screen_height-r)
                    dst = sqrt((x - self.hero_x)**2 + (y - self.hero_y)**2)

                enemy_conf['pos_x'] = x
                enemy_conf['pos_y'] = y

                enemy_conf['enemy_id'] = self.enemy_id
                self.enemy_id += 1

                enemy = Enemy(**enemy_conf)
                self.enemies.add(enemy)
                self.logger.debug('Enemy spawn: %s' % enemy_conf)

            # +1 to max enemies
            if (self.iter_count+1) % self.enemies_max_iter_step == 0:
                self.enemies_max += 1
                self.logger.debug('+1 max enemies')

            self.update_world_stat()
            self.logger.debug('World stat: %s' % self.world_stat)

            self.logger.debug('Iter %d done' % self.iter_count)
            self.iter_count += 1


class WorldLogger(logging.LoggerAdapter):

    def __init__(self, world):
        self.world = world

        self.__logger = logging.getLogger('npgameworld')
        self.handler = logging.StreamHandler()

        self.formatter = logging.Formatter('%(asctime)s - %(iter_num)s - \
%(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.__logger.addHandler(self.handler)

        self.params = {'iter_num': self.world.iter_count}
        super().__init__(self.__logger, self.params)

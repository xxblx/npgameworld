# -*- coding: utf-8 -*-

from .npc import Hero


class NpGameWorld:

    def __init__(self, screen_width=1024, screen_height=768):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.enemies_spawned = 0
        self.max_enemies = 0
        self.enemies_settings = {}
        self.enemies = set()
        self.hero_bullets = set()

        self.game_over = False
        self.iter_count = 0
        self.enemies_killed = 0

    def init_hero(self, hp=100, radius=15, spd=3, bullet_radius=3,
                  bullet_spd=6, bullet_power=1, reload_iters=5):
        """ Setup and add hero to world """

        self.hero_hp = hp
        self.hero_radius = radius
        self.hero_spd = spd
        self.hero_reload_iters = reload_iters

        self.herp_bul_radius = bullet_radius
        self.hero_bul_spd = bullet_spd
        self.hero_bul_power = bullet_power

        self.hero_x = int(self.screen_width / 2)
        self.hero_y = int(self.screen_height / 2)

        self.hero = Hero(self, self.hero_x, self.hero_y, self.hero_radius,
                         self.hero_spd, self.herp_bul_radius,
                         self.hero_bul_spd, self.hero_bul_power,
                         self.hero_reload_iters)

    def add_enemy(self, hp=1, radius=15, spd=1, unlock=0, power=2,
                  probability=1):
        pass

    def world_gen(self):
        """ Generator for world loop """

        hero_actions = None

        while not self.game_over:
            # TODO: unlock new enemies
            # TODO: increase max enemies count
            # TODO: add new enemies

            hero_iter_damage = 0
            rm_bullets = set()
            rm_enemies = set()

            # TODO: iter process for hero
            hero_actions = yield hero_actions
            if hero_actions:
                pass

            self.hero_x = self.hero.x
            self.hero_y = self.hero.y

            for bullet in self.hero_bullets:
                bullet.iter_process()
                if bullet.border_crossed:
                    rm_bullets.add(bullet)

            for enemy in self.enemies:
                enemy.iter_process()

                if enemy.hit_hero:
                    hero_iter_damage += enemy.power

                if enemy.killed_by is not None:
                    rm_enemies.add(enemy)
                    rm_bullets.add(enemy.killed_by)

            self.enemies_killed += len(rm_enemies)
            self.hero_hp -= hero_iter_damage

            if self.hero_hp <= 0:
                self.game_over = True
                return

            self.hero_bullets.difference_update(rm_bullets)
            self.enemies.difference_update(rm_enemies)

            # TODO: grab stats

            self.iter_count += 1

# -*- coding: utf-8 -*-


class NpGameWorld:

    def __init__(self, screen_width=1024, screen_height=768):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.enemies_spawned = 0
        self.enemies = set()
        self.hero_bullets = set()

        self.game_over = False
        self.iter_count = 0
        self.enemies_killed = 0

    def setup_hero(self, hp=100, radius=15, spd=3, bul_radius=3, bul_spd=6,
                   bul_power=1, reload_iters=5):

        self.hero_hp = hp
        self.hero_radius = radius
        self.hero_spd = spd
        self.hero_reload_iters = reload_iters

        self.herp_buld_radius = bul_radius
        self.hero_bul_spd = bul_spd
        self.hero_bul_power = bul_power

    def setup_enemy(self, hp=1, radius=15, spd=1, unlock=0, probability=1):
        pass

    def world_gen(self):
        """ Generator for world loop """

        hero_actions = None

        while not self.game_over:
            hero_actions = yield hero_actions

            hero_iter_damage = 0
            rm_bullets = set()
            rm_enemies = set()

            # TODO: iter process for hero

            for bullet in self.hero_bullets:
                bullet.iter_process()
                if bullet.border_crossed:
                    rm_bullets.add(bullet)

            for enemy in self.enemies:
                enemy.iter_process()

                if enemy.hit_hero:
                    hero_iter_damage += enemy.power

                if enemy.killed is not None:
                    rm_enemies.add(enemy)

            self.enemies_killed += len(rm_enemies)
            self.hero_hp -= hero_iter_damage

            if self.hero_hp <= 0:
                self.game_over = True
                return

            self.hero_bullets.difference_update(rm_bullets)
            self.enemies.difference_update(rm_enemies)

            # TODO: grab stats

            self.iter_count += 1

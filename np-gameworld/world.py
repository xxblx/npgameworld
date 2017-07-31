# -*- coding: utf-8 -*-


class NpGameWorld:

    hero_x = None
    hero_y = None

    enemies = set()
    hero_bullets = set()

    def __init__(self, screen_width=1024, screen_height=768):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.enemies_spawned = 0

        self.hero_x = None
        self.hero_y = None
        self.hero_hp = 100

        self.enemies = set()
        self.hero_bullets = set()

        self.game_over = False
        self.iter_count = 0
        self.enemies_killed = 0

    def setup_hero(self, hero_hp=100, hero_size=30, hero_spd=3,
                   hero_bul_size=6, hero_bul_spd=6, hero_reload_delay=5):
        self.hero_hp = hero_hp
        self.hero_size = hero_size
        self.hero_spd = hero_spd
        self.hero_bul_spd = hero_bul_spd

        self.hero_radius = self.hero_size / 2

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

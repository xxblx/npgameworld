# -*- coding: utf-8 -*-

from .npc import Hero


class NpGameWorld:

    def __init__(self, screen_width=1024, screen_height=768, start_enemies=3,
                 enemies_max_iter_step=100):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.enemies_in_game = 0
        # Every <enemies_max_iter_step> +1 max enemies
        self.enemies_max_iter_step = enemies_max_iter_step
        self.enemies_max = start_enemies
        self.enemies_locked = {}  # key is unlock level
        self.enemies_types = []  # available unlocked enemies

        self.enemies = set()  # alive enemies objects
        self.hero_bullets = set()  # alive hero's bullets objects

        self.game_over = False
        self.iter_count = 0  # completed iterations counter
        self.enemies_killed = 0

    def init_hero(self, hp=100, radius=15, spd=3, bullet_radius=3,
                  bullet_spd=6, bullet_power=1, reload_iters=5):
        """ Setup and add hero to world """

        self.hero_hp = hp
        self.hero_radius = radius
        self.hero_spd = spd
        # How many iterations hero reloads after one shot
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

    def setup_enemy(self, hp=1, radius=15, spd=1, unlock=0, power=2):
        pass

    def world_gen(self):
        """ Generator for world loop """

        hero_actions = None

        while not self.game_over:

            hero_iter_damage = 0
            rm_bullets = set()
            rm_enemies = set()

            # TODO: iter process for hero
            hero_actions = yield hero_actions
            if hero_actions:
                pass

            self.hero_x = self.hero.x
            self.hero_y = self.hero.y

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

                if enemy.killed_by is not None:
                    rm_enemies.add(enemy)
                    rm_bullets.add(enemy.killed_by)

            self.enemies_killed += len(rm_enemies)
            self.hero_hp -= hero_iter_damage

            if self.hero_hp <= 0:
                self.game_over = True
                return

            # Remove killed objects
            self.hero_bullets.difference_update(rm_bullets)
            self.enemies.difference_update(rm_enemies)

            # Enemies spawn
            while self.enemies_in_game < self.enemies_max:
                # TODO: spawn new enemy
                pass

            # Unlock new enemies
            if self.enemies_locked and self.iter_count in self.enemies_locked:
                self.enemies_types += self.enemies_locked[self.iter_count]
                del self.enemies_locked[self.iter_count]

            # +1 to max enemies
            if (self.iter_count+1) % self.enemies_max_iter_step == 0:
                self.enemies_max += 1

            # TODO: grab stats

            self.iter_count += 1

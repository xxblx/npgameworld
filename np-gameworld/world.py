# -*- coding: utf-8 -*-


class NpGameWorld:

    enemies = set()
    hero_bullets = set()

    def __init__(self, screen_width=1024, screen_height=768):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.enemies_spawned = 0

    def setup_hero(self, hero_hp=100, hero_size=30, hero_spd=3,
                   hero_bul_size=6, hero_bul_spd=6, hero_reload_delay=5):
        self.hero_hp = hero_hp
        self.hero_size = hero_size
        self.hero_spd = hero_spd
        self.hero_bul_spd = hero_bul_spd

#        self.hero_radius = self.hero_size / 2

    def run_world(self):
        self.game_over = False

        while not self.game_over:
            pass

# -*- coding: utf-8 -*-

import numpy as np


class NPC:
    """ Basic class for all NPC - hero and enemies """

    def __init__(self, world, pos_x, pos_y, radius, spd):
        self.__world = world

        self.spd = spd
        self.radius = radius
        self.size = self.radius * 2

        # x, y - cord of npc's circle center
        self.x = pos_x
        self.y = pos_y

        # pad_x, pad_y are cords of left upper corner
        # of rectangle for incircle
        self.pad_x = self.x - self.size / 2
        self.pad_y = self.y - self.size / 2

    @property
    def screen_width(self):
        return self.__world.screen_width

    @property
    def screen_height(self):
        return self.__world.screen_height

    def iter_process(self):
        raise NotImplemented

    def move(self, x_step=0, y_step=0, borders=True):

        # x moving
        if self.pad_x <= 0 or self.pad_x >= self.screen_width - self.size:
            x_step = 0

        elif 0 < self.screen_width - self.pad_x + self.size < self.spd:
            x_step = self.screen_width - self.pad_x + self.size

        elif 0 < self.pad_x < self.spd:
            x_step = -(self.spd - self.pad_x)

        # y moving
        if self.pad_y <= 0 or self.pad_y >= self.screen_height - self.size:
            y_step = 0

        elif 0 < self.screen_height - self.pad_y + self.size < self.spd:
            y_step = self.screen_height - self.pad_y + self.size

        elif 0 < self.pad_y < self.spd:
            y_step = -(self.spd - self.pad_y)

        self.pad_x += x_step
        self.pad_y += y_step
        self.x += x_step
        self.y += y_step


class Hero(NPC):
    pass


class HeroBullet(NPC):
    border_crossed = False

    def move(self):
        self.pad_x += self.spd
        self.pad_y += self.spd
        self.x += self.spd
        self.y += self.spd

    def check_border_cross(self):
        if self.pad_x < 0 or self.pad_x > self.screen_width:
            self.border_crossed = True
        elif self.pad_y < 0 or self.pad_y > self.screen_height:
            self.border_crossed = True

    def iter_process(self):
        self.move()
        self.check_border_cross()


class Enemy(NPC):

    collide_hero = False
    collided_hero_bullet = False

    @property
    def hero_x(self):
        return self.__world.hero_x

    @property
    def hero_y(self):
        return self.__world.hero_y

    @property
    def hero_radius(self):
        return self.__world.hero_radius

    @property
    def hero_bullets_x(self):
        return self.__world.hero_bullets_x

    @property
    def hero_bullets_y(self):
        return self.__world.hero_bullets_y

    def check_hero_bullet_collision(self):
        """
        Check does enemy collides with hero's bullets
        """

        raise NotImplemented

    def check_hero_collision(self):
        """
        Check does enemy collides hero.
        True if distance between centers less or equal sum of radiuses.
        """

        dst = np.sqrt((self.x - self.hero_x)**2 + (self.y - self.hero_y)**2)
        if dst <= self.radius + self.hero_radius:
            self.collide_hero = True

    def iter_process(self):
        self.collide_hero = False

        if self.hero_x > self.x:
            x_step = self.spd
        elif self.hero_x < self.x:
            x_step = -self.spd
        else:
            x_step = 0

        if self.hero_y > self.y:
            y_step = self.spd
        elif self.hero_y < self.y:
            y_step = -self.spd
        else:
            y_step = 0

        self.move(x_step, y_step)

        # TODO: check collisions with hero's bulletrs
        # collided_hero_bullet = True

        if not self.collided_hero_bullet:
            self.check_hero_collision()

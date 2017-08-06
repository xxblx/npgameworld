# -*- coding: utf-8 -*-

from math import sqrt


class NPC:
    """ Basic class for all NPC - hero and enemies """

    def __init__(self, world, pos_x, pos_y, radius, spd):
        self._world = world

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
        return self._world.screen_width

    @property
    def screen_height(self):
        return self._world.screen_height

    def iter_process(self):
        raise NotImplementedError

    def move(self, x_step=0, y_step=0):

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
    """ Hero controlled by player """

    def __init__(self, world, pos_x, pos_y, radius, spd, bullet_radius,
                 bullet_spd, bullet_power):

        super().__init__(world, pos_x, pos_y, radius, spd)

        self.bullet_radius = bullet_radius
        self.bullet_spd = bullet_spd
        self.bullet_power = bullet_power
        self.reload_wait = 0

    def shoot(self, x_target, y_target):
        dst = sqrt((x_target - self.x)**2 + (y_target - self.y)**2)
        steps = dst / self.bullet_spd

        # Bullet will get target if moves with x_step and y_step
        x_step = (x_target - self.x) / steps
        y_step = (y_target - self.y) / steps

        return HeroBullet(self._world, self.x, self.y, self.bullet_radius,
                          self.bullet_spd, self.bullet_power, x_step, y_step)


class HeroBullet(NPC):
    border_crossed = False
    got_enemy = False

    def __init__(self, world, pos_x, pos_y, radius, spd, power,
                 x_step, y_step):
        super().__init__(world, pos_x, pos_y, radius, spd)
        self.power = power
        self.x_step = x_step
        self.y_step = y_step

    def move(self):
        self.pad_x += self.x_step
        self.pad_y += self.y_step
        self.x += self.x_step
        self.y += self.y_step

    def check_border_cross(self):
        if self.pad_x < 0 or self.pad_x > self.screen_width:
            self.border_crossed = True
        elif self.pad_y < 0 or self.pad_y > self.screen_height:
            self.border_crossed = True

    def iter_process(self):
        self.move()
        self.check_border_cross()


class Enemy(NPC):
    hit_hero = False
    killed_by = None

    def __init__(self, world, pos_x, pos_y, radius, spd, power, hp, enemy_id):
        super().__init__(world, pos_x, pos_y, radius, spd)
        self.power = power
        self.hp = hp
        self.enemy_id = enemy_id

    @property
    def hero_x(self):
        return self._world.hero_x

    @property
    def hero_y(self):
        return self._world.hero_y

    @property
    def hero_radius(self):
        return self._world.hero_radius

    @property
    def hero_bullets(self):
        return self._world.hero_bullets

    def check_bullets_collision(self):
        """
        Check does enemy collides with hero's bullets
        """

        for bullet in self.hero_bullets:
            dst = sqrt((self.x - bullet.x)**2 + (self.y - bullet.y)**2)
            if dst <= self.radius + bullet.radius:
                bullet.got_enemy = True

                self.hp -= bullet.power
                if self.hp <= 0:
                    self.killed_by = bullet
                    break

    def check_hero_collision(self):
        """
        Check does enemy collides hero.
        True if distance between centers less or equal sum of radiuses.
        """

        dst = sqrt((self.x - self.hero_x)**2 + (self.y - self.hero_y)**2)
        if dst <= self.radius + self.hero_radius:
            self.hit_hero = True

    def iter_process(self):
        self.hit_hero = False

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
        self.check_bullets_collision()
        self.check_hero_collision()

#coding: utf-8
__author__ = 'gold'
__date__ = '2019/2/17'
__time__ = '23:04'
__filename__ = 'tank.py'


import pygame
import random
from tank.bullet import Bullet
from tank.constants import WINDOWWIDTH,WINDOWHEIGHT,PANEL_BOTTOM,PANEL_LEFT,PANEL_TOP,PANEL_RIGHT


class PlayerTank(pygame.sprite.Sprite):
    '''
	the player's tank class
    '''
    def __init__(self, player):
        '''
		initial the player's tank object
        :param player: int,1 or 2,representing the player's code.
		'''
        super(PlayerTank,self).__init__()
        # pygame.sprite.Sprite.__init__(self)

        self.player = player
        # different player has different tank
        if player == 1:
            self.tanks = ['./images/myTank/tank_T1_0.png', './images/myTank/tank_T1_1.png', './images/myTank/tank_T1_2.png']
        elif player == 2:
            self.tanks = ['./images/myTank/tank_T2_0.png', './images/myTank/tank_T2_1.png', './images/myTank/tank_T2_2.png']
        else:
            raise ValueError('myTank class -> player value error.')

        # the level of the tank
        self.level = 0
        # load the tank image,use 2 images for the visual effect.
        self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha()
        self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
        self.rect = self.tank_0.get_rect()
        # the protect mask
        self.protected_mask = pygame.image.load('./images/others/protect.png').convert_alpha()
        self.protected_mask1 = self.protected_mask.subsurface((0, 0), (48, 48))
        self.protected_mask2 = self.protected_mask.subsurface((48, 0), (48, 48))
        # initially the tank's direction.
        self.direction_x, self.direction_y = 0, -1
        # TODO ,I must come up a better way to make the parameters not so fixed.
        if player == 1:
            self.rect.left, self.rect.top = PANEL_LEFT + 24 * 8, PANEL_LEFT + 24 * 24
        elif player == 2:
            self.rect.left, self.rect.top = PANEL_LEFT + 24 * 16, PANEL_LEFT + 24 * 24
        else:
            raise ValueError('myTank class -> player value error.')
        # the tank's speed
        self.speed = 3
        # indicate if the tank is alive or not
        self.being = True
        # the player's life count
        self.life = 3
        # if the tank is in a protection status or not.
        self.protected = False
        # the player's tank bullet.
        self.bullet = Bullet()

    def shoot(self):
        '''
		the tank's shoot method.
		:return:
		'''
        self.bullet.being = True
        self.bullet.turn(self.direction_x, self.direction_y)
        if self.direction_x == 0 and self.direction_y == -1:
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.bottom = self.rect.top - 1
        elif self.direction_x == 0 and self.direction_y == 1:
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.top = self.rect.bottom + 1
        elif self.direction_x == -1 and self.direction_y == 0:
            self.bullet.rect.right = self.rect.left - 1
            self.bullet.rect.top = self.rect.top + 20
        elif self.direction_x == 1 and self.direction_y == 0:
            self.bullet.rect.left = self.rect.right + 1
            self.bullet.rect.top = self.rect.top + 20
        else:
            raise ValueError('myTank class -> direction value error.')
        if self.level == 0:
            self.bullet.speed = 8
            self.bullet.stronger = False
        elif self.level == 1:
            self.bullet.speed = 12
            self.bullet.stronger = False
        elif self.level == 2:
            self.bullet.speed = 12
            self.bullet.stronger = True
        elif self.level == 3:
            self.bullet.speed = 16
            self.bullet.stronger = True
        else:
            raise ValueError('myTank class -> level value error.')

    def up_level(self):
        '''
		up the tank's level
		:param self:
		:return:
		'''
        if self.level < 3:
            self.level += 1
        try:
            self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha()
        except:
            self.tank = pygame.image.load(self.tanks[-1]).convert_alpha()

    def down_level(self):
        '''
		down the tank's level
		:param self:
		:return:
		'''
        if self.level > 0:
            self.level -= 1
        self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha()

    # TODO
    def move(self):
        '''
		this is my own move function, i think i can combine all the possible movement in a function.
		:return:
		'''
        pass

    def move_up(self, tankGroup, brickGroup, ironGroup, myhome):
        '''
		judge if the tank can go up.
		:param self:
		:param tankGroup:
		:param brickGroup:
		:param ironGroup:
		:param myhome:
		:return:bool,if the tank can go up or not.
		'''
        self.direction_x, self.direction_y = 0, -1
        self.rect = self.rect.move(0, self.speed*self.direction_y)
        self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
        # indicate if the tank can move up or not.
        is_move = True
        # the tank arrived at the panel's most height.
        if self.rect.top < PANEL_TOP:
            self.rect = self.rect.move(0, self.speed*(-self.direction_y))
            is_move = False
        # the tank collided with some fixed objects.
        if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
            pygame.sprite.spritecollide(self, ironGroup, False, None):
            self.rect = self.rect.move(0, self.speed*(-self.direction_y))
            is_move = False
        # collide with other tanks
        if pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(0, self.speed*(-self.direction_y))
            is_move = False
        # collide with the base camp.
        if pygame.sprite.collide_rect(self, myhome):
            self.rect = self.rect.move(0, self.speed*(-self.direction_y))
            is_move = False
        return is_move

    def move_down(self, tankGroup, brickGroup, ironGroup, myhome):
        '''
		judge if the tank can go down.
		:param self:
		:param tankGroup:
		:param brickGroup:
		:param ironGroup:
		:param myhome:
		:return: bool
		'''
        self.direction_x, self.direction_y = 0, 1

        self.rect = self.rect.move(0, self.speed*self.direction_y)
        self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
        # if the tank can go down.
        is_move = True
        # the tank arrived at the bottom of the panel.
        if self.rect.bottom > PANEL_BOTTOM:
            self.rect = self.rect.move(0, self.speed*(-self.direction_y))
            is_move = False
        # collide with the fixed obstacles.
        if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
            pygame.sprite.spritecollide(self, ironGroup, False, None):
            self.rect = self.rect.move(0, self.speed*(-self.direction_y))
            is_move = False
        # collide with other tanks.
        if pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(0, self.speed*(-self.direction_y))
            is_move = False
        # collide with the base camp.
        if pygame.sprite.collide_rect(self, myhome):
            self.rect = self.rect.move(0, self.speed*(-self.direction_y))
            is_move = False
        return is_move

    def move_left(self, tankGroup, brickGroup, ironGroup, myhome):
        '''
		judge if the tank can go left
		:param self:
		:param tankGroup:
		:param brickGroup:
		:param ironGroup:
		:param myhome:
		:return: bool
		'''
        self.direction_x, self.direction_y = -1, 0
        self.rect = self.rect.move(self.speed*self.direction_x, 0)
        self.tank_0 = self.tank.subsurface((0, 96), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 96), (48, 48))

        is_move = True
        # the tank arrived at the panel's most left side.
        if self.rect.left < PANEL_LEFT:
            self.rect = self.rect.move(self.speed*(-self.direction_x), 0)
            is_move = False
        # collide with fixed obstacles.
        if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
            pygame.sprite.spritecollide(self, ironGroup, False, None):
            self.rect = self.rect.move(self.speed*(-self.direction_x), 0)
            is_move = False
        # collide with other tanks.
        if pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(self.speed*(-self.direction_x), 0)
            is_move = False
        # collide with the base camp.
        if pygame.sprite.collide_rect(self, myhome):
            self.rect = self.rect.move(self.speed*(-self.direction_x), 0)
            is_move = False
        return is_move

    def move_right(self, tankGroup, brickGroup, ironGroup, myhome):
        '''
		judge if the tank can go right
		:param self:
		:param tankGroup:
		:param brickGroup:
		:param ironGroup:
		:param myhome:
		:return: bool
		'''
        self.direction_x, self.direction_y = 1, 0

        self.rect = self.rect.move(self.speed*self.direction_x, 0)
        self.tank_0 = self.tank.subsurface((0, 144), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 144), (48, 48))

        is_move = True
        # arrived at the panel's rightmost side.
        if self.rect.right > PANEL_RIGHT:
            self.rect = self.rect.move(self.speed*(-self.direction_x), 0)
            is_move = False
        # collide with other fixed obstacles.
        if pygame.sprite.spritecollide(self, brickGroup, False, None) or \
            pygame.sprite.spritecollide(self, ironGroup, False, None):
            self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
            is_move = False
        # collide with ohter tanks.
        if pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
            is_move = False
        # collide with the base camp.
        if pygame.sprite.collide_rect(self, myhome):
            self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
            is_move = False
        return is_move

    def reset(self):
        '''
		reset the player's tank object.r
		:param self:
		:return:
		'''
        self.level = 0
        self.protected = False
        self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha()
        self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
        self.rect = self.tank_0.get_rect()
        self.direction_x, self.direction_y = 0, -1
        if self.player == 1:
            self.rect.left, self.rect.top = PANEL_LEFT + 24 * 8, PANEL_LEFT + 24 * 24
        elif self.player == 2:
            self.rect.left, self.rect.top = PANEL_LEFT + 24 * 16, PANEL_LEFT + 24 * 24
        else:
            raise ValueError('myTank class -> player value error.')
        self.speed = 3


class EnemyTank(pygame.sprite.Sprite):
    '''
	enemy tank class
	'''
    def __init__(self, x=None, kind=None, is_red=None):
        '''
		:param x:
		:param kind:
		:param is_red:
		'''
        super(EnemyTank,self).__init__()
        # pygame.sprite.Sprite.__init__(self)

		# the new tank's sound
        self.born = True
        self.times = 90
        # the enemy tank's code
        if kind is None:
            self.kind = random.randint(0, 3)
        else:
            self.kind = kind
        # all the enemy tanks
        self.tanks1 = ['./images/enemyTank/enemy_1_0.png', './images/enemyTank/enemy_1_1.png', './images/enemyTank/enemy_1_2.png', './images/enemyTank/enemy_1_3.png']
        self.tanks2 = ['./images/enemyTank/enemy_2_0.png', './images/enemyTank/enemy_2_1.png', './images/enemyTank/enemy_2_2.png', './images/enemyTank/enemy_2_3.png']
        self.tanks3 = ['./images/enemyTank/enemy_3_0.png', './images/enemyTank/enemy_3_1.png', './images/enemyTank/enemy_3_2.png', './images/enemyTank/enemy_3_3.png']
        self.tanks4 = ['./images/enemyTank/enemy_4_0.png', './images/enemyTank/enemy_4_1.png', './images/enemyTank/enemy_4_2.png', './images/enemyTank/enemy_4_3.png']
        self.tanks = [self.tanks1, self.tanks2, self.tanks3, self.tanks4]
        # red means that the enemy tank has food
        if is_red is None:
            self.is_red = random.choice((True, False, False, False, False))
        else:
            self.is_red = is_red
        # red tank has more blood.
        if self.is_red:
            self.color = 3
        else:
            self.color = random.randint(0, 2)
        # the blood amount.
        self.blood = self.color

        self.tank = pygame.image.load(self.tanks[self.kind][self.color]).convert_alpha()
        self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
        self.rect = self.tank_0.get_rect()
        # 坦克位置
        if x is None:
            self.x = random.randint(0, 2)
        else:
            self.x = x
        self.rect.left, self.rect.top = PANEL_LEFT + self.x * 12 * 24, PANEL_LEFT
        # indicate if the tank can move
        self.can_move = True
        # the tank's speed
        self.speed = max(3 - self.kind, 1)
        # direction
        self.direction_x, self.direction_y = 0, 1
        # alive or not
        self.being = True
        # bullet
        self.bullet = Bullet()

    def shoot(self):
        '''
        the tank's bullet
        :return:
        '''
        self.bullet.being = True
        self.bullet.turn(self.direction_x, self.direction_y)
        if self.direction_x == 0 and self.direction_y == -1:
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.bottom = self.rect.top - 1
        elif self.direction_x == 0 and self.direction_y == 1:
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.top = self.rect.bottom + 1
        elif self.direction_x == -1 and self.direction_y == 0:
            self.bullet.rect.right = self.rect.left - 1
            self.bullet.rect.top = self.rect.top + 20
        elif self.direction_x == 1 and self.direction_y == 0:
            self.bullet.rect.left = self.rect.right + 1
            self.bullet.rect.top = self.rect.top + 20
        else:
            raise ValueError('enemyTank class -> direction value error.')

    def move(self, tankGroup, brickGroup, ironGroup, myhome):
        '''
		judge if the tank can move or not
		:param tankGroup:
		:param brickGroup:
		:param ironGroup:
		:param myhome:
		:return: bool
		'''
        self.rect = self.rect.move(self.speed*self.direction_x, self.speed*self.direction_y)
        is_move = True
        if self.direction_x == 0 and self.direction_y == -1:
            self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
            self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
            if self.rect.top < PANEL_TOP:
                self.rect = self.rect.move(0, self.speed*(-self.direction_y))
                self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
                is_move = False
        elif self.direction_x == 0 and self.direction_y == 1:
            self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
            self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
            if self.rect.bottom > PANEL_BOTTOM:
                self.rect = self.rect.move(0, self.speed*(-self.direction_y))
                self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
                is_move = False
        elif self.direction_x == -1 and self.direction_y == 0:
            self.tank_0 = self.tank.subsurface((0, 96), (48, 48))
            self.tank_1 = self.tank.subsurface((48, 96), (48, 48))
            if self.rect.left < PANEL_LEFT:
                self.rect = self.rect.move(self.speed*(-self.direction_x), 0)
                self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
                is_move = False
        elif self.direction_x == 1 and self.direction_y == 0:
            self.tank_0 = self.tank.subsurface((0, 144), (48, 48))
            self.tank_1 = self.tank.subsurface((48, 144), (48, 48))
            if self.rect.right > PANEL_RIGHT:
                self.rect = self.rect.move(self.speed*(-self.direction_x), 0)
                self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
                is_move = False
        else:
            raise ValueError('enemyTank class -> direction value error.')
        if pygame.sprite.spritecollide(self, brickGroup, False, None) \
            or pygame.sprite.spritecollide(self, ironGroup, False, None) \
            or pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
            self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
            is_move = False
        if pygame.sprite.collide_rect(self, myhome):
            self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
            self.direction_x, self.direction_y = random.choice(([0, 1], [0, -1], [1, 0], [-1, 0]))
            is_move = False
        return is_move

    def reload(self):
        '''
        reload the enemy tank
        :return:
        '''
        self.tank = pygame.image.load(self.tanks[self.kind][self.color]).convert_alpha()
        self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
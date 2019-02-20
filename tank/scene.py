#coding: utf-8
__author__ = 'gold'
__date__ = '2019/2/20'
__time__ = '19:56'
__filename__ = 'scene.py'

import pygame
import random


class Brick(pygame.sprite.Sprite):
    '''
    the brick class
    '''
    def __init__(self):
        #pygame.sprite.Sprite.__init__(self)
        super(Brick,self).__init__()
        self.brick = pygame.image.load('./images/scene/brick.png')
        self.rect = self.brick.get_rect()
        self.being = False


class Iron(pygame.sprite.Sprite):
    '''
    the protect for the base camp.
    '''
    def __init__(self):
        # pygame.sprite.Sprite.__init__(self)
        super(Iron,self).__init__()
        self.iron = pygame.image.load('./images/scene/iron.png')
        self.rect = self.iron.get_rect()
        self.being = False


class Ice(pygame.sprite.Sprite):
    '''
    what is this class?
    '''
    def __init__(self):
        # pygame.sprite.Sprite.__init__(self)
        super(Ice,self).__init__()
        self.ice = pygame.image.load('./images/scene/ice.png')
        self.rect = self.ice.get_rect()
        self.being = False


class River(pygame.sprite.Sprite):
    '''
    river class,but what this?
    '''
    def __init__(self, kind=None):
        # pygame.sprite.Sprite.__init__(self)
        super(River,self).__init__()
        if kind is None:
            self.kind = random.randint(0, 1)
        self.rivers = ['./images/scene/river1.png', './images/scene/river2.png']
        self.river = pygame.image.load(self.rivers[self.kind])
        self.rect = self.river.get_rect()
        self.being = False


class Tree(pygame.sprite.Sprite):
    '''
    tree class
    '''
    def __init__(self):
        # pygame.sprite.Sprite.__init__(self)
        super().__init__()
        self.tree = pygame.image.load('./images/scene/tree.png')
        self.rect = self.tree.get_rect()
        self.being = False


class Map():
    '''
    map class
    '''
    def __init__(self, stage):
        self.brickGroup = pygame.sprite.Group()
        self.ironGroup = pygame.sprite.Group()
        self.iceGroup = pygame.sprite.Group()
        self.riverGroup = pygame.sprite.Group()
        self.treeGroup = pygame.sprite.Group()
        if stage == 1:
            self.stage1()
        elif stage == 2:
            self.stage2()

    def stage1(self):
        '''
        map 1
        '''
        for x in [2, 3, 6, 7, 18, 19, 22, 23]:
            for y in [2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22, 23]:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brick.being = True
                self.brickGroup.add(self.brick)
        for x in [10, 11, 14, 15]:
            for y in [2, 3, 4, 5, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19, 20]:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brick.being = True
                self.brickGroup.add(self.brick)
        for x in [4, 5, 6, 7, 18, 19, 20, 21]:
            for y in [13, 14]:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brick.being = True
                self.brickGroup.add(self.brick)
        for x in [12, 13]:
            for y in [16, 17]:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brick.being = True
                self.brickGroup.add(self.brick)
        for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
            self.brick = Brick()
            self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
            self.brick.being = True
            self.brickGroup.add(self.brick)
        for x, y in [(0, 14), (1, 14), (12, 6), (13, 6), (12, 7), (13, 7), (24, 14), (25, 14)]:
            self.iron = Iron()
            self.iron.rect.left, self.iron.rect.top = 3 + x * 24, 3 + y * 24
            self.iron.being = True
            self.ironGroup.add(self.iron)

    def stage2(self):
        '''
        state 2
        '''
        for x in [2, 3, 6, 7, 18, 19, 22, 23]:
            for y in [2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22, 23]:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brick.being = True
                self.brickGroup.add(self.brick)
        for x in [10, 11, 14, 15]:
            for y in [2, 3, 4, 5, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19, 20]:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brick.being = True
                self.brickGroup.add(self.brick)
        for x in [4, 5, 6, 7, 18, 19, 20, 21]:
            for y in [13, 14]:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brick.being = True
                self.brickGroup.add(self.brick)
        for x in [12, 13]:
            for y in [16, 17]:
                self.brick = Brick()
                self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
                self.brick.being = True
                self.brickGroup.add(self.brick)
        for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
            self.brick = Brick()
            self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
            self.brick.being = True
            self.brickGroup.add(self.brick)
        for x, y in [(0, 14), (1, 14), (12, 6), (13, 6), (12, 7), (13, 7), (24, 14), (25, 14)]:
            self.iron = Iron()
            self.iron.rect.left, self.iron.rect.top = 3 + x * 24, 3 + y * 24
            self.iron.being = True
            self.ironGroup.add(self.iron)

    def protect_home(self):
        for x, y in [(11, 23), (12, 23), (13, 23), (14, 23), (11, 24), (14, 24), (11, 25), (14, 25)]:
            self.iron = Iron()
            self.iron.rect.left, self.iron.rect.top = 3 + x * 24, 3 + y * 24
            self.iron.being = True
            self.ironGroup.add(self.iron)

    # TODO
    def createObstacles(self):
        '''
        this method is used to create the map's obstacke.
        :return:
        '''
        pass
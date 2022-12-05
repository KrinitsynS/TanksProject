import pygame
import time
import random

pygame.init()
size = 650, 500
screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.HWSURFACE)
pygame.display.set_caption('test')
clock = pygame.time.Clock()
color = 0, 0, 0
color2 = 0, 255, 0

initbase = True
basehp = 2


class Base:
    def __init__(self, basehp):
        self.basehp = basehp
        initbase = False

    def destroy(self):
        if self.basehp == 0:
            base = dbase


class Shoot:
    def __init__(self, pos1, pos2, orient, sight):
        self.x = pos1
        self.y = pos2
        self.orient = orient
        self.speed = 2
        self.damage = 15
        self.sight = sight
        self.rect = pygame.Rect(self.x * 2 + 5, self.y * 2 + 5, 10, 10)


    def step(self):
        if self.orient == 1:
            self.y -= self.speed
        elif self.orient == 2:
            self.y += self.speed
        elif self.orient == 3:
            self.x -= self.speed
        elif self.orient == 4:
            self.x += self.speed
        self.rect = pygame.Rect(self.x * 2 + 5, self.y * 2 + 5, 10, 10)

    def render(self, screen):
        if self.orient == 1:
            screen.blit(bullet1, (self.x * 2, self.y * 2))
        elif self.orient == 2:
            screen.blit(bullet2, (self.x * 2, self.y * 2))
        elif self.orient == 3:
            screen.blit(bullet3, (self.x * 2, self.y * 2))
        elif self.orient == 4:
            screen.blit(bullet4, (self.x * 2, self.y * 2))


class Player:
    def __init__(self, pos1, pos2):
        self.ggx = pos1 * 10
        self.ggy = pos2 * 10
        self.orient = 1
        self.hp = 25
        self.lives = 3
        self.move = 0
        self.ggu = ggu
        self.ggd = pygame.transform.rotate(self.ggu, 180)
        self.ggl = pygame.transform.rotate(self.ggu, 90)
        self.ggr = pygame.transform.rotate(self.ggu, 270)
        self.gg = self.ggu
        self.wall = 0
        self.rect = pygame.Rect(self.ggx * 2, self.ggy * 2, 20, 20)
        self.power = 2


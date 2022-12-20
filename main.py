import pygame
from random import randint
from Bonus import *
from world_map_gen import *
from menu import *
pygame.init()

FPS = 30
TILE = 16

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

fontUI = pygame.font.Font(None, 30)

imgBrick = pygame.image.load('images/images_map/block_brick.png')
imgWater = pygame.image.load('images/images_map/block_water.png')
imgForest = pygame.image.load('images/images_map/block_forest.png')
imgSand = pygame.image.load('images/images_map/block_sand.png')
imgGrass = pygame.image.load('images/images_map/block_grass.png')

imgTanks = [
    pygame.image.load('images/tank1.png'),
    pygame.image.load('images/tank2.png'),
    pygame.image.load('images/tank3.png'),
    pygame.image.load('images/tank4.png'),
    pygame.image.load('images/tank5.png'),
    pygame.image.load('images/tank6.png'),
    pygame.image.load('images/tank7.png'),
    pygame.image.load('images/tank8.png'),
]
imgBangs = [
    pygame.image.load('images/bang1.png'),
    pygame.image.load('images/bang2.png'),
    pygame.image.load('images/bang3.png'),
]
imgBonuses = [
    pygame.image.load('images/bonus_star.png'),
    pygame.image.load('images/bonus_tank.png'),
]

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]

MOVE_SPEED = [1, 2, 2, 1, 2, 3, 3, 2]
BULLET_SPEED = [4, 5, 6, 5, 5, 5, 6, 7]
BULLET_DAMAGE = [1, 1, 2, 3, 2, 2, 3, 4]
SHOT_DELAY = [60, 50, 30, 40, 30, 25, 25, 30]


class UI:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        i = 0
        for obj in objects:
            if obj.type == 'tank':
                pygame.draw.rect(window, obj.color, (5 + i * 70, 5, 22, 22))

                text = fontUI.render(str(obj.rank), 1, 'black')
                rect = text.get_rect(center=(5 + i * 70 + 11, 5 + 11))
                window.blit(text, rect)

                text = fontUI.render(str(obj.hp), 1, obj.color)
                rect = text.get_rect(center=(5 + i * 70 + 32, 5 + 11))
                window.blit(text, rect)
                i += 1

'Tank class'
class Tank:
    def __init__(self, color, px, py, direct, keyList):
        objects.append(self)
        self.type = 'tank'

        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.hp = 8
        self.shotTimer = 0

        self.moveSpeed = 2
        self.shotDelay = 60
        self.bulletSpeed = 5
        self.bulletDamage = 1

        self.keyLEFT = keyList[0]
        self.keyRIGHT = keyList[1]
        self.keyUP = keyList[2]
        self.keyDOWN = keyList[3]
        self.keySHOT = keyList[4]

        self.rank = 0
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.image = pygame.transform.rotate(imgTanks[self.rank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width() - 5, self.image.get_height() - 5))
        self.rect = self.image.get_rect(center=self.rect.center)

        self.moveSpeed = MOVE_SPEED[self.rank]
        self.shotDelay = SHOT_DELAY[self.rank]
        self.bulletSpeed = BULLET_SPEED[self.rank]
        self.bulletDamage = BULLET_DAMAGE[self.rank]

        oldX, oldY = self.rect.topleft
        if keys[self.keyLEFT]:
            self.rect.x -= self.moveSpeed
            self.direct = 3
        elif keys[self.keyRIGHT]:
            self.rect.x += self.moveSpeed
            self.direct = 1
        elif keys[self.keyUP]:
            self.rect.y -= self.moveSpeed
            self.direct = 0
        elif keys[self.keyDOWN]:
            self.rect.y += self.moveSpeed
            self.direct = 2

        for obj in objects:
            if obj != self and (obj.type == 'block' or obj.type == 'forest') and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY

        if keys[self.keySHOT] and self.shotTimer == 0:
            dx = DIRECTS[self.direct][0] * self.bulletSpeed
            dy = DIRECTS[self.direct][1] * self.bulletSpeed
            Bullet(self, self.rect.centerx, self.rect.centery, dx, dy, self.bulletDamage)
            self.shotTimer = self.shotDelay

        if self.shotTimer > 0:
            self.shotTimer -= 1

    def draw(self):
        window.blit(self.image, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)
            print(self.color, 'dead')

'down there was the bullet class'
class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage):
        bullets.append(self)
        self.parent = parent
        self.px, self.py = px, py
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        self.px += self.dx
        self.py += self.dy

        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.type != 'bang' and obj.type != 'bonus' and obj.type != 'water' and obj.type != 'sand':
                    if obj.rect.collidepoint(self.px, self.py):
                        obj.damage(self.damage)
                        bullets.remove(self)
                        Bang(self.px, self.py)
                        break

    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)

'down there was a Bang class'
class Bang:
    def __init__(self, px, py):
        objects.append(self)
        self.type = 'bang'

        self.px, self.py = px, py
        self.frame = 0

    def update(self):
        self.frame += 0.2
        if self.frame >= 3:
            objects.remove(self)

    def draw(self):
        image = imgBangs[int(self.frame)]
        rect = image.get_rect(center=(self.px, self.py))
        window.blit(image, rect)

'blocks clases'
class Block:
    def __init__(self, px, py, size, type_x):
        objects.append(self)
        self.type = type_x

        self.rect = pygame.Rect(px, py, size, size)
        self.hp = 1

    def update(self):
        pass

    def draw(self, img):
        window.blit(img, self.rect)

    def damage(self, value):
        self.hp -= value
        if self.hp <= 0:
            objects.remove(self)

'Bonus class'
class Bonus:
    def __init__(self, px, py, bonusNum):
        objects.append(self)
        self.type = 'bonus'

        self.image = imgBonuses[bonusNum]
        self.rect = self.image.get_rect(center=(px, py))

        self.timer = 600
        self.bonusNum = bonusNum

    def update(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            objects.remove(self)

        for obj in objects:
            if obj.type == 'tank' and self.rect.colliderect(obj.rect):
                if self.bonusNum == 0:
                    if obj.rank < len(imgTanks) - 1:
                        obj.rank += 1
                        objects.remove(self)
                        break
                elif self.bonusNum == 1:
                    obj.hp += 1
                    objects.remove(self)
                    break

    def draw(self):
        if self.timer % 30 < 15:
            window.blit(self.image, self.rect)


last_color = ""
while True:
    bullets = []
    objects = []
    Tank('blue', randint(100,400), randint(HEIGHT//4,HEIGHT), 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE))
    Tank('red', randint(510,800) - 300, randint(HEIGHT//4,HEIGHT), 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RETURN))

    gen_all(50, WIDTH // TILE, HEIGHT // TILE)
    with open('map_world.txt', 'r') as f:
        n = 0
        for s in f.readlines():
            for m in range(len(s) - 1):
                k = int(s[m])
                if k == 0:
                    Block(n * TILE, m * TILE, TILE, 'water')
                elif k == 2:
                    Block(n * TILE, m * TILE, TILE, 'forest')
                elif k == 3:
                    Block(n * TILE, m * TILE, TILE, 'sand')
                elif k == 4:
                    Block(n * TILE, m * TILE, TILE, 'block')
            n += 1
    bonusTimer = 180
    ui = UI()
    
    menu = True
    play = False
    menu, play = main_menu(menu, play, last_color)
    if not play:
        break
    last_color = ""
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
        keys = pygame.key.get_pressed()

        if bonusTimer > 0:
            bonusTimer -= 1
        else:
            Bonus(randint(50, WIDTH - 50), randint(50, HEIGHT - 50), randint(0, len(imgBonuses) - 1))
            bonusTimer = randint(120, 240)

        for bullet in bullets:
            bullet.update()
        for obj in objects:
            obj.update()
        ui.update()

        window.blit(imgGrass, pygame.Rect(0, 0, WIDTH, HEIGHT))
        
        for obj in objects:
            if type(obj) == Block:
                if obj.type == 'water':
                    obj.draw(imgWater)
                elif obj.type == 'forest':
                    obj.draw(imgForest)
                elif obj.type == 'sand':
                    obj.draw(imgSand)
                elif obj.type == 'block':
                    obj.draw(imgBrick)
        for bullet in bullets:
            bullet.draw()
        tanks = 0
        last_color = ""
        for obj in objects:
            if type(obj) != Block:
                obj.draw()
            if type(obj) == Tank:
                tanks += 1
                last_color = obj.color
        if tanks < 2:
            play = False
        else:
            last_color = ""
        ui.draw()
        pygame.display.update()
        clock.tick(FPS)


pygame.quit()

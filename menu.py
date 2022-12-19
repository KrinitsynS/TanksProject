import pygame
import pygame.font
from pygame.draw import *
pygame.init()

BLACK = (0, 0, 0)
YELLOW = 0xFFC91F
RED = 0xFF0000
WIDTH, HEIGHT = 800, 600

def main_menu(menu, play):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    keys = ['start', 'authors', 'quit']
    item_keys = 0
    active_key = 'start'
    font = pygame.font.Font(None, 72)
    
    text1 = font.render('start', True, YELLOW)
    text1_e = font.render('start', True, RED)
    place1 = text1.get_rect(center=(WIDTH // 2, 50))
    place1_e = text1_e.get_rect(center=(WIDTH // 2, 50))
    
    text2 = font.render('authors', True, YELLOW)
    text2_e = font.render('authors', True, RED)
    place2 = text2.get_rect(center=(WIDTH // 2, 100))
    place2_e = text2_e.get_rect(center=(WIDTH // 2, 100))
    
    text3 = font.render('quit', True, YELLOW)
    text3_e = font.render('quit', True, RED)
    place3 = text3.get_rect(center=(WIDTH // 2, 150))
    place3_e = text3_e.get_rect(center=(WIDTH // 2, 150))
    
    text4 = font.render('semen and cumstantin', True, YELLOW)
    place4 = text3.get_rect(center=(WIDTH // 2 - 200, 250))
    F = False
    while menu:
        screen.fill(BLACK)
        buttons = pygame.key.get_pressed()
        if buttons[pygame.K_UP]:
            item_keys += 2
            item_keys %= 3
            active_key = keys[item_keys]
            pygame.time.wait(200)
        elif buttons[pygame.K_DOWN]:
            item_keys += 1
            item_keys %= 3
            active_key = keys[item_keys]
            pygame.time.wait(200)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                play = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if active_key == 'start':
                        menu = False
                        play = True
                        return menu, play
                    elif active_key == 'authors':
                        if F:
                            F = False
                        else:
                            F = True
                    elif active_key == 'quit':
                        menu = False
                        play = False
                        return menu, play
        
        if item_keys == 0:
            screen.blit(text1_e, place1_e)
            screen.blit(text2, place2)
            screen.blit(text3, place3)
        elif item_keys == 1:
            screen.blit(text1, place1)
            screen.blit(text2_e, place2_e)
            screen.blit(text3, place3)
        elif item_keys == 2:
            screen.blit(text1, place1)
            screen.blit(text2, place2)
            screen.blit(text3_e, place3_e)
        if F:
            screen.blit(text4, place4)
        pygame.display.update()


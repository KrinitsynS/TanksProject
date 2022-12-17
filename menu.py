import pygame

def main_menu(menu, play):
    screen = pygame.display.set_mode((LIMX, LIMY))
    keys = ['start', 'settings', 'quit']
    item_keys = 0
    active_key = 'start'
    while menu:
        screen.fill(WHITE)
        buttons = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                play = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_enter:
                    if active_key == 'start':
                        menu = False
                        play = True
                    elif active_key == 'settings':
                        continue
                    elif active_key == 'quit':
                        menu = False
                        play = False
        if buttons == pygame.K_UP:
            item_keys += 2
            item_keys %= 3
            active_key = keys[item_keys]
    

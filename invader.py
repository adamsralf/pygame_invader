"""A short Pygame test program 

This short program checks if you have installed pygame 
and that your environment is set up properly.
"""
import pygame
import os

if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"   # left, top corner of the window
    pygame.init()                                   # start PyGame

    screen = pygame.display.set_mode((600, 400))    # create an window
    clock = pygame.time.Clock()                     # start the clock

    running = True                                  # main loop flag
    while running:                                  # main loop
        clock.tick(60)                              # slow down to 1/60 sec
        for event in pygame.event.get():            # event handle
            if event.type == pygame.QUIT:
                running = False
        screen.fill((255, 255, 255))                # fill the screen
        pygame.display.flip()                       # flip doublebuffer

    pygame.quit()                                   # stop PyGame

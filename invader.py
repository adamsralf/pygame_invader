"""A Space Invader variant.
"""
import pygame
import os

class Settings:
    """Project global informations.

    This static class contains informations that 
    are used on many places in the project.
    """
    window_width = 1000
    window_height = 600
    window_border = 10
    enemy_dist = 20
    enemy_nof_cols = 13



if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    pygame.init()

    screen = pygame.display.set_mode((Settings.window_width, Settings.window_height))
    clock = pygame.time.Clock()

    # Loading and scaling the background image
    background_image = pygame.image.load("images/background03.png")
    background_image = pygame.transform.scale(background_image, (Settings.window_width, Settings.window_height))
    background_rect = background_image.get_rect()
    
    # Loading, scaling positioning the defender image
    defender_image = pygame.image.load("images/defender01.png")
    defender_image = pygame.transform.scale(defender_image, (30,30))
    defender_rect = defender_image.get_rect()
    defender_rect.centerx = Settings.window_width // 2
    defender_rect.bottom = Settings.window_height - Settings.window_border

    # Loading and scaling one of the enemy images
    enemy_image = pygame.image.load("images/alienbig0101.png")
    enemy_image = pygame.transform.scale(enemy_image, (50,45))

    # Computing the postions of the many enemy images
    enemy_rect = []
    for rowindex in range(0, 2):
        for colindex in range(0, Settings.enemy_nof_cols):
            rect =  enemy_image.get_rect()
            newx = Settings.window_border + (rect.width  + Settings.enemy_dist) * colindex
            newy = Settings.window_border + (rect.height + Settings.enemy_dist) * rowindex
            rect.move_ip(newx, newy)
            enemy_rect.append(rect)


    running = True 
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        # blitting the background
        screen.blit(background_image, (background_rect.left, background_rect.top))
        # blitting the enemies
        for colindex in range(0, len(enemy_rect)):
            screen.blit(enemy_image, (enemy_rect[colindex].left, enemy_rect[colindex].top))
        # blitting the defender
        screen.blit(defender_image, (defender_rect.left, defender_rect.top))
        pygame.display.flip()

    pygame.quit()

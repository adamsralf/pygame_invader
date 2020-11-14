"""A Space Invader variant.
"""
import pygame
from pygame.constants import (
    QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_ESCAPE, K_SPACE)
import os
from random import randint


class Settings:
    """Project global informations.

    This static class contains informations that 
    are used on many places in the project.
    """
    window_width = 1000
    window_height = 650
    window_border = 10
    enemy_bottom_border = window_height - 80
    enemy_nof_cols = 13
    file_path = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(file_path, "images")
    score = (100, 50, 10)
    max_bombs = 6
    max_rockets = 6


class Background(object):
    """Bitmap class to managethe baground of the game.
    """

    def __init__(self, filename):
        """Constructor

        Loading and scaling the background image.
        Args:
            filename (string): name (without path) of the background bitmap
        """
        self.image = pygame.image.load(
            os.path.join(Settings.image_path, filename))
        self.image = pygame.transform.scale(
            self.image, (Settings.window_width, Settings.window_height)).convert()
        self.rect = self.image.get_rect()

    def draw(self, screen):
        """Draws the bitmap on a surface (screen).

        Args:
            screen (python.Surface): surface object - usally the screen.
        """
        screen.blit(self.image, self.rect)


class Defender(pygame.sprite.Sprite):
    """Defender sprite class.
    """

    def __init__(self, filename):
        """Constructor

        Loading, converting, and scaling the defender image.
        Args:
            filename (string): name (without path) of the defender bitmap
        """
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(Settings.image_path, filename))
        self.image = pygame.transform.scale(
            self.image, (30, 30)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = Settings.window_width // 2
        self.rect.bottom = Settings.window_height - Settings.window_border
        self.direction = 0
        self.speed = 3

    def update(self):
        """Implemention of the horizontal movements
        """
        newrect = self.rect.move(self.direction * self.speed, 0)
        if newrect.left <= Settings.window_border:
            self.move_stop()
        if newrect.right >= Settings.window_width - Settings.window_border:
            self.move_stop()
        self.rect.move_ip(self.direction * self.speed, 0)

    def move_left(self):
        """Sets the direction to left.
        """
        self.direction = -1

    def move_right(self):
        """Sets the direction to right.
        """
        self.direction = 1

    def move_stop(self):
        """The defender stops.
        """
        self.direction = 0


class Rocket(pygame.sprite.Sprite):
    """Rockets fired by the defender.
    """

    def __init__(self, filename, defender):
        """Constructor.

        Loading, converting, and scaling the rocket image.
        Args:
            filename (string): name (without path) of the rocket bitmap
            defender (Defender): the defender who launches the rocket
        """
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(Settings.image_path, filename))
        self.image = pygame.transform.scale(
            self.image, (10, 10)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = defender.rect.centerx
        self.rect.bottom = defender.rect.top
        self.direction = -1
        self.speed = 3
        self.is_to_remove = False

    def update(self):
        """Updates the position and the status of the rocket.
        """
        newrect = self.rect.move(0, self.direction * self.speed)
        if newrect.bottom > 0:
            self.rect = newrect
        else:
            self.is_to_remove = True


class Bomb(pygame.sprite.Sprite):
    """Bombs droped by the enemies
    """

    def __init__(self, filename, enemy):
        """Constructor.

        Loading, converting, and scaling the bomb image.
        Args:
            filename (string): name (without path) of the bomb bitmap
            enemy (Enemy): the enemy who drops the bomb
        """
        super().__init__()
        self.image = pygame.image.load(
            os.path.join(Settings.image_path, filename))
        self.image = pygame.transform.scale(
            self.image, (10, 10)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = enemy.rect.centerx
        self.rect.top = enemy.rect.bottom
        self.direction = 1
        self.speed = 3
        self.is_to_remove = False

    def update(self):
        """Updates the position and the status of the bomb.
        """
        newrect = self.rect.move(0, self.direction * self.speed)
        if newrect.top < Settings.window_height - Settings.window_border:
            self.rect = newrect
        else:
            self.is_to_remove = True


class Enemy(pygame.sprite.Sprite):
    """Enemy sprite class. 

    Direction and speed are organized as static member variables.
    """
    speed_horizontal = 2
    direction_horizontal = 1
    speed_vertical = 0
    direction_vertical = 0

    def __init__(self, filename, aliennumber, colindex, rowindex):
        """Constructor.

        Loading, converting, and scaling the enemy bitmaps.

        Args:
            filename (string): name (without path) of the enemy bitmap
            colindex (int): number of the column of the sprite
            rowindex (int): number of the row of the sprite
        """
        super().__init__()
        self.images_alive = []
        self.imageindex_alive = -1
        for i in range(1, 3):
            bitmap = pygame.image.load(os.path.join(
                Settings.image_path, filename.format(aliennumber, i)))
            bitmap = pygame.transform.scale(bitmap, (50, 45)).convert_alpha()
            self.images_alive.append(bitmap)
        self.imageindex_alive = 0

        self.images_explosion = []
        self.imageindex_explosion = -1
        for i in range(1, 5):
            bitmap = pygame.image.load(os.path.join(
                Settings.image_path, "explosion0{0}.png".format(i)))
            bitmap = pygame.transform.scale(bitmap, (50, 45)).convert_alpha()
            self.images_explosion.append(bitmap)

        self.image = self.images_alive[self.imageindex_alive]
        self.rect = self.image.get_rect()
        self.distance = 5
        self.score = Settings.score[rowindex//4]
        newx = Settings.window_border + \
            (self.rect.width + self.distance) * colindex
        newy = Settings.window_border + \
            (self.rect.height + self.distance) * rowindex
        self.rect.move_ip(newx, newy)
        Enemy.speed_vertical = self.rect.height // 4
        self.fliptime_alive = 10
        self.flipcounter = self.fliptime_alive
        self.fliptime_explosion = 3


    def update(self):
        """Implemention of the horizontal and vertical movements
        """
        if self.imageindex_explosion == -1:
            self.image = self.images_alive[self.imageindex_alive]
            if self.imageindex_alive == 1:
                if self.flipcounter <= 0:
                    self.imageindex_alive = 0
                    self.flipcounter = self.fliptime_alive
                else:
                    self.flipcounter -= 1
        else:
            self.imageindex_alive = -1
            if self.imageindex_explosion < len(self.images_explosion):
                self.image = self.images_explosion[self.imageindex_explosion]
                if self.flipcounter <= 0:
                    self.imageindex_explosion += 1
                    self.flipcounter = self.fliptime_explosion
                else:
                    self.flipcounter -= 1

        self.rect.move_ip(Enemy.direction_horizontal * Enemy.speed_horizontal,
                          Enemy.direction_vertical * Enemy.speed_vertical)

    @staticmethod
    def switch_horizontal_direction():
        """Switches the horizontal direction from left to right or from right to left. 

        It is implemented as a static method because all enemies must switch at the same time.
        """
        Enemy.direction_horizontal *= -1

    @staticmethod
    def switch_vertical_direction():
        """Switches the vertical direction from up to down or from down to up. 

        It is implemented as a static method because all enemies must switch at the same time.
        """
        if Enemy.direction_vertical == 0:
            Enemy.direction_vertical = 1
        else:
            Enemy.direction_vertical = 0

    def is_horizontal_border_reached(self):
        """Has the enemy reached left or right borders of the screen.

        Returns:
            bool: True if it has reached the border otherwise False.
        """
        newrect = self.rect.move(Enemy.direction_horizontal * Enemy.speed_horizontal,
                                 Enemy.direction_vertical * Enemy.speed_vertical)
        if newrect.left <= Settings.window_border:
            return True
        if newrect.right >= Settings.window_width - Settings.window_border:
            return True
        return False

    def is_vertical_border_reached(self):
        """Has the enemy reached upper or lower borders his area.

        Returns:
            bool: True if it has reached the border otherwise False.
        """
        newrect = self.rect.move(Enemy.direction_horizontal * Enemy.speed_horizontal,
                                 Enemy.direction_vertical * Enemy.speed_vertical)
        if newrect.bottom >= Settings.enemy_bottom_border:
            return True
        return False

    def dropped_bomb(self):
        self.imageindex_alive = 1

    def can_drop(self):
        return self.flipcounter == self.fliptime_alive

    def hit_by_rocket(self):
        self.imageindex_explosion = 0
        self.flipcounter = self.fliptime_explosion

    def is_exploded(self):
        return self.imageindex_explosion >= len(self.images_explosion)

    def is_exploding(self):
        return self.imageindex_explosion >= 0 and not self.is_exploded()


if __name__ == '__main__':
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10, 50"
    #pylint: disable=no-member
    pygame.init()
    #pylint: enable=no-member

    screen = pygame.display.set_mode(
        (Settings.window_width, Settings.window_height))
    clock = pygame.time.Clock()
    score = 0
    font = pygame.font.Font(pygame.font.get_default_font(), 24)

    # All sprites are organized in sprite groups
    all_defenders = pygame.sprite.Group()
    all_enemies_alive = pygame.sprite.Group()
    all_enemies_exploding = pygame.sprite.Group()
    all_rockets = pygame.sprite.Group()
    all_bombs = pygame.sprite.Group()

    # Creating background and defender
    background = Background("background03.png")
    defender = Defender("defender01.png")
    all_defenders.add(defender)

    # Creating and ositioning the enemies in columns and rows
    for rowindex in range(0, 8):
        for colindex in range(0, Settings.enemy_nof_cols):
            aliennumber = rowindex // 2
            enemy = Enemy("alienbig0{0}0{1}.png",
                          aliennumber, colindex, rowindex)
            all_enemies_alive.add(enemy)

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_LEFT:
                    defender.move_left()
                elif event.key == K_RIGHT:
                    defender.move_right()
                elif event.key == K_SPACE:
                    if len(all_rockets) < Settings.max_rockets:
                        rocket = Rocket("shoot.png", defender)
                        all_rockets.add(rocket)
            elif event.type == KEYUP:
                if event.key == K_LEFT or event.key == K_RIGHT:
                    defender.move_stop()

        # Update defender
        defender.update()

        # Update enemies
        has_horizontal_border_reached = False
        for enemy in all_enemies_alive:
            if enemy.is_horizontal_border_reached():
                has_horizontal_border_reached = True
                break
        has_vertical_border_reached = False
        for enemy in all_enemies_alive:
            if enemy.is_vertical_border_reached():
                has_vertical_border_reached = True
                break

        if has_horizontal_border_reached:
            Enemy.switch_horizontal_direction()
            if not has_vertical_border_reached:
                Enemy.switch_vertical_direction()

        if has_horizontal_border_reached:
            if not has_vertical_border_reached:
                Enemy.switch_vertical_direction()

        all_enemies_alive.update()
        all_enemies_exploding.update()

        # Update rockets
        all_rockets.update()
        rockets_to_remove = pygame.sprite.Group()
												 
        for rocket in all_rockets:
            tmp = pygame.sprite.spritecollide(rocket, all_enemies_alive, False)
            if len(tmp) > 0:
                rocket.is_to_remove = True
                all_enemies_alive.remove(tmp)
                all_enemies_exploding.add(tmp)
                for enemy in tmp:
                    enemy.hit_by_rocket()
                    score += enemy.score
            if rocket.is_to_remove:
                rockets_to_remove.add(rocket)
        all_rockets.remove(rockets_to_remove)

        # Update Enemies
        enemies_to_remove = pygame.sprite.Group()
        for enemy in all_enemies_exploding:
            if enemy.is_exploded():
                enemies_to_remove.add(enemy)
        all_enemies_exploding.remove(enemies_to_remove)

        # Drop bombs
        if len(all_bombs) < Settings.max_bombs and len(all_enemies_alive) > 0:
            enemy_index = randint(0, len(all_enemies_alive) - 1)
            enemy = all_enemies_alive.sprites()[enemy_index]
            if enemy.can_drop():
                bomb = Bomb("bomb.png", enemy)
                all_bombs.add(bomb)
                enemy.dropped_bomb()
            all_bombs.add(bomb)
        all_bombs.update()
        bombs_to_remove = pygame.sprite.Group()
        tmp = pygame.sprite.spritecollide(defender, all_bombs, False)
        for t in tmp:
            t.is_to_remove = True
        for bomb in all_bombs:
            if bomb.is_to_remove:
                bombs_to_remove.add(bomb)
        all_bombs.remove(bombs_to_remove)

        # Draw
        background.draw(screen)
        all_defenders.draw(screen)
        all_enemies_alive.draw(screen)
        all_enemies_exploding.draw(screen)
        all_rockets.draw(screen)
        all_bombs.draw(screen)

        text_surface_scrore = font.render(
            "Score: {0}".format(score), True, (255, 255, 255))
        screen.blit(text_surface_scrore,
                    (Settings.window_border, Settings.window_height - 50))
        pygame.display.flip()

    #pylint: disable=no-member
    pygame.quit()
    #pylint: enable=no-member

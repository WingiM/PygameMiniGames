# Суть игры заключается в том, чтобы вытеснить своего оппонента за игровое поле
# Управление - клавишы W и UP

import pygame
from load_image import load_image
from load_sound import load_sound
from constants import SUMO_WIN_SOUND, SUMO_MOVES, SUMO_FIELD_COORDS, SUMO_PLAYER_SCALE, SUMO_FIELD_IMAGE, \
    SUMO_PLAYER_IMAGE

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
FIELD_IMAGE = pygame.transform.scale(load_image(SUMO_FIELD_IMAGE), (500, 500))
SUMO_field = pygame.sprite.Sprite()
SUMO_field.image = FIELD_IMAGE
SUMO_field.rect = SUMO_field.image.get_rect()
SUMO_field.rect.x, SUMO_field.rect.y = SUMO_FIELD_COORDS


class SumoGame:
    """Класс игры в Сумо"""

    win_sound = load_sound(SUMO_WIN_SOUND)

    def __init__(self, screen, player1, player2, sprite_group):
        self.screen = screen
        self.p1, self.p2 = player1, player2
        self.sprite_group = sprite_group
        self.caption = 'Сумо'
        self.win = False

    def render(self):
        """Прорисовка поля"""
        self.screen.fill((255, 255, 102))
        self.sprite_group.draw(screen)

    def update(self, player):
        """Обновление позиций игроков, их столкновений, а также выход за пределы поля"""
        if not self.win:
            collide = pygame.sprite.collide_mask(self.p1, self.p2)  # Сталкиваются ли игроки друг с другом
            if player == 1:
                self.p1.rect = self.p1.rect.move(*SUMO_MOVES)
                if collide:
                    self.p2.rect = self.p2.rect.move(*SUMO_MOVES)
                if not pygame.sprite.collide_rect(SUMO_field, self.p2):  # Не вышел ли игрок за пределы поля
                    self.caption = f'Сумо (ПОБЕДИЛ ИГРОК 1)'
                    self.win = True
                    pygame.mixer.Sound.play(SumoGame.win_sound)
            else:
                self.p2.rect = self.p2.rect.move(*map(lambda x: -x, SUMO_MOVES))
                if collide:
                    self.p1.rect = self.p1.rect.move(*map(lambda x: -x, SUMO_MOVES))
                if not pygame.sprite.collide_rect(SUMO_field, self.p1):  # Не вышел ли игрок за пределы поля
                    self.caption = f'Сумо (ПОБЕДИЛ ИГРОК 2)'
                    self.win = True
                    pygame.mixer.Sound.play(SumoGame.win_sound)

    def restart(self):
        """Перезапуск игры"""
        self.p1.rect.x, self.p1.rect.y = self.p1.pos
        self.p2.rect.x, self.p2.rect.y = self.p2.pos
        self.win = False
        self.caption = 'Сумо'


class Player(pygame.sprite.Sprite):
    """Класс игрока в Сумо"""

    image = pygame.transform.scale(load_image(SUMO_PLAYER_IMAGE), SUMO_PLAYER_SCALE)

    def __init__(self, *group, pos, transform=None):
        super(Player, self).__init__(*group)
        if transform:
            self.image = pygame.transform.rotate(Player.image, 180)
        else:
            self.image = Player.image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

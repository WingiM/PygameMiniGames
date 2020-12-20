import pygame
from Board import Board
from load_image import load_image
from load_sound import load_sound
from constants import SUMO_WIN_SOUND, SUMO_MOVES

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
FIELD_IMAGE = pygame.transform.scale(load_image('sumo_field.png'), (500, 500))
SUMO_field = pygame.sprite.Sprite()
SUMO_field.image = FIELD_IMAGE
SUMO_field.rect = SUMO_field.image.get_rect()
SUMO_field.rect.x, SUMO_field.rect.y = 150, 150


class SumoGame(Board, pygame.sprite.Sprite):
    win_sound = load_sound(SUMO_WIN_SOUND)

    def __init__(self, screen, player1, player2, sprite_group):
        super().__init__(10, 10, screen)
        self.screen = screen
        self.p1, self.p2 = player1, player2
        self.sprite_group = sprite_group
        self.caption = 'Сумо'
        self.win = False

    def render(self):
        self.screen.fill((255, 255, 102))
        self.sprite_group.draw(screen)

    def update(self, player):
        if not self.win:
            collide = pygame.sprite.collide_mask(self.p1, self.p2)
            if player == 1:
                self.p1.rect = self.p1.rect.move(*SUMO_MOVES)
                if collide:
                    self.p2.rect = self.p2.rect.move(*SUMO_MOVES)
                if not pygame.sprite.collide_rect(SUMO_field, self.p2):
                    pygame.display.set_caption(f'Сумо (ПОБЕДИЛ ВЕРХНИЙ)')
                    self.win = True
                    pygame.mixer.Sound.play(SumoGame.win_sound)
            else:
                self.p2.rect = self.p2.rect.move(*map(lambda x: -x, SUMO_MOVES))
                if collide:
                    self.p1.rect = self.p1.rect.move(*map(lambda x: -x, SUMO_MOVES))
                if not pygame.sprite.collide_rect(SUMO_field, self.p1):
                    pygame.display.set_caption(f'Сумо (ПОБЕДИЛ НИЖНИЙ)')
                    self.win = True
                    pygame.mixer.Sound.play(SumoGame.win_sound)

    def restart(self):
        self.p1.rect.x, self.p1.rect.y = self.p1.pos
        self.p2.rect.x, self.p2.rect.y = self.p2.pos
        self.win = False
        pygame.display.set_caption('Сумо')


class Player(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('sumo.png'), (200, 200))

    def __init__(self, *group, pos, transform=None):
        super(Player, self).__init__(*group)
        if not transform:
            self.image = Player.image
        else:
            self.image = pygame.transform.rotate(Player.image, 90)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

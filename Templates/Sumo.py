import pygame
from Templates.Board import Board
from Templates.load_image import load_image

FPS = 60
clock = pygame.time.Clock()
pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
FIELD_IMAGE = pygame.transform.scale(load_image('sumo_field.png'), (500, 500))
SUMO_field = pygame.sprite.Sprite()
SUMO_field.image = FIELD_IMAGE
SUMO_field.rect = SUMO_field.image.get_rect()
SUMO_field.rect.x, SUMO_field.rect.y = 150, 150


class SumoGame(Board, pygame.sprite.Sprite):
    def __init__(self, screen, player1, player2, sprite_group):
        super().__init__(10, 10, screen)
        self.screen = screen
        self.p1, self.p2 = player1, player2
        self.sprite_group = sprite_group
        self.caption = 'Сумо'
        self.win = False

    def render(self):
        self.sprite_group.draw(screen)

    def update(self, player):
        if not self.win:
            collide = pygame.sprite.collide_mask(self.p1, self.p2)
            if player == 1:
                self.p1.rect = self.p1.rect.move(0, 30)
                if collide:
                    self.p2.rect = self.p2.rect.move(0, 30)
                if not pygame.sprite.collide_rect(SUMO_field, self.p2):
                    pygame.display.set_caption(f'Сумо (ПОБЕДИЛ ВЕРХНИЙ)')
                    self.win = True
            else:
                self.p2.rect = self.p2.rect.move(0, -30)
                if collide:
                    self.p1.rect = self.p1.rect.move(0, -30)
                if not pygame.sprite.collide_rect(SUMO_field, self.p1):
                    pygame.display.set_caption(f'Сумо (ПОБЕДИЛ НИЖНИЙ)')
                    self.win = True

    def restart(self):
        self.p1.rect.y = 150
        self.p2.rect.y = 450
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
        self.rect.x = pos[0]
        self.rect.y = pos[1]


# pygame.display.set_caption('Сумо')
# running = True
# all_sprites = pygame.sprite.Group()
# player1 = Player(all_sprites, pos=(300, 150))
# player2 = Player(all_sprites, pos=(300, 450), transform=90)
# game = SumoGame(screen, player1, player2, all_sprites)
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
#             game.restart()
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_w:
#                 game.update(1)
#             elif event.key == pygame.K_UP:
#                 game.update(2)
#     game.render()
#     clock.tick(60)
#     pygame.display.flip()

import os
import sys
import pygame

FPS = 60
clock = pygame.time.Clock()
pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class SumoGame:
    def __init__(self, screen, player1, player2, sprite_group):
        self.screen = screen
        self.p1, self.p2 = player1, player2
        self.sprite_group = sprite_group

    def render(self):
        pygame.draw.circle(self.screen, 'yellow', (400, 400), 300)
        all_sprites.draw(screen)

    def update(self, player):
        if player == 1:
            self.p1.rect.y += 10
            self.p2.rect.y += 10
        else:
            self.p2.rect.y -= 10
            self.p1.rect.y -= 10


class Player(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('sumo.png'), (200, 200))

    def __init__(self, *group, pos, transform=None):
        super(Player, self).__init__(*group)
        if not transform:
            self.image = Player.image
        else:
            self.image = pygame.transform.rotate(Player.image, 90)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def move(self, val):
        delta = 0
        while delta != val:
            self.rect.y += 1


if __name__ == '__main__':
    pygame.display.set_caption('Сумо')
    running = True
    all_sprites = pygame.sprite.Group()
    player1 = Player(all_sprites, pos=(300, 150))
    player2 = Player(all_sprites, pos=(300, 450), transform=90)
    game = SumoGame(screen, player1, player2, all_sprites)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pass  # TODO: restart
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    game.update(1)
                elif event.key == pygame.K_UP:
                    game.update(2)
        game.render()
        clock.tick(60)
        pygame.display.flip()

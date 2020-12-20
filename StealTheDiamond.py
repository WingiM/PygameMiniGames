import pygame
import random
from Board import Board
from load_image import load_image
from load_sound import load_sound
from constants import STD_TIME_RANGE, STD_DELAY, STD_EVENT_TYPE, \
    STD_HAND1_EVENT, STD_HAND2_EVENT, STD_HAND_SPEED, WIDTH, HEIGHT

FPS = 60
pygame.init()
size = width, height = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)


class StealTheDiamond(Board):
    bell = load_sound('bell.mp3')
    rewind = load_sound('restart.mp3')

    def __init__(self, screen, sprites):
        super().__init__(10, 10, screen)
        self.screen = screen
        self.time_range = STD_TIME_RANGE
        self.caption = 'Украсть бриллиант'
        self.sprites = sprites
        self.active = False
        self.time = random.randint(*self.time_range)
        self.delay = STD_DELAY
        pygame.time.set_timer(STD_EVENT_TYPE, self.delay)

    def render(self):
        if self.active:
            self.screen.fill((0, 4, 71))
        else:
            self.screen.fill((153, 102, 51))
        self.sprites.draw(self.screen)

    def update(self):
        if self.time > 0:
            self.time -= self.delay
        else:
            pygame.mixer.Sound.play(StealTheDiamond.bell)
            self.active = True
            pygame.time.set_timer(STD_EVENT_TYPE, 0)

    def restart(self):
        pygame.mixer.Sound.play(StealTheDiamond.rewind)
        self.active = False
        self.time = random.randint(*self.time_range)
        pygame.time.set_timer(STD_EVENT_TYPE, self.delay)


class Diamond(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('diamond.png'), (200, 200))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Diamond.image
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - self.image.get_width() // 2
        self.rect.y = HEIGHT // 2 - self.image.get_width() // 2
        self.mask = pygame.mask.from_surface(self.image)
        self.grabbed = False

    def move(self, speed):
        self.rect = self.rect.move(speed, 0)
        self.grabbed = True

    def set_start_pos(self):
        self.rect.x = WIDTH // 2 - self.image.get_width() // 2
        self.rect.y = HEIGHT // 2 - self.image.get_width() // 2


class Hand(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('hand.png'), (200, 150))
    snatch = load_sound('snatch.mp3')

    def __init__(self, *group, number=0, diamond=None):
        super().__init__(*group)
        self.number = number
        self.diamond = diamond
        self.event = STD_HAND1_EVENT if self.number == 1 else STD_HAND2_EVENT
        self.delay = STD_DELAY
        self.image = Hand.image if self.number == 1 else pygame.transform.flip(Hand.image, True, False)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = -50 if self.number == 1 else WIDTH - 150
        self.rect.y = HEIGHT // 2 - self.image.get_height() // 2
        self.speed = 0
        self.can_move = False

    def pressed(self):
        if not self.speed:
            self.speed = STD_HAND_SPEED if self.number == 1 else -STD_HAND_SPEED
            pygame.time.set_timer(self.event, self.delay)

    def check_collision(self):
        if pygame.sprite.collide_mask(self, self.diamond) and not self.diamond.grabbed and self.can_move:
            pygame.mixer.Sound.play(Hand.snatch)
            self.speed = -STD_HAND_SPEED
            self.diamond.move(self.speed * 2)
        if self.number == 1:
            if self.rect.x >= 200:
                self.speed = -STD_HAND_SPEED
            if self.rect.x < -50:
                self.speed = 0
                self.rect.x = -50
                pygame.time.set_timer(self.event, 0)
        else:
            if self.rect.x <= 400:
                self.speed = -STD_HAND_SPEED
            if self.rect.x > 650:
                self.speed = 0
                self.rect.x = 650
                pygame.time.set_timer(self.event, 0)

    def move(self):
        self.rect = self.rect.move(self.speed, 0)
        self.check_collision()
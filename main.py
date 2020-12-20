import pygame
from itertools import cycle
from constants import *  # Переносит все константы, использующиеся в проекте
from TicTacToe import TicTacToeBoard   # Поле для игры в крестики-нолики
from Sumo import SumoGame, Player, SUMO_field  # Поле для игры в сумо, а также класс игрока
from StealTheDiamond import StealTheDiamond, Hand, Diamond

# Начало работы с pygame
pygame.init()
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

# Настройка игры в крестики нолики
TicTacToe = TicTacToeBoard(screen)
TicTacToe.set_view((WIDTH - TicTacToe.width * CELL_SIZE) // 2, (HEIGHT - TicTacToe.height * CELL_SIZE) // 2, CELL_SIZE)

# Настройка игры в сумо
SUMO_all_sprites = pygame.sprite.Group()
SUMO_all_sprites.add(SUMO_field)
SUMO_player1 = Player(SUMO_all_sprites, pos=SUMO_PLAYER1)
SUMO_player2 = Player(SUMO_all_sprites, pos=SUMO_PLAYER2, transform=90)
Sumo = SumoGame(screen, SUMO_player1, SUMO_player2, SUMO_all_sprites)

# Настройка игры в "Украсть бриллиант"
STD_all_sprites = pygame.sprite.Group()
diamond = Diamond(STD_all_sprites)
hand1 = Hand(STD_all_sprites, number=1, diamond=diamond)
hand2 = Hand(STD_all_sprites, number=2, diamond=diamond)
STD = StealTheDiamond(screen, STD_all_sprites)

# Цикл со всеми играми (временный)
GAMES = cycle([STD, TicTacToe, Sumo])


def play_game(game, event):
    if game == STD:
        if event.type == STD_EVENT_TYPE:
            game.update()
        if event.type == STD_HAND1_EVENT:
            hand1.move()
        if event.type == STD_HAND2_EVENT:
            hand2.move()
    if event.type == pygame.KEYDOWN:
        if game == Sumo:
            if event.key == pygame.K_w:
                game.update(1)
            if event.key == pygame.K_UP:
                game.update(2)
        if game == STD:
            if event.key == pygame.K_w:
                hand1.pressed()
            if event.key == pygame.K_UP:
                hand2.pressed()


def start_game():
    game = next(GAMES)
    pygame.display.set_caption(game.caption)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.get_click(event.pos)
            play_game(game, event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.restart()
                elif event.key == pygame.K_RALT:
                    game.restart()
                    game = next(GAMES)
                    pygame.display.set_caption(game.caption)
        screen.fill((0, 0, 0))
        game.render()
        clock.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    start_game()

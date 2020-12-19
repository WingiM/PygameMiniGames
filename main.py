import pygame
from itertools import cycle
from constants import *  # Переносит все константы, использующиеся в проекте
from TicTacToe import TicTacToeBoard
from Sumo import SumoGame, Player, SUMO_field

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
SUMO_PLAYER_X, SUMO_PLAYER1_Y, SUMO_PLAYER2_Y = 300, 190, 410
SUMO_player1 = Player(SUMO_all_sprites, pos=(SUMO_PLAYER_X, SUMO_PLAYER1_Y))
SUMO_player2 = Player(SUMO_all_sprites, pos=(SUMO_PLAYER_X, SUMO_PLAYER2_Y), transform=90)
Sumo = SumoGame(screen, SUMO_player1, SUMO_player2, SUMO_all_sprites)

# Цикл со всеми играми (временный)
GAMES = cycle([TicTacToe, Sumo])


def play_game(game, event):
    if game == Sumo:
        if event.key == pygame.K_w:
            game.update(1)
        elif event.key == pygame.K_UP:
            game.update(2)


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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.restart()
                elif event.key == pygame.K_RALT:
                    game.restart()
                    game = next(GAMES)
                    pygame.display.set_caption(game.caption)
                play_game(game, event)
        screen.fill((255, 255, 102))
        game.render()
        clock.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    start_game()

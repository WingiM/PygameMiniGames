import pygame
from itertools import cycle
from Templates.TicTacToe import TicTacToeBoard
from Templates.Sumo import SumoGame, Player


def play_game(game, event):
    if game == Sumo:
        if event.key == pygame.K_w:
            game.update(1)
        elif event.key == pygame.K_UP:
            game.update(2)

# Объявление констант, определяющих работу игр
FPS = 60
CELL_SIZE = 100  # Для игр с клетчатым полем (17.12.2020 - TicTacToe)

# Начало работы с pygame
pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# Настройка игры в крестики нолики
TicTacToe = TicTacToeBoard(screen)
TicTacToe.set_view((width - TicTacToe.width * CELL_SIZE) // 2, (height - TicTacToe.height * CELL_SIZE) // 2, CELL_SIZE)

# Настройка игры в сумо
SUMO_all_sprites = pygame.sprite.Group()
SUMO_player1 = Player(SUMO_all_sprites, pos=(300, 150))
SUMO_player2 = Player(SUMO_all_sprites, pos=(300, 450), transform=90)
Sumo = SumoGame(screen, SUMO_player1, SUMO_player2, SUMO_all_sprites)

# Цикл со всеми играми (временный)
GAMES = cycle([TicTacToe, Sumo])

if __name__ == '__main__':
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
                    screen.fill((0, 0, 0))
                    game.restart()
                    game = next(GAMES)
                    pygame.display.set_caption(game.caption)
                play_game(game, event)
        game.render()
        clock.tick(FPS)
        pygame.display.flip()

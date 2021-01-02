import pygame
from itertools import product
from Board import Board

# from load_image import load_image
# from load_sound import load_sound
# from constants import WIDTH, HEIGHT

pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)


def check_equal_coordinates(arr) -> bool:  # Проверяет, нет ли "косых" кораблей
    a, all_x = list(map(lambda w: w[0], arr)), True
    b, all_y = list(map(lambda w: w[1], arr)), True
    for i in a:
        if a[0] != i:
            all_x = False
    for i in b:
        if b[0] != i:
            all_y = False
    return any([all_x, all_y])


def correct(x, y):  # Проверяет корректность введеных координат (существует ли такая клетка)
    return True if 0 <= x <= 7 and 0 <= y <= 7 else False


def get_round_ships(arrange, x, y) -> int:  # Возвращает количество клеток с кораблями вокруг данной
    boards = [(x, y)]
    rounds = list(
        filter(lambda w: correct(*w) and not (w[0] == x and w[1] == y), product([x, x + 1, x - 1], [y, y + 1, y - 1])))
    for x, y in rounds:
        if arrange[y][x] == '#':
            boards.append((x, y))
    if c := len(boards) == 1 or check_equal_coordinates(boards):
        return c
    else:
        return 3


def check_arrangement(arrangement) -> bool:  # Проверяет правильность расстановки
    print(len(arrangement))
    if max(map(len, arrangement)) > 8 or len(arrangement) != 8:
        return False

    for i in range(len(arrangement)):
        for j in range(len(arrangement[i])):
            if arrangement[i][j] == '#' and get_round_ships(arrangement, j, i) > 2:
                return False

    return True


def load_arrangement(filename) -> list:  # Загружает расстановку
    with open(filename, 'r') as arrange:
        arrange = [list(line.strip().ljust(8, '.')) for line in arrange if line.strip()]
        if not arrange:
            arrange = [list('.' * 8) for _ in range(8)]

    if not check_arrangement(arrange):
        print(f'Ошибка в расстановке {filename}')

    return arrange


class SeaBattleBoard(Board):
    def __init__(self):
        super().__init__(8, 8, screen)
        self.turn = 'red'
        self.p1 = load_arrangement('SB_player1.txt')
        self.p2 = load_arrangement('SB_player2.txt')


game = SeaBattleBoard()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    pygame.display.flip()

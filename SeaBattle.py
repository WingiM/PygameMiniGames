import pygame
from itertools import product
from Board import Board
# from load_image import load_image
# from load_sound import load_sound
from constants import WIDTH, HEIGHT, COLORS, SB_CELL_SIZE, SB_CD_LEN
from load_image import load_image
from load_sound import load_sound

pygame.init()
size = width, height = WIDTH, HEIGHT
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


def get_round_ships_count(arrange, x, y) -> int:  # Возвращает количество клеток с кораблями вокруг данной
    boards = [(x, y)]
    rounds = list(
        filter(lambda w: correct(*w) and not (w[0] == x and w[1] == y), product([x, x + 1, x - 1], [y, y + 1, y - 1])))
    for x, y in rounds:
        if arrange[y][x] == '#':
            boards.append((x, y))
    if (c := len(boards)) == 1 or check_equal_coordinates(boards):
        return c
    else:
        return 4


def check_arrangement(arrangement) -> bool:  # Проверяет правильность расстановки
    if max(map(len, arrangement)) > 8 or len(arrangement) != 8:
        return False

    for i in range(len(arrangement)):
        for j in range(len(arrangement[i])):
            if arrangement[i][j] == '#' and get_round_ships_count(arrangement, j, i) > 3:
                return False

    return True


def load_arrangement(filename) -> tuple:  # Загружает расстановку
    empty = False
    with open(filename, 'r') as arrangement:
        arrangement = [list(line.strip().ljust(8, '.')) for line in arrangement if line.strip()]
        if not arrangement:
            empty = True
            arrangement = [list('.' * 8) for _ in range(8)]

    if not check_arrangement(arrangement):
        print(f'Ошибка в расстановке {filename}')

    return arrangement, empty


class SeaBattleBoard(Board):
    explosion_sound = load_sound('SB_explosion.mp3')
    miss_sound = load_sound('SB_miss.mp3')
    background = pygame.transform.scale(load_image('SB_back.jpg'), (WIDTH, HEIGHT))

    def __init__(self, screen):
        super().__init__(8, 8, screen)
        self.caption = 'Морской Бой'
        self.turn = 'red'
        self.screen = screen
        self.cooldown = 0
        self.p1, self.p1_is_empty = load_arrangement('SB_player1.txt')
        self.p2, self.p2_is_empty = load_arrangement('SB_player2.txt')
        self.board = self.p1
        if any([self.p1_is_empty, self.p2_is_empty]):
            self.caption = 'Морской Бой (у одного из игроков пустое поле)'

    def render(self):
        if self.cooldown:
            self.cooldown -= 1
            if not self.cooldown:
                self.turn = 'blue' if self.turn == 'red' else 'red'
                self.board = self.p1 if self.board == self.p2 else self.p2
        self.screen.blit(SeaBattleBoard.background, (0, 0))
        y = self.top
        for i in range(self.height):
            x = self.left
            for j in range(self.width):
                pygame.draw.rect(self.screen, (0, 102, 204), (x, y, self.cell_size, self.cell_size), 1)
                pygame.draw.rect(self.screen, 'white', (x + 1, y + 1, self.cell_size - 2, self.cell_size - 2))
                if self.board[i][j] == '+':
                    pygame.draw.rect(self.screen, 'red', (x + 1, y + 1, self.cell_size - 2, self.cell_size - 2))
                elif self.board[i][j] == '@':
                    another_y = y + 1 + self.cell_size // 5
                    for _ in range(4):
                        pygame.draw.line(self.screen, (0, 102, 204), (x + 1, another_y - 5),
                                         (x + self.cell_size - 2, another_y + 5), 5)
                        another_y += self.cell_size // 5
                x += self.cell_size
            y += self.cell_size

    def on_click(self, cell):
        if cell and not self.cooldown:
            x, y = cell
            if self.board[y][x] == '.':
                pygame.mixer.Sound.play(SeaBattleBoard.miss_sound)
                self.board[y][x] = '@'
                self.cooldown = SB_CD_LEN
            elif self.board[y][x] == '#':
                pygame.mixer.Sound.play(SeaBattleBoard.explosion_sound)
                self.board[y][x] = '+'

    def restart(self):
        pass


if __name__ == '__main__':
    game = SeaBattleBoard(screen)
    game.set_view((WIDTH - game.width * SB_CELL_SIZE) // 2,
                  (HEIGHT - game.height * SB_CELL_SIZE) // 2, SB_CELL_SIZE)
    running = True
    while running:
        pygame.display.set_caption(game.caption)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.get_click(event.pos)

        screen.fill((0, 0, 0))
        game.render()

        pygame.display.flip()

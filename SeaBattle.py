import pygame
from itertools import product
from Board import Board
from constants import WIDTH, HEIGHT, SB_CELL_SIZE, SB_CD_LENGTH, SB_FONT_COLOR, SB_PLAYER1_FILENAME, \
    SB_PLAYER2_FILENAME, SB_EXPLOSION_SOUND, SB_MISS_SOUND, WIN_SOUND, COLORS
from load_image import load_image
from load_sound import load_sound

pygame.init()
size = width, height = WIDTH, HEIGHT
screen = pygame.display.set_mode(size)


def create_ship_map(arrangement, filename) -> dict:  # Создает "карту" расстановки кораблей
    ships = {1: [], 2: [], 3: [], 4: []}

    # Для каждого значения координат X и Y создается массив координат, где расположены корабли
    xs = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
    ys = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}

    for i in range(len(arrangement)):
        for j in range(len(arrangement[i])):
            if arrangement[i][j] == '#':
                # Одиночные корабли можно сразу исключить
                if get_round_ships_count(arrangement, j, i) == 1:
                    ships[1].append([(j, i)])
                    continue
                xs[j].append((j, i))
                ys[i].append((j, i))

    # Происходит поиск кораблей по оси X
    for n in xs:
        coords = []
        for i in xs[n]:
            x, y = i
            if (x, y + 1) in xs[n]:
                coords.append((x, y))
            elif len(coords) > 0:
                coords.append((x, y))
                break
        try:
            if 1 < len(coords):
                ships[len(coords)].append(coords)
        except KeyError:
            print(f'Длина одного или нескольких кораблей превышает 4 клетки в расстановке {filename}')
            exit(0)

    # Происходит поиск кораблей по оси Y
    for n in ys:
        coords = []
        for i in ys[n]:
            x, y = i
            if (x + 1, y) in ys[n]:
                coords.append((x, y))
            elif len(coords) > 0:
                coords.append((x, y))
                break
        try:
            if 1 < len(coords):
                ships[len(coords)].append(coords)
        except KeyError:
            print(f'Длина одного или нескольких кораблей превышает 4 клетки в расстановке {filename}')
            exit(0)

    return ships


def check_equal_coordinates(arrangement) -> bool:  # Проверяет, нет ли "косых" кораблей
    a, all_x = list(map(lambda w: w[0], arrangement)), True
    b, all_y = list(map(lambda w: w[1], arrangement)), True
    for i in a:
        if a[0] != i:
            all_x = False
    for i in b:
        if b[0] != i:
            all_y = False
    return any([all_x, all_y])


def correct(x, y):  # Проверяет корректность введеных координат (существует ли такая клетка)
    return True if 0 <= x <= 9 and 0 <= y <= 9 else False


def get_round_ships_count(arrangement, x, y) -> int:  # Возвращает количество клеток с кораблями вокруг данной
    boards = [(x, y)]
    rounds = list(
        filter(lambda w: correct(*w) and not (w[0] == x and w[1] == y), product([x, x + 1, x - 1], [y, y + 1, y - 1])))
    for x, y in rounds:
        if arrangement[y][x] == '#':
            boards.append((x, y))
    if (c := len(boards)) == 1 or check_equal_coordinates(boards):
        return c
    else:
        return 4


def check_arrangement(arrangement, ship_map) -> bool:  # Проверяет правильность расстановки
    if max(map(len, arrangement)) > 10 or len(arrangement) != 10:  # Не превышает ли поле установленные размеры
        return False

    for i in range(len(arrangement)):  # Нет ли неправильных кораблей (косых или образующих угол)
        for j in range(len(arrangement[i])):
            if arrangement[i][j] == '#' and get_round_ships_count(arrangement, j, i) > 3:
                return False

    # Правильно ли задано количество кораблей (4 одиночных, 3 двойных и т.д.)
    if list(map(len, ship_map.values())) != [4, 3, 2, 1]:
        return False

    return True


def load_arrangement(filename) -> tuple:  # Загружает расстановку
    is_empty = False
    try:
        with open(filename, 'r') as arrangement:
            # Если длины одной из строк не хватает, то добавляются точки
            arrangement = [list(line.strip().ljust(10, '.')) for line in arrangement if line.strip()]
            if not arrangement:
                is_empty = True
                arrangement = [list('.' * 10) for _ in range(10)]
    except FileNotFoundError:
        print(f'Файл {filename} не найден')
        exit(0)

    ship_map = create_ship_map(arrangement, filename)

    if not check_arrangement(arrangement, ship_map):
        print(f'Ошибка в расстановке {filename}')
        exit(0)

    return arrangement, ship_map, is_empty


class SeaBattleBoard(Board):
    explosion_sound = load_sound(SB_EXPLOSION_SOUND)
    miss_sound = load_sound(SB_MISS_SOUND)
    background = pygame.transform.scale(load_image('SB_back.png'), (WIDTH, HEIGHT))

    def __init__(self, screen):
        super().__init__(10, 10, screen)
        self.caption = 'Морской Бой'
        self.won = False
        self.screen = screen
        self.cooldown = 0
        self.p1, self.p1_ship_map, self.p1_is_empty = load_arrangement(SB_PLAYER1_FILENAME)
        self.p2, self.p2_ship_map, self.p2_is_empty = load_arrangement(SB_PLAYER2_FILENAME)
        self.board = self.p2
        self.map = self.p2_ship_map
        self.font = pygame.font.Font(None, SB_CELL_SIZE)
        if any([self.p1_is_empty, self.p2_is_empty]):
            self.caption = 'Морской Бой (у одного из игроков пустое поле)'

    def render(self):
        if self.cooldown:
            self.cooldown -= 1
            if not self.cooldown:
                self.board = self.p1 if self.board == self.p2 else self.p2
                self.map = self.p1_ship_map if self.map == self.p2_ship_map else self.p2_ship_map
        self.screen.fill((255, 255, 255))
        self.screen.blit(SeaBattleBoard.background, (0, 0))
        y = self.top
        c = 1
        for i in range(self.height):
            x = self.left
            num = self.font.render(f'{c}', True, SB_FONT_COLOR)
            if c == 10:
                self.screen.blit(num, (x - self.cell_size // 1.2, y + self.cell_size // 10))
            else:
                self.screen.blit(num, (x - self.cell_size // 2, y + 5))
            let = ord('A')
            for j in range(self.width):
                if i == 0:
                    letter = self.font.render(f'{chr(let)}', True, SB_FONT_COLOR)
                    self.screen.blit(letter, (x + self.cell_size // 4, y - self.cell_size // 1.5))
                    let += 1
                pygame.draw.rect(self.screen, (0, 102, 204), (x, y, self.cell_size, self.cell_size), 1)
                pygame.draw.rect(self.screen, 'white', (x + 1, y + 1, self.cell_size - 2, self.cell_size - 2))
                if self.board[i][j] == '+':
                    pygame.draw.rect(self.screen, COLORS['red'], (x + 1, y + 1, self.cell_size - 2, self.cell_size - 2))
                elif self.board[i][j] == '@':
                    another_y = y + 1 + self.cell_size // 5
                    for _ in range(4):
                        pygame.draw.line(self.screen, COLORS['dark-blue'], (x + 1, another_y - 5),
                                         (x + self.cell_size - 2, another_y + 5), 5)
                        another_y += self.cell_size // 5
                x += self.cell_size
            c += 1
            y += self.cell_size

    def on_click(self, cell):
        if cell and not self.cooldown and not self.won:
            x, y = cell
            # Если игрок промахивается, то ход передается следующему после "перезарядки"
            if self.board[y][x] == '.':
                pygame.mixer.Sound.play(SeaBattleBoard.miss_sound)
                self.board[y][x] = '@'
                self.cooldown = SB_CD_LENGTH
            elif self.board[y][x] == '#':
                pygame.mixer.Sound.play(SeaBattleBoard.explosion_sound)
                self.board[y][x] = '+'
                self.check_kills()

    def check_kills(self):  # Проверяет, нет ли уничтоженных кораблей
        for ship_size in self.map:
            for ship in self.map[ship_size]:
                if all(self.cell_is_destroyed(x, y) for x, y in ship):
                    self.map[ship_size].remove(ship)
                    self.shoot_rounds(ship)
        self.check_win()

    def check_win(self):
        if not any(self.map[ship_size] for ship_size in self.map):
            self.won = True
            pygame.mixer.Sound.play(load_sound(WIN_SOUND))
            if self.map == self.p1_ship_map:
                self.caption = 'Морской бой (ПОБЕДИЛ ИГРОК 2)'
            else:
                self.caption = 'Морской бой (ПОБЕДИЛ ИГРОК 1)'

    def shoot_rounds(self, ship):  # Закрашивает клетки возле уничтоженного корабля (вызывается из check_kills())
        for i in ship:
            x, y = i
            rounds = list(
                filter(lambda w: correct(*w) and not (w[0] == x and w[1] == y),
                       product([x, x + 1, x - 1], [y, y + 1, y - 1])))
            for j in rounds:
                x1, y1 = j
                if self.board[y1][x1] == '.':
                    self.board[y1][x1] = '@'

    def cell_is_destroyed(self, x, y):  # Есть ли в этой клетке поврежденная часть корабля
        return self.board[y][x] == '+'

    def restart(self):
        self.caption = 'Морской бой'
        self.p1, self.p1_ship_map, self.p1_is_empty = load_arrangement(SB_PLAYER1_FILENAME)
        self.p2, self.p2_ship_map, self.p2_is_empty = load_arrangement(SB_PLAYER2_FILENAME)
        self.won = False
        self.board = self.p2
        self.map = self.p2_ship_map


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
import os
import sys
import pygame
from Templates.Board import Board

CELL_SIZE = 100
COLORS = {'red': (255, 102, 102),
          'blue': (0, 153, 255)}

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


class TicTacToeBoard(Board):
    cross = load_image('cross.png')
    nought = load_image('nought.png')

    def __init__(self, screen):
        super().__init__(3, 3, screen)
        self.turn = 'red'
        self.outline = self.cell_size // 10
        self.cross = pygame.transform.scale(TicTacToeBoard.cross,
                                            (self.cell_size - self.outline, self.cell_size - self.outline))
        self.nought = pygame.transform.scale(TicTacToeBoard.nought,
                                             (self.cell_size - self.outline, self.cell_size - self.outline))
        self.working = True
        self.won = None

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.outline = self.cell_size // 10
        self.cross = pygame.transform.scale(TicTacToeBoard.cross,
                                            (self.cell_size - self.outline, self.cell_size - self.outline))
        self.nought = pygame.transform.scale(TicTacToeBoard.nought,
                                             (self.cell_size - self.outline, self.cell_size - self.outline))

    def render(self):
        y = self.top
        for i in range(self.height):
            x = self.left
            for j in range(self.width):
                pygame.draw.rect(self.screen, COLORS[self.turn], (x, y, self.cell_size, self.cell_size), self.outline)
                if x != self.left:
                    pygame.draw.line(self.screen, (0, 0, 0), (x, y), (x, y + self.cell_size), self.outline)
                if self.board[i][j] == 1:
                    self.screen.blit(self.cross, (x + self.outline // 2, y + self.outline // 2))
                if self.board[i][j] == 2:
                    self.screen.blit(self.nought, (x + self.outline // 2, y + self.outline // 2))
                x += self.cell_size
            if y != self.top:
                pygame.draw.line(self.screen, (0, 0, 0), (self.left, y), (self.left + self.cell_size * self.width, y),
                                 self.outline)
            y += self.cell_size

    def check_three(self, p1, p2, p3):
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        if self.board[y1][x1] == self.board[y2][x2] == self.board[y3][x3] != 0:
            self.working = False
            self.won = 'red' if self.board[y1][x1] == 1 else 'blue'

    def check_win(self):
        for i in range(3):
            self.check_three((i, 0), (i, 1), (i, 2))
            self.check_three((0, i), (1, i), (2, i))
        self.check_three((0, 0), (1, 1), (2, 2))
        self.check_three((2, 0), (1, 1), (0, 2))

    def on_click(self, cell):
        if cell:
            x, y = cell
            if not self.board[y][x]:
                if self.working:
                    self.board[y][x] = 1 if self.turn == 'red' else 2
                self.check_win()
                if self.working:
                    self.turn = 'blue' if self.turn == 'red' else 'red'

    def set_win(self):
        if self.won:
            pygame.display.set_caption(f'Крестики нолики ({self.won.upper()} ПОБЕДИЛ!)')

    def restart(self):
        self.won = None
        self.working = True
        self.board = [[0] * self.width for _ in range(self.height)]
        self.turn = 'red'
        pygame.display.set_caption('Крестики-нолики')


if __name__ == '__main__':
    pygame.display.set_caption('Крестики-нолики')
    board = TicTacToeBoard(screen)
    board.set_view((width - board.width * CELL_SIZE) // 2, (height - board.height * CELL_SIZE) // 2, CELL_SIZE)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
            if event.type == pygame.KEYDOWN:
                board.restart()
        screen.fill(COLORS[board.turn])
        board.render()
        board.set_win()
        pygame.display.flip()

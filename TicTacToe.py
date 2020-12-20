import pygame
from Board import Board
from load_image import load_image
from load_sound import load_sound
from constants import TTT_WIN_SOUND, TTT_CLICK_SOUND, COLORS, WIDTH, HEIGHT

size = width, height = 800, 800
screen = pygame.display.set_mode(size)


class TicTacToeBoard(Board):
    cross = load_image('cross.png')
    nought = load_image('nought.png')
    press_sound = load_sound(TTT_CLICK_SOUND)
    win_sound = load_sound(TTT_WIN_SOUND)

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
        self.caption = 'Крестики-нолики'
        self.won_cells = ()

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
        self.screen.fill(COLORS[self.turn])
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
        self.set_win()

    def check_three(self, p1, p2, p3):
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        if self.board[y1][x1] == self.board[y2][x2] == self.board[y3][x3] != 0:
            self.working = False
            self.won = 'red' if self.board[y1][x1] == 1 else 'blue'
            pygame.mixer.Sound.play(TicTacToeBoard.win_sound)
            self.won_cells = (p1, p3)

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
                    pygame.mixer.Sound.play(TicTacToeBoard.press_sound)
                    self.board[y][x] = 1 if self.turn == 'red' else 2
                self.check_win()
                if self.working:
                    self.turn = 'blue' if self.turn == 'red' else 'red'

    def set_win(self):
        if self.won:
            x1, y1 = self.won_cells[0]
            x2, y2 = self.won_cells[1]
            if x1 == x2 and y1 != y2:
                x1 = (WIDTH - self.width * self.cell_size) // 2 + x1 * self.cell_size + self.cell_size // 2
                x2 = (WIDTH - self.width * self.cell_size) // 2 + x2 * self.cell_size + self.cell_size // 2
                y1 = (HEIGHT - self.height * self.cell_size) // 2 + y1 * self.cell_size
                y2 = (HEIGHT - self.height * self.cell_size) // 2 + y2 * self.cell_size + self.cell_size
            elif x1 != x2 and y1 == y2:
                x1 = (WIDTH - self.width * self.cell_size) // 2 + x1 * self.cell_size
                x2 = (WIDTH - self.width * self.cell_size) // 2 + x2 * self.cell_size + self.cell_size
                y1 = (HEIGHT - self.height * self.cell_size) // 2 + y1 * self.cell_size + self.cell_size // 2
                y2 = (HEIGHT - self.height * self.cell_size) // 2 + y2 * self.cell_size + self.cell_size // 2
            elif x1 != x2 and y1 != y2 and x2 > x1:
                x1 = (WIDTH - self.width * self.cell_size) // 2 + x1 * self.cell_size
                x2 = (WIDTH - self.width * self.cell_size) // 2 + x2 * self.cell_size + self.cell_size
                y1 = (HEIGHT - self.height * self.cell_size) // 2 + y1 * self.cell_size
                y2 = (HEIGHT - self.height * self.cell_size) // 2 + y2 * self.cell_size + self.cell_size
            else:
                x1 = (WIDTH - self.width * self.cell_size) // 2 + x1 * self.cell_size + self.cell_size
                x2 = (WIDTH - self.width * self.cell_size) // 2 + x2 * self.cell_size
                y1 = (HEIGHT - self.height * self.cell_size) // 2 + y1 * self.cell_size
                y2 = (HEIGHT - self.height * self.cell_size) // 2 + y2 * self.cell_size + self.cell_size
            pygame.draw.line(self.screen, (255, 255, 255), (x1, y1), (x2, y2), 6)
            pygame.display.set_caption(f'Крестики нолики ({self.won.upper()} ПОБЕДИЛ!)')

    def restart(self):
        self.won = None
        self.working = True
        self.board = [[0] * self.width for _ in range(self.height)]
        self.turn = 'red'
        pygame.display.set_caption('Крестики-нолики')

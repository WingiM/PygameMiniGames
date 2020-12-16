import pygame
from Templates.Board import Board

INDENT_LEFT, INDENT_TOP, CELL_SIZE = 100, 100, 100
COLORS = {'red': (255, 102, 102),
          'blue': (0, 153, 255)}


class TicTacToeBoard(Board):

    def __init__(self, width, height, screen):
        super().__init__(3, 3, screen)
        self.turn = 'red'

    def render(self):
        y = self.top
        for i in range(self.height):
            x = self.left
            for j in range(self.width):
                pygame.draw.rect(self.screen, COLORS[self.turn], (x, y, self.cell_size, self.cell_size), 10)
                if x != self.left:
                    pygame.draw.line(self.screen, (0, 0, 0), (x,  y), (x, y + self.cell_size), 10)
                if self.board[i][j] == 1:
                    pass  # TODO: PNG с крестиком
                if self.board[i][j] == 2:
                    pass  # TODO: PNG с ноликом
                x += self.cell_size
            if y != self.top:
                pygame.draw.line(self.screen, (0, 0, 0), (self.left, y), (self.left + self.cell_size * self.width, y), 10)
            y += self.cell_size

    def on_click(self, cell):
        x, y = cell
        self.board[y][x] = 1 if self.turn == 'red' else 2
        self.turn = 'blue' if self.turn == 'red' else 'red'


if __name__ == '__main__':
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Мини-игры')
    board = TicTacToeBoard(3, 3, screen)
    board.set_view((width - board.width * CELL_SIZE) // 2, (height - board.height * CELL_SIZE) // 2, CELL_SIZE)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill(COLORS[board.turn])
        board.render()
        pygame.display.flip()

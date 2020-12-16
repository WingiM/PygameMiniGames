import pygame
from Templates.Board import Board

INDENT_LEFT, INDENT_TOP, CELL_SIZE = 10, 10, 150

if __name__ == '__main__':
    size = width, height = 800, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Мини-игры')
    board = Board(3, 3, screen)
    board.set_view(INDENT_LEFT, INDENT_TOP, CELL_SIZE)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        board.render()
        pygame.display.flip()

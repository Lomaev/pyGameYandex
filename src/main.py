import pygame
from heroes_classes import *


class Board:
    def __init__(self, cols, rows, cell_size, top, left):
        self._cols = cols
        self._rows = rows
        self._cell_size = cell_size
        self._top = top
        self._left = left
        self.board = [[None for __ in range(cols)] for _ in range(rows)]

    def render(self, screen):
        pygame.draw.rect(screen, pygame.Color('Black'),
                         ((self._left, self._top),
                          (self._cell_size * self._cols, self._cell_size * self._rows)), 1)
        for i, row in enumerate(self.board):
            for j, elem in enumerate(row):
                self.render_cell(screen, elem, (i, j))

    def render_cell(self, screen, cell, pos):
        if (pos[0] + pos[1]) % 2 == 1:
            pygame.draw.rect(screen, pygame.Color('Black'),
                             ((self._left + self._cell_size * pos[1], self._top + self._cell_size * pos[0]),
                              (self._cell_size, self._cell_size)))

    def get_cell(self, left, top):
        top_cell = (top - self._top) // self._cell_size
        left_cell = (left - self._left) // self._cell_size
        if 0 <= top_cell < self._cols and 0 <= left_cell < self._rows:
            return top_cell, left_cell
        else:
            return None

    def get_item(self, col, row):
        try:
            return self.board[row][col]
        except BaseException:
            return None

    def set_item(self, col, row, item):
        self.board[row][col] = item

    def click(self, left, top):
        pos = self.get_cell(left, top)


def draw_UI(screen):
    screen.fill(pygame.Color('White'))
    board.render(screen)
    pygame.draw.rect(screen, pygame.Color('Black'), ((700, 80), (300, 560)), 1)


pygame.init()

screen = pygame.display.set_mode((1200, 800))

screen.fill(pygame.Color('Black'))

board = Board(8, 8, 70, 80, 120)
board.render(screen)

clock = pygame.time.Clock()

all_heroes = pygame.sprite.Group()
test_hero = BaseHero(all_heroes)
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit(0)

    draw_UI(screen)
    test_hero.rect.x = 300
    test_hero.rect.y = 300
    all_heroes.draw(screen)

    pygame.display.flip()

pygame.quit()

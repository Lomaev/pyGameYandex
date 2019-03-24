import pygame


class Board:
    def __init__(self, cols, rows, cell_size, top, left):
        self._cols = cols
        self._rows = rows
        self._cell_size = cell_size
        self._top = top
        self._left = left
        self.board = [[None for __ in range(cols)] for _ in range(rows)]
        self.enemy_HP = 25
        self.player_HP = 25

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
        if cell:
            if cell.HP <= 0:
                cell.kill()
                self.board[pos[0]][pos[1]] = None
            else:
                cell.rect.x = self._left + pos[1] * self._cell_size
                cell.rect.y = self._top + pos[0] * self._cell_size

    def get_cell(self, left, top):
        top_cell = (top - self._top) // self._cell_size
        left_cell = (left - self._left) // self._cell_size
        if 0 <= top_cell < self._cols and 0 <= left_cell < self._rows:
            return top_cell, left_cell
        else:
            return None

    def get_item(self, row, col):
        if 0 < row < self._rows and 0 < col < self._cols:
            return self.board[row][col]
        else:
            return None

    def set_item(self, col, row, item):
        self.board[row][col] = item

    def click(self, left, top):
        pos = self.get_cell(left, top)

    def add_hero(self, hero, row, col):
        if not self.board[row][col]:
            self.board[row][col] = hero
            return True
        else:
            hero.kill()
            return False

    def update_heroes(self):
        old_board = [i.copy() for i in self.board]
        for i, row in enumerate(old_board):
            for j, elem in enumerate(row):
                if elem:
                    elem.move(self, i, j)

    def check_winner(self):
        if self.enemy_HP < 0:
            return 'Player'
        elif self.player_HP < 0:
            return 'Bot'
        else:
            return False

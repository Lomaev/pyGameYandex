import pygame
import random
from heroes_classes import *
from coin_class import Coin

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
        if cell:
            if cell.HP <= 0:
                cell.kill()
                self.board[pos[0]][pos[1]] = None
            else:
                cell.rect.x = self._left + pos[1] * 70
                cell.rect.y = self._top + pos[0] * 70

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

def draw_UI(screen, hero_to_place):
    screen.fill(pygame.Color('White'))
    board.render(screen)
    pygame.draw.rect(screen, pygame.Color('Black'), ((700, 80), (300, 560)), 1)
    hero_choice_sprites.draw(screen)

    if hero_to_place == 'warrior':
        pygame.draw.rect(screen, pygame.Color('Green'), ((705, 155), (255, 100)), 3)
    elif hero_to_place == 'ranger':
        pygame.draw.rect(screen, pygame.Color('Green'), ((705, 260), (255, 100)), 3)
    elif hero_to_place == 'knight':
        pygame.draw.rect(screen, pygame.Color('Green'), ((705, 365), (255, 100)), 3)


pygame.init()

screen = pygame.display.set_mode((1200, 800))

screen.fill(pygame.Color('Black'))

board = Board(8, 8, 70, 80, 120)
board.render(screen)

clock = pygame.time.Clock()

move_time = 0
coin_animation_time = 0
summon_time = -500

all_heroes = pygame.sprite.Group()
coins_sprites = pygame.sprite.Group()
coin = Coin(coins_sprites, 720, 100)

hero_choice_sprites = pygame.sprite.Group()
warrior_choice = WarriorChoice(hero_choice_sprites)
warrior_choice.rect.x = 705
warrior_choice.rect.y = 155
ranger_choice = RangerChoice(hero_choice_sprites)
ranger_choice.rect.x = 705
ranger_choice.rect.y = 260
knight_choice = KnightChoice(hero_choice_sprites)
knight_choice.rect.x = 705
knight_choice.rect.y = 365

hero_to_place = None
heroes_be_name = {
    'warrior' : Warrior,
    'ranger' : Ranger,
    'knight' : Knight
}

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_pos = pygame.mouse.get_pos()
            if warrior_choice.rect.collidepoint(m_pos):
                hero_to_place = 'warrior'
            if ranger_choice.rect.collidepoint(m_pos):
                hero_to_place = 'ranger'
            if knight_choice.rect.collidepoint(m_pos):
                hero_to_place = 'knight'
            if 120 < m_pos[0] < 680 and 80 < m_pos[1] < 640 and hero_to_place:
                if board.add_hero(heroes_be_name[hero_to_place](all_heroes, board), 7, (m_pos[0] - 120) // 70):
                    hero_to_place = None

    draw_UI(screen, hero_to_place)
    all_heroes.draw(screen)
    coins_sprites.draw(screen)

    if move_time > 1000:
        board.update_heroes()
        move_time = 0

    if coin_animation_time > 150:
        coins_sprites.update()
        coin_animation_time = 0

    if summon_time > 2000:
        n = random.randint(0, 7)
        while board.get_item(0, n):
            n = random.randint(0, 7)

        board.add_hero(FireSkull(all_heroes, board), 0, n)

        summon_time = 0

    t = clock.tick()
    move_time += t
    coin_animation_time += t
    summon_time += t

    pygame.display.flip()

pygame.quit()

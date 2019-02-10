import pygame
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        image = image.convert_alpha()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
            image = image.convert_alpha()
        return image
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)


class BaseHero(pygame.sprite.Sprite):
    def __init__(self, group, board, side='player'):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image('test.png', colorkey=-1), (70, 70))
        self.rect = self.image.get_rect()
        self.side = side
        self.board = board
        self.HP = 2
        self.dmg = 1
        self.moved = True

    def move(self, board, row, col):
        print(self.side, row, col, self.HP)
        self.moved = False
        if self.side == 'player':
            if row == 0:
                self.board.board[row][col] = None
                self.kill()
            elif self.board.get_item(row - 1, col) and self.board.get_item(row - 1, col).side != 'player':
                self.board.get_item(row - 1, col).hit(self.dmg)
                self.attack(row, col)
            elif self.board.get_item(row - 1, col + 1) and self.board.get_item(row - 1, col + 1).side != 'player':
                self.board.get_item(row - 1, col + 1).hit(self.dmg)
                self.attack(row, col)
            elif self.board.get_item(row - 1, col - 1) and self.board.get_item(row - 1, col - 1).side != 'player':
                self.board.get_item(row - 1, col - 1).hit(self.dmg)
                self.attack(row, col)
            elif not self.board.get_item(row - 1, col):
                self.board.board[row - 1][col] = self
                self.board.board[row][col] = None
                self.moved = True
                print(row)
            else:
                print('Stopped ally.')
        else:
            if row == 7:
                self.board.board[row][col] = None
                self.kill()
            elif self.board.get_item(row + 1, col) and self.board.get_item(row + 1, col).side == 'player':
                self.board.get_item(row + 1, col).hit(self.dmg)
                self.attack(row, col)
            elif self.board.get_item(row + 1, col + 1) and self.board.get_item(row + 1, col + 1).side == 'player':
                self.board.get_item(row + 1, col + 1).hit(self.dmg)
                self.attack(row, col)
            elif self.board.get_item(row + 1, col - 1) and self.board.get_item(row + 1, col - 1).side == 'player':
                self.board.get_item(row + 1, col - 1).hit(self.dmg)
                self.attack(row, col)
            elif not self.board.get_item(row + 1, col):
                self.board.board[row + 1][col] = self
                self.board.board[row][col] = None
                self.moved = True
                print(row)
            else:
                print('Stopped enemy.')

    def hit(self, hit_dmg):
        if not self.moved:
            self.HP -= hit_dmg

    def attack(self, row, col):
        pass


class FireSkull(BaseHero):
    def __init__(self, group, board, side='bot'):
        super().__init__(group, board, side)
        self.image = pygame.transform.scale(load_image('fire_skull.png', colorkey=-1), (70, 70))
        self.rect = self.image.get_rect()
        self.HP = 1
        self.dmg = 4

    def attack(self, row, col):
        print('attak!')
        self.board.board[row][col] = None
        self.kill()
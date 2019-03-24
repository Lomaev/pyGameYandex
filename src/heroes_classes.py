import pygame
import os


def load_image(name, colorkey=None):
    if type(name) != str:
        fullname = os.path.join('data', *name)
    else:
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
        self.max_HP = 2
        self.HP = self.max_HP
        self.dmg = 1
        self.moved = True

    def move(self, board, row, col):
        self.moved = False
        if self.side == 'player':
            if row == 0:
                self.board.board[row][col] = None
                self.board.enemy_HP -= self.dmg
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
            else:
                print('Stopped ally.')
        else:
            if row == 7:
                self.board.board[row][col] = None
                self.board.player_HP -= self.dmg
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
            else:
                print('Stopped enemy.')

    def hit(self, hit_dmg, ranged=False):
        if not self.moved or self.side == 'player' or ranged:  # Solution for problems with time.
            self.HP -= hit_dmg
            return True
        else:
            return False

    def attack(self, row, col):  # For one-hit heroes and animations.
        pass


class FireSkull(BaseHero):
    def __init__(self, group, board, side='bot'):
        super().__init__(group, board, side)
        self.image = pygame.transform.scale(load_image('fire_skull.png', colorkey=-1), (70, 70))
        self.rect = self.image.get_rect()
        self.max_HP = 1
        self.HP = 1
        self.dmg = 4

    def attack(self, row, col):
        print('attak!')
        self.kill()
        self.board.board[row][col] = None


class Knight(BaseHero):
    def __init__(self, group, board, side='player'):
        super().__init__(group, board, side)
        self.image = pygame.transform.scale(load_image('Red_knight.png', colorkey=-1), (70, 70))
        self.rect = self.image.get_rect()
        self.max_HP = 5
        self.HP = 5
        self.dmg = 3

    def move(self, board, row, col):  # Now it's only players hero, so there aren't code for bot-move.
        self.moved = False
        was_hit = False  # For cleave mechanic.

        if row == 0:
            self.board.board[row][col] = None
            self.board.enemy_HP -= self.dmg
            self.kill()
        if self.board.get_item(row - 1, col) and self.board.get_item(row - 1, col).side != 'player':
            self.board.get_item(row - 1, col).hit(self.dmg)
            self.attack(row, col)
            was_hit = True
        if self.board.get_item(row - 1, col + 1) and self.board.get_item(row - 1, col + 1).side != 'player':
            self.board.get_item(row - 1, col + 1).hit(self.dmg)
            self.attack(row, col)
            was_hit = True
        if self.board.get_item(row - 1, col - 1) and self.board.get_item(row - 1, col - 1).side != 'player':
            self.board.get_item(row - 1, col - 1).hit(self.dmg)
            self.attack(row, col)
            was_hit = True
        if not was_hit and not self.board.get_item(row - 1, col):
            self.board.board[row - 1][col] = self
            self.board.board[row][col] = None
            self.moved = True
        else:
            print('Stopped ally.')

        if self.HP < self.max_HP:
            self.HP += 1


class Warrior(BaseHero):
    def __init__(self, group, board, side='player'):
        super().__init__(group, board, side)
        self.image = pygame.transform.scale(load_image('warrior.png', colorkey=-1), (70, 70))
        self.rect = self.image.get_rect()


class Ranger(BaseHero):
    def __init__(self, group, board, side='player'):
        super().__init__(group, board, side)
        self.image = pygame.transform.scale(load_image('green_redhead.png', colorkey=-1), (70, 70))
        self.rect = self.image.get_rect()
        self.max_HP = 3
        self.HP = 3
        self.dmg = 2

    def move(self, board, row, col):  # Only players hero.
        self.moved = False
        was_hit = False  # For cleave mechanic.

        if row == 0:
            self.board.board[row][col] = None
            self.board.enemy_HP -= self.dmg
            self.kill()

        for i in range(-1, 2):
            if was_hit:  # Only one attack.
                break
            for j in range(1, 3):
                if self.board.get_item(row - j, col + i) and self.board.get_item(row - j, col + i).side != 'player':
                    self.board.get_item(row - j, col + i).hit(self.dmg, ranged=True)
                    self.attack(row, col)
                    was_hit = True
                    break

        if not was_hit and not self.board.get_item(row - 1, col):
            self.board.board[row - 1][col] = self
            self.board.board[row][col] = None
            self.moved = True
        else:
            print('Stopped ally.')


class HeroChoice(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image('warrior_spawn.png', colorkey=-1), (250, 100))
        self.rect = self.image.get_rect()


class WarriorChoice(HeroChoice):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image('warrior_spawn.png', colorkey=-1), (250, 100))
        self.rect = self.image.get_rect()


class KnightChoice(HeroChoice):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image('knight_spawn.png', colorkey=-1), (250, 100))
        self.rect = self.image.get_rect()


class RangerChoice(HeroChoice):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image('ranger_spawn.png', colorkey=-1), (250, 100))
        self.rect = self.image.get_rect()

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
    def __init__(self, group, side='player'):
        super().__init__(group)
        self.image = load_image('test.png', colorkey=-1)
        self.rect = self.image.get_rect()
        self.side = side

    def move(self, board, row, col):
        if 0 <= self.row < 8 and not board.get_item(row - 1, col):
            self.row -= 1
            print(self.row)
        else:
            print('Nope')

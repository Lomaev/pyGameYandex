import pygame
import os
from heroes_classes import load_image


class Coin(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.number = 0
        self.x = x
        self.y = y
        self.update()

    def update(self, *args):
        super().update(*args)
        self.number += 1
        if self.number > 10:
            self.number = 1
        coin_image = load_image(['coin', 'Gold_%i.png' % self.number], colorkey=-1)
        coin_image = pygame.transform.scale(coin_image,
                                            (round(coin_image.get_width() * (50 / coin_image.get_height())), 50))
        self.image = coin_image
        self.rect = self.image.get_rect()
        self.rect.x = self.x + 25 - self.image.get_width() // 2
        self.rect.y = self.y

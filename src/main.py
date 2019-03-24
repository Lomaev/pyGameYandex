import pygame
import random
from heroes_classes import *
from coin_class import Coin
from board_module import Board


def draw_UI(screen, hero_to_place, moneys):
    screen.fill(pygame.Color('White'))
    board.render(screen)
    pygame.draw.rect(screen, pygame.Color('Black'), ((700, 80), (300, 560)), 1)
    hero_choice_sprites.draw(screen)
    screen.blit(coin_font.render(str(moneys), False, (0, 0, 0)), (810, 100))

    if hero_to_place == 'warrior':
        pygame.draw.rect(screen, pygame.Color('Green'), ((705, 155), (255, 100)), 3)
    elif hero_to_place == 'ranger':
        pygame.draw.rect(screen, pygame.Color('Green'), ((705, 260), (255, 100)), 3)
    elif hero_to_place == 'knight':
        pygame.draw.rect(screen, pygame.Color('Green'), ((705, 365), (255, 100)), 3)


pygame.init()
pygame.font.init()
coin_font = pygame.font.SysFont('Arial', 50)
winner_font = pygame.font.SysFont('Arial', 100)

screen = pygame.display.set_mode((1200, 800))

screen.fill(pygame.Color('Black'))

board = Board(8, 8, 70, 80, 120)
board.render(screen)

# Timers for events.
clock = pygame.time.Clock()
move_time = 0
coin_animation_time = 0
summon_time = -500

# Sprites.
all_heroes = pygame.sprite.Group()
coin_sprite = pygame.sprite.Group()
coin = Coin(coin_sprite, 720, 100)


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
    'warrior': Warrior,
    'ranger': Ranger,
    'knight': Knight
}

# Money as in-game economic.
moneys = 5

# Start screen.
screen.blit(pygame.image.load(os.path.join('data', 'start.png')), (0, 0))
pygame.display.flip()
ev = pygame.event.wait()
while ev.type != pygame.KEYDOWN:
    ev = pygame.event.wait()

# Game cycle.
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
            if 120 < m_pos[0] < 680 and 80 < m_pos[1] < 640 and hero_to_place and moneys >= 3:
                if board.add_hero(heroes_be_name[hero_to_place](all_heroes, board), 7, (m_pos[0] - 120) // 70):
                    moneys -= 3
                    hero_to_place = None

    draw_UI(screen, hero_to_place, moneys)
    all_heroes.draw(screen)
    coin_sprite.draw(screen)

    if move_time > 1000:
        moneys += 1
        board.update_heroes()
        move_time = 0

    if coin_animation_time > 150:
        coin_sprite.update()
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

    if board.check_winner():
        screen.fill(pygame.Color('White'))
        screen.blit(winner_font.render(board.check_winner() + ' wins!', False, (0, 0, 0)), (200, 100))
        screen.blit(winner_font.render('Press any key to exit.', False, (0, 0, 0)), (200, 500))
        pygame.display.flip()
        ev = pygame.event.wait()
        while ev.type != pygame.KEYDOWN:
            ev = pygame.event.wait()
        break

    pygame.display.flip()



pygame.quit()

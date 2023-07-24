import pygame

# Need to import os module to avoid driver error in console
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
import random
import math
import sys

pygame.init()
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
game_active = False
cooldown_weapon = 0
score = 0
game_level = 2
temp_boss_count = 2
obstacle = None
game_on_ = True
start_x = WIDTH / 8
start_y = HEIGHT / 2
dt = clock.tick(60) / 1000
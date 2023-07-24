import pygame
from pygame.locals import *
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
import random
import math
import sys
import info

WIDTH = info.WIDTH
HEIGHT= info.HEIGHT
play_button_image = pygame.image.load('graphics/buttons/main menu/play.png').convert_alpha()
play_button_rect = play_button_image.get_rect(center = (WIDTH/2, HEIGHT/6))

def main_menu(screen, game_active):
    if not game_active:
        screen.fill('black')
        screen.blit(play_button_image, play_button_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                game_active = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(mouse_pos):
                    game_active= True
    return game_active
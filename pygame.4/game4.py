import pygame
from pygame.locals import *
# Need to import os module to avoid driver error in console
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
import random
import math
import sys
import classes
import info
import main_menu
#import player

pygame.init()
screen_info = pygame.display.Info()
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
game_active = info.game_active
cooldown_weapon = 0
sword_cooldown = 0
score_count = 0
game_level = 2
temp_boss_count = 2
obstacle = None
game_on_ = 1
start_x = info.start_x
start_y = info.start_y
font = pygame.font.SysFont("Arial", 36)
obstacle_boss_count = 1

# Initialize sprite groups (for some reason)

player = pygame.sprite.GroupSingle()
obstacles = pygame.sprite.Group()
bullets = pygame.sprite.Group()
obstacle_boss = pygame.sprite.Group()

# Create player sprite
player_sprite = classes.Player(info.dt, start_x, start_y, obstacle, screen, cooldown_weapon, sword_cooldown)                                                    #defines player sprite
obstacle_boss_sprite = classes.Obstacle_Boss(game_level)                                           #adds player to all sprites
player.add(player_sprite)                                                   #adds player to player group
target = player.sprite                                                      # sets 'target' as player
obstacle_sprite = classes.Obstacle()
sword_sprite = classes.Sword(screen ,player_sprite)


#timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

boss_timer = pygame.USEREVENT + 2 
pygame.time.set_timer(boss_timer, 2000)

def maingame(game_active):
    global cooldown_weapon
    global obstacle_boss_count
    bullets_count =  str(player_sprite.bullet_count)
    text_surface_bullets = font.render(bullets_count, True, (255, 255, 255))
    score = str(info.score)
    text_surface_score = font.render(score, True, (255, 255, 255))         
    if game_active:
        if len(player.sprites()) == 0:
            print("The player group is empty!")
            player.add(player_sprite)
            print("player added")
            player_sprite.rect.center = (info.start_x, info.start_y)
        
        if info.score >= 10:
            obstacle_boss.add(obstacle_boss_sprite)
            obstacle_boss_count -= 1

        #backgroung
        screen.fill('Black')

        #player
        player.draw(screen)
        player.update()

        bullets.draw(screen)
        bullets.update(obstacles, obstacle_sprite, obstacle_boss, obstacle_boss_sprite)
        
        #obstacles
        obstacles.draw(screen)
        obstacles.update(target)

        obstacle_boss.draw(screen)
        obstacle_boss.update(obstacles)

        #cooldown for player_sprite.shoot()
        if player_sprite.cooldown_weapon > 0:
            player_sprite.cooldown_weapon -= 0.2
        if player_sprite.sword_cooldown > 0:
            player_sprite.sword_cooldown -= 0.2

        #quits game if collision
        game_active = classes.collisions_sprite(player, obstacles, obstacle_boss)
        screen.blit(text_surface_bullets, (WIDTH - 50, HEIGHT - 50))
        screen.blit(text_surface_score, (50, 50))

    else:
        obstacles.empty()
        obstacle_boss.empty()
        bullets.empty()
        player.empty()
        print(len(player.sprites()))

    for event in pygame.event.get():
        #quits game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            pygame.quit()
            exit()
        #in-game events                 
        if game_active:
            if event.type == obstacle_timer and game_level > 0:                 #adds obstacles
                obstacles.add(classes.Obstacle())#obstacles.add(obstacle_sprite)        #to obstacles group
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:      #shoots bullets
                player_sprite.shoot(obstacles, bullets)        #calls 'shoot()' comand in sprite player(Player())
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:      #shoots bullets
                player_sprite.sword(obstacles, obstacle_sprite, obstacle_boss, obstacle_boss_sprite)    
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                player_sprite.weapon = 2
    return game_active



while True:
    if not game_active:
        game_active = main_menu.main_menu(screen, game_active)
    game_active = maingame(game_active)
    dt = clock.tick(60) / 1000    
    pygame.display.update()
    clock.tick(60)




#add bullets to boss

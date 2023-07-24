import pygame
from pygame.locals import *
# Need to import os module to avoid driver error in console
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
import random
import math
import sys
import info
WIDTH = info.WIDTH
HEIGHT= info.HEIGHT

pygame.init()

class Sword(pygame.sprite.Sprite):
    def __init__(self, screen, player):
        super().__init__()
        self.true = False
        self.direction = None
        self.owner = player
        self.animation_index = 0
        # Initialize direction and frames
        self.update_direction_and_frames()  # Call the method to set rect attribute
        self.screen = screen
        self.rect = self.frames[self.animation_index].get_rect()

    def update_direction_and_frames(self):
        #self.direction = self.mouse_position_relative_to_sprite(self.owner)
        if self.direction == "right":
            pepe_image_sword1 = pygame.image.load('graphics/sword/sword1.png').convert_alpha()
            pepe_image_sword2 = pygame.image.load('graphics/sword/sword2.png').convert_alpha()
            pepe_image_sword3 = pygame.image.load('graphics/sword/sword3.png').convert_alpha()
            #self.rect.x += 24
        else:
            pepe_image_sword1 = pygame.image.load('graphics/sword/swordr1.png').convert_alpha()
            pepe_image_sword2 = pygame.image.load('graphics/sword/swordr2.png').convert_alpha()
            pepe_image_sword3 = pygame.image.load('graphics/sword/swordr3.png').convert_alpha()
            #self.rect.x -= 24
        self.frames = [pepe_image_sword1, pepe_image_sword2, pepe_image_sword3]


    def mouse_position_relative_to_sprite(self, sprite):
        mouse_x, _ = pygame.mouse.get_pos()

        if mouse_x < sprite.rect.x:
            return "left"
        elif mouse_x > sprite.rect.x + sprite.rect.width:
            return "right"
        else:
            return "over"

    def sword_animation(self):
        if self.animation_index >= len(self.frames):
            self.true == False
        if self.animation_index < 3 and self.true:
            self.update_direction_and_frames()  # Update direction and frames
            self.image_pepe = self.frames[int(self.animation_index)]
            self.screen.blit(self.image_pepe, self.rect)
            self.animation_index += 0.5

    def update(self):
        self.direction = self.mouse_position_relative_to_sprite(self.owner)
        if self.direction == "right":
            self.rect.center = self.owner.rect.center
            self.rect.x = self.owner.rect.x
            self.rect.y = self.owner.rect.y - 56
            self.sword_animation()
        else:
            self.rect.center = self.owner.rect.center 
            self.rect.x = self.owner.rect.x - 48
            self.rect.y = self.owner.rect.y - 56
            self.sword_animation()

class Player(pygame.sprite.Sprite):
    def __init__(self,dt, start_x, start_y, obstacle, screen, cooldown_weapon, sword_cooldown):                                                #dt, starting coordinate x and y, obstacles
        super().__init__()
        #frames
        pepe1 = pygame.image.load('graphics/pepe/pepe1.png').convert_alpha()
        self.image = pepe1
        self.rect = self.image.get_rect(center = (start_x, start_y))
        #variables
        self.speed = 300           #was 300
        self.obstacle_ = obstacle
        self.sword_sprite = Sword(screen, self)
        self.dt = dt
        self.bullet_count = 15
        self.cooldown_weapon = cooldown_weapon
        self.sword_cooldown = sword_cooldown
        self.recharge = 0
    #movement controls
    def movement(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.rect.y -= self.speed * self.dt
            if keys[pygame.K_s]:
                self.rect.y += self.speed * self.dt
            if keys[pygame.K_a]:
                self.rect.x -= self.speed * self.dt
            if keys[pygame.K_d]:
                self.rect.x += self.speed * self.dt

    #shoots bullet
    def shoot(self, obstacle, bullets):                                                                          #obstacle,all_sprites, bullets
        if self.cooldown_weapon > 0 or self.bullet_count <= 0:
            print('Wait bro.')
        else:
            bullet = Bullet(self.rect.center, obstacle)                                                                                 #sprite groups: all_sprites, bullets
            bullets.add(bullet)
            self.cooldown_weapon = 3
            self.bullet_count -= 1


    def sword(self, obstacles, obstacle_sprite, obstacle_boss, obstacle_boss_sprite):                               #obstacles group, obstacle sprite(class), obstacle_boss group, obstacle boss sprite (class)
        if self.sword_cooldown > 0:
            print("wait bruv")
        else:
            self.sword_sprite.animation_index = 0
            # Check for collisions with obstacles and boss
            colliding_obstacles = pygame.sprite.spritecollide(self.sword_sprite, obstacles, True)
            colliding_obstacle_boss = pygame.sprite.spritecollide(self.sword_sprite, obstacle_boss, False)
            if colliding_obstacles:
                self.obstacle_ = obstacle_sprite
                print('collision')
                self.obstacle_.hp -= 20
                print(self.obstacle_.hp)
                info.score += 1
            if colliding_obstacle_boss:
                self.obstacle_ = obstacle_boss_sprite
                print('collision boss')
                self.obstacle_.hp -= 20
                info.score += 10
            self.sword_sprite.true = True
            self.sword_cooldown = 1

    def update(self):
        self.movement()
        self.sword_sprite.update()
        if self.bullet_count <= 0:
            self.recharge += 1
        if self.recharge == 100:
            self.bullet_count = 15
            self.recharge = 0
            
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):                                                                            #WIDTH, HEIGHT
        super().__init__()

        ppe = random.randint(0,1)
        tron1 = pygame.image.load('graphics/pepe_enemy1/tron1.png').convert_alpha()
        self.image = tron1
        self.speed_multiplier = 3
        self.hp = 20
        if ppe:
            self.rect = self.image.get_rect(center = (random.randint(-100,WIDTH + 100), HEIGHT + 100))
        else:
            self.rect = self.image.get_rect(center = (random.randint(-100,WIDTH + 100), -100))

    #moves towards player
    def movement_attack(self, target):
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery  
        distance = math.sqrt(dx**2 + dy**2)
        if distance != 0:
            dx /= distance
            dy /= distance
        self.rect.x += dx * self.speed_multiplier
        self.rect.y += dy * self.speed_multiplier

    def check_health(self):
        if self.hp <= 0:
            self.kill()

    def update(self,target):
        self.movement_attack(target)
        self.check_health()
        
class Obstacle_Boss(pygame.sprite.Sprite):
    def __init__(self, game_level):                      #width, height
        super().__init__()
        self.ppe = game_level - 1
        tron1 = pygame.image.load('graphics/pepe_enemy_tronboss1/tronboss_1.png').convert_alpha()
        self.image = tron1
        self.hp = 10000
        if self.ppe == 1:
            self.x = 600
            self.rect = self.image.get_rect(center = (WIDTH - 100, HEIGHT / 2))
        elif self.ppe == 2:
            self.x = 200
            self.rect = self.image.get_rect(center = (WIDTH + 100, HEIGHT / 2))
        self.spawn_trons_count = 100
        
    #moves to destination
    def movement_attack(self):
        dx = self.x - self.rect.centerx
        dy = HEIGHT / 2 - self.rect.centery  
        distance = math.sqrt(dx**2 + dy**2)

        if distance != 0:
            dx /= distance
            dy /= distance
        self.rect.x += dx * 2
        self.rect.y += dy * 2

    def check_health(self):
        if self.hp <= 0:
            self.kill()
            info.score += 1

    def spawn_trons(self, obstacles):                                                                   #obstacles group
        if self.rect.x == WIDTH + 100 or self.rect.x == WIDTH - 100:
            obstacles.add(Obstacle())  # Adds obstacles

    def update(self, obstacles):
        self.movement_attack()
        self.check_health()
        self.spawn_trons(obstacles)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, obstacle):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=position)
        #self.target = target
        self.mouse_c = pygame.mouse.get_pos()
        self.dx = self.mouse_c[0] - self.rect.centerx
        self.dy = self.mouse_c[1] - self.rect.centery
        self.obstacle_ = obstacle
        self.speed_multipier = 15
    def movement_attack(self):
        distance = math.sqrt(self.dx ** 2 + self.dy ** 2)                 #constant

        #Normalize the direction vector to ensure constant speed
        if distance != 0:
            self.dx /= distance
            self.dy /= distance

        #updates x and y pos of sprite
        self.rect.x += self.dx * self.speed_multipier
        self.rect.y += self.dy * self.speed_multipier

    def collision_tron(self, obstacles, obstacle_sprite, obstacle_boss, obstacle_boss_sprite):                               #obstacles group, obstacle sprite(class), obstacle_boss group, obstacle boss sprite (class)):
        colliding_obstacles = pygame.sprite.spritecollide(self, obstacles, True)
        colliding_obstacle_boss = pygame.sprite.spritecollide(self, obstacle_boss, False)
        global score_count
        if colliding_obstacles:
            self.obstacle_ = obstacle_sprite
            print('collision')
            self.obstacle_.hp -= 20
            self.kill()
            info.score += 1
        
        if colliding_obstacle_boss:
            self.obstacle_ = obstacle_boss_sprite
            print('collision boss')
            self.obstacle_.hp -= 20
            self.kill()
            info.score += 10

        
    def update(self, obstacles, obstacle_sprite, obstacle_boss, obstacle_boss_sprite):
        self.movement_attack()
        self.collision_tron(obstacles, obstacle_sprite, obstacle_boss, obstacle_boss_sprite)                                               #Check for collision with obstacles

        if not (0 <= self.rect.x <= WIDTH and 0 <= self.rect.y <= HEIGHT):       #Remove the bullet when it goes off-screen
            self.kill()

#checks collisions between rite and player
def collisions_sprite(player, obstacles, obstacle_boss):                               #player obstacles group, obstacle_boss group,
    if pygame.sprite.spritecollide(player.sprite, obstacles, False):
        obstacles.empty()
        obstacle_boss.empty()
        return False  
    elif pygame.sprite.spritecollide(player.sprite, obstacle_boss, False):
        obstacles.empty()
        obstacle_boss.empty()
        return False
    else:
        return True
import pygame
from pygame.locals import *
# Need to import os module to avoid driver error in console
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
import random
import math
import sys


class Sword(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.owner = player
        pepe_image_sword1 = pygame.image.load('graphics/sword/sword1.png').convert_alpha()
        pepe_image_sword2 = pygame.image.load('graphics/sword/sword2.png').convert_alpha()
        pepe_image_sword3 = pygame.image.load('graphics/sword/sword3.png').convert_alpha()
        self.frames = [pepe_image_sword1, pepe_image_sword2, pepe_image_sword3]
        self.animation_index = 0
        self.true = False
        self.rect = self.frames[self.animation_index].get_rect()

    def sword_animation(self):
        if self.animation_index >= len(self.frames):
            self.true == False
        if self.animation_index < 3 and self.true:
            self.image_pepe = self.frames[int(self.animation_index)]
            screen.blit(self.image_pepe, self.rect)
            self.animation_index += 0.5
        
    def update(self):
        self.rect.topleft = self.owner.rect.topleft
        self.rect.x = self.owner.rect.x
        self.rect.y = self.owner.rect.y - 56
        self.sword_animation()

class Player(pygame.sprite.Sprite):
    def __init__(self, obstacle):
        super().__init__()
        #frames
        pepe1 = pygame.image.load('graphics/pepe/pepe1.png').convert_alpha()
        self.image = pepe1
        self.rect = self.image.get_rect(center = (WIDTH / 8, HEIGHT / 2))
        #variables
        self.speed = 300           #was 300
        self.obstacle_ = obstacle
        self.sword_sprite = Sword(self)

    #movement controls
    def movement(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.rect.y -= self.speed * dt
            if keys[pygame.K_s]:
                self.rect.y += self.speed * dt
            if keys[pygame.K_a]:
                self.rect.x -= self.speed * dt
            if keys[pygame.K_d]:
                self.rect.x += self.speed * dt

    #shoots bullet
    def shoot(self):
        global cooldown_weapon
        if cooldown_weapon > 0:
            print('Wait bro.')
        else:
            bullet = Bullet(self.rect.center, obstacle)
            all_sprites.add(bullet)
            bullets.add(bullet)
            cooldown_weapon = 3
                
    def sword(self):
        self.sword_sprite.animation_index = 0
        # Check for collisions with obstacles and boss
        colliding_obstacles = pygame.sprite.spritecollide(self.sword_sprite, obstacles, True)
        colliding_obstacle_boss = pygame.sprite.spritecollide(self.sword_sprite, obstacle_boss, False)
        global score_count
        if colliding_obstacles:
            self.obstacle_ = obstacle_sprite
            print('collision')
            score_count += 1
            self.obstacle_.hp -= 20
        if colliding_obstacle_boss:
            self.obstacle_ = obstacle_boss_sprite
            print('collision boss')
            score_count += 1 
            self.obstacle_.hp -= 20
        self.sword_sprite.true = True

    def update(self):
        self.movement()
        self.sword_sprite.update()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        ppe = random.randint(0,1)
        tron1 = pygame.image.load('graphics/pepe_enemy1/tron1.png').convert_alpha()
        self.image = tron1
        self.speed_multiplier = 1
        self.hp = 10
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
        if self.hp == 0:
            self.kill()


    def update(self,target):
        self.movement_attack(target)
        self.check_health()
        
class Obstacle_Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global game_level
        self.ppe = game_level - 1
        tron1 = pygame.image.load('graphics/pepe_enemy_tronboss1/tronboss_1.png').convert_alpha()
        self.image = tron1
        self.hp = 100
        if self.ppe == 1:
            self.x = 600
            self.rect = self.image.get_rect(center = (WIDTH - 100, HEIGHT / 2))
        elif self.ppe == 2:
            self.x = 200
            self.rect = self.image.get_rect(center = (WIDTH + 100, HEIGHT / 2))
        self.spawn_trons_count = 100
    #moves towards player
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
        if self.hp == 0:
            self.kill()

    def spawn_trons(self):
        if self.rect.x == WIDTH + 100 or self.rect.x == WIDTH - 100:
            obstacles.add(Obstacle())  # Adds obstacles

    def update(self):
        self.movement_attack()
        self.check_health()
        self.spawn_trons()
        

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
        self.speed_multipier = 10
    def movement_attack(self):
        distance = math.sqrt(self.dx ** 2 + self.dy ** 2)                 #constant

        #Normalize the direction vector to ensure constant speed
        if distance != 0:
            self.dx /= distance
            self.dy /= distance

        #updates x and y pos of sprite
        self.rect.x += self.dx * self.speed_multipier
        self.rect.y += self.dy * self.speed_multipier

    def collision_tron(self):
        colliding_obstacles = pygame.sprite.spritecollide(self, obstacles, True)
        colliding_obstacle_boss = pygame.sprite.spritecollide(self, obstacle_boss, False)
        global score_count
        if colliding_obstacles:
            self.obstacle_ = obstacle_sprite
            print('collision')
            score_count += 1
            self.obstacle_.hp -= 20
            self.kill()
        
        if colliding_obstacle_boss:
            self.obstacle_ = obstacle_boss_sprite
            print('collision boss')
            score_count += 1
            self.obstacle_.hp -= 20
            self.kill()

        
    def update(self):
        self.movement_attack()
        self.collision_tron()                                               #Check for collision with obstacles

        if not (0 <= self.rect.x <= WIDTH and 0 <= self.rect.y <= HEIGHT):       #Remove the bullet when it goes off-screen
            self.kill()

#checks collisions between rite and player
def collisions_sprite():
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
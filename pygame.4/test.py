import pygame
from pygame.locals import *
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
game_active = True
cooldown_weapon = 0
score_count = 0
game_level = 2
temp_boss_count = 2
obstacle = None
game_on_ = 1


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


# Initialize sprite groups (for some reason)
all_sprites = pygame.sprite.Group()
player = pygame.sprite.GroupSingle()
obstacles = pygame.sprite.Group()
bullets = pygame.sprite.Group()
obstacle_boss = pygame.sprite.Group()

# Create player sprite
player_sprite = Player(obstacle)                                                    #defines player sprite
obstacle_boss_sprite = Obstacle_Boss()
all_sprites.add(player_sprite)                                              #adds player to all sprites
player.add(player_sprite)                                                   #adds player to player group
target = player.sprite                                                      # sets 'target' as player
obstacle_sprite = Obstacle()
sword_sprite = Sword(player_sprite)


#timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)

boss_timer = pygame.USEREVENT + 2 
pygame.time.set_timer(boss_timer, 2000)

def main_game():
    global game_on_
    global temp_boss_count
    global game_active
    global cooldown_weapon
    if temp_boss_count:#temp_boss_count:
        obstacle_boss.add(obstacle_boss_sprite)
        temp_boss_count -= 1

    if game_active:
        #backgroung
        screen.fill('Black')

        #player
        player.draw(screen)
        player.update()

        bullets.draw(screen)
        bullets.update()
        
        #obstacles
        obstacles.draw(screen)
        obstacles.update(target)

        obstacle_boss.draw(screen)
        obstacle_boss.update()

        #cooldown for player_sprite.shoot()
        if cooldown_weapon > 0:
            cooldown_weapon -= 0.2

        #quits game if collision
        game_active = collisions_sprite()
    else:
        obstacles.empty()
        obstacle_boss.empty()
        game_active = True
        game_on_ = False

    for event in pygame.event.get():
        #quits game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            pygame.quit()
            exit()

        #starts game if 'SPACE' pressed if in intro screen
        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:   
                game_active = True
                      
        #events for game_active                 
        if game_active:
            if event.type == obstacle_timer and game_level > 0:                 #adds obstacles
                obstacles.add(Obstacle())#obstacles.add(obstacle_sprite)        #to obstacles group
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:      #shoots bullets
                player_sprite.shoot()                                           #calls 'shoot()' comand in sprite player(Player())
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:      #shoots bullets
                player_sprite.sword()    
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                player_sprite.weapon = 2

# Button properties
button_width = 200
button_height = 50
button_color = (0, 128, 255)
button_text = "Click Me!"
text_color = (255, 255, 255)
button_font = pygame.font.Font(None, 30)

def draw_button():
    pygame.draw.rect(screen, button_color, (WIDTH//2 - button_width//2, HEIGHT//2 - button_height//2, button_width, button_height))
    text_surface = button_font.render(button_text, True, text_color)
    text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text_surface, text_rect)

def main_menu():
    global game_on_
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            button_rect = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 - button_height//2, button_width, button_height)
            if button_rect.collidepoint(mouse_pos):
                print("Button clicked!")
                game_on_ = True

    screen.fill((255, 255, 255))  # Clear the screen
    draw_button()
    pygame.display.flip()  # Update the display

while True:
    print(game_on_)
    if game_on_:
        main_game()
        #game_on_ = main_game()
    else:
        main_menu()
    dt = clock.tick(60) / 1000    
    pygame.display.update()
    clock.tick(60)

#to do
'''
give trons hp instead of kill-at-hit #done

/create index that changes when a key is pressed and pass it into .shoot()
/make a if loop deciding what type of weapon player uses when .shoot()
/make different attack mechanics
    -make a sword (when .shoot(): a rect is created and every obstacle in that rect takes damage) #done

adjust bosses and bosses spowns
make a score system
add music and sounds
add a pause menu
and main menu
make a game over screen

add more enemies

make levels
    -increase boss and torn hp eveery level

add animations
'''
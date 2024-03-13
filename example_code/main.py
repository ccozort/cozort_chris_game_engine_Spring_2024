# content from kids can code: http://kidscancode.org/blog/

# sources
# getting mouse position: https://www.pygame.org/docs/ref/mouse.html#pygame.mouse.get_pos
# shorthand for loops (used in getting mouse collision with sprite): https://stackoverflow.com/questions/6475314/python-for-in-loop-preceded-by-a-variable
# fire towards mouse:
# https://stackoverflow.com/questions/63495823/how-to-shoot-a-bullet-towards-mouse-cursor-in-pygame 
# timer https://www.youtube.com/watch?v=YOCt8nsQqEo 


#  design
'''
Innovation:
Fire projectile at mouse...
Create a timer/cooldown class
Load game background image
Create particles
Create tiny healthbars above all mobs that adjust based on their hitpoints
Add double jump

Goals rules feedback freedom!!!

'''

# import libraries and modules
# from platform import platform
from hashlib import new
from itertools import count
from secrets import choice
import pygame as pg
# import settings
# from settings import *
from pygame.sprite import Sprite
import random
from random import randint, randrange
import os
from os import path
from math import *
from time import *

vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')



# sound added
pg.mixer.init

# game settings 
WIDTH = 1280
HEIGHT = 720
FPS = 30
mpos = (0,0)
PAUSED = False

# player settings
PLAYER_GRAV = 0.9
PLAYER_FRIC = 0.1
SCORE = 0

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
ORANGE = (255, 98, 0)

# images
# background = pg.image.load(path.join(img_folder, 'starfield.png'))
# background_rect = background.get_rect()
# theBell = pg.image.load(path.join(img_folder, 'theBell.png'))
# theBell_rect = background.get_rect()
# theBell.set_colorkey(BLACK)
# theBell = pg.transform.scale(theBell, (200,200))

def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

def colorbyte(x,y):
    if x < 0 or x > 255:
        x = 0
    if y > 255 or y < 0:
        y = 255
    return float(random.randint(x,y))

# create all classees as sprites...

class Cooldown():
    def __init__(self):
        self.current_time = 0
        self.event_time = 0
        self.delta = 0
    def ticking(self):
        self.current_time = floor((pg.time.get_ticks())/1000)
        self.delta = self.current_time - self.event_time
        # print(self.delta)
    def timer(self):
        self.current_time = floor((pg.time.get_ticks())/1000)

# player sprite
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.countdown = Cooldown()
        self.image = pg.Surface((50, 50))
        self.r = 0
        self.g = 0
        self.b = 255
        self.image.set_colorkey(BLACK)
        # self.image.fill((self.r,self.g,self.b))
        self.rect = self.image.get_rect()
        self.radius = 23
        pg.draw.circle(self.image, (self.r,self.g,self.b), self.rect.center, self.radius)
        # self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT-45)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.health = 100
        self.damage = 3
        self.jumppower = 16
        self.fired = False
        self.jumps = 2
        self.ammo = 100
    def controls(self):
        keys = pg.key.get_pressed()
        # if keys[pg.K_w]:
        #     self.acc.y = -5
        if keys[pg.K_a]:
            self.acc.x = -5
        # if keys[pg.K_s]:
        #     self.acc.y = 5a
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_e]:
            self.fire()
    def fire(self):
        self.ammo -= 1
        self.countdown.event_time = floor(pg.time.get_ticks()/1000)
        mpos = pg.mouse.get_pos()
        targetx = mpos[0]
        targety = mpos[1]
        distance_x = targetx - self.rect.x
        distance_y = targety - self.rect.y
        angle = atan2(distance_y, distance_x)
        speed_x = 10 * cos(angle)
        speed_y = 10 * sin(angle)
        # print(speed_x)
        if self.countdown.delta > 2:
            p = Pewpew(self.pos.x,self.pos.y - self.rect.height, 30, 30, speed_x, speed_y, "player")
        else:
            p = Pewpew(self.pos.x,self.pos.y - self.rect.height, 10, 10, speed_x, speed_y, "player")

        all_sprites.add(p)
        pewpews.add(p)

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, all_plats, False)
        self.rect.x += -1
        if hits:
            self.jumps = 2
        if self.jumps > 0:
            self.vel.y = -self.jumppower
            self.jumps -=1
            print(self.jumps)
    def draw(self):
        pass
    def inbounds(self):
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
    def update(self):
        self.countdown.ticking()
        # print(f"current time: {self.countdown.current_time} button press time: {self.countdown.event_time} delta time {self.countdown.delta}")

        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # friction
        self.acc.x += self.vel.x * -0.1
        # self.acc.y += self.vel.y * -0.1
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # self.rect.x += self.xvel
        # self.rect.y += self.yvel
        self.inbounds()
        self.rect.midbottom = self.pos
    # def draw(self):
    #     pass


# platforms
class Platform(Sprite):
    def __init__(self, x, y, w, h, typeof):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.typeof = typeof
# powerup

class Powerup(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# display image
# class Displayimage(Sprite):
#     def __init__(self, x, y):
#         Sprite.__init__(self)
#         self.image = pg.image.load(os.path.join(img_folder, 'theBell.png')).convert()
#         self.image.set_colorkey(BLACK)
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#     def update(self):
#         pass


# bullet sprite
class Pewpew(Sprite):
    def __init__(self, x, y, w, h,sx,sy, owner):
        Sprite.__init__(self)
        self.owner = owner
        self.image = pg.Surface((w, h))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        if self.owner == 'player':
            self.radius = w/2
            pg.draw.circle(self.image, YELLOW, self.rect.center, self.radius)
        else:
            self.image.fill(RED)
        self.rect.x = x
        self.rect.y = y
        self.speed_x = sx
        self.speed_y = sy
        self.fired = False
    
    def update(self):
        if self.owner == "player":
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            # print(pewpews)
        else:
            self.rect.y += self.speed_y
        if (self.rect.y < 0 or self.rect.y > HEIGHT):
            self.kill()
            # print(pewpews)

# here's the healthbar
class Healthbar(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def damage(self, newwidth):
        self.rect.w = newwidth

# here's the mobs
class Mob(Sprite):
    def __init__(self, x, y, w, h, color, typeof, health):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.color = color
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.typeof = typeof
        self.health = health
        self.currenthealth = health
        self.initialized = False
        self.healthbar = pg.Surface((self.rect.width, 5))
        self.healthbar.fill(RED)
        self.countdown = Cooldown()
        self.canshoot = True
        self.countdown.event_time = floor(pg.time.get_ticks()/1000)
    def update(self):
        self.countdown.ticking()
        self.healthbar = pg.Surface((self.rect.width*(self.currenthealth/self.health), 5))
        self.healthbar.fill(RED)

        # self.rect.y += self.speed
        if self.typeof == "boss":
            self.rect.x += self.speed*5

            if self.rect.right > WIDTH or self.rect.x < 0:
                self.speed *= -1
                self.rect.y += 25
            if self.rect.bottom > HEIGHT:
                self.rect.top = 0
        else:
            self.rect.x += self.speed
            if self.rect.right > WIDTH or self.rect.x < 0:
                self.speed *= -1
                self.rect.y += 15
            if self.countdown.delta > randint(2,25) and enemyPewpews.__len__() < 10:
                self.countdown.event_time = floor(pg.time.get_ticks()/1000)
                p = Pewpew(self.rect.x, self.rect.y, 5, 15, 0, 5, 'enemy')
                all_sprites.add(p)
                enemyPewpews.add(p)

class Particle(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = randint(2,20)*choice([-1,1])
        self.speedy = randint(2,20)*choice([-1,1])
        self.countdown = Cooldown()
        self.countdown.event_time = floor(pg.time.get_ticks()/1000)
        print('created a particle')
    def update(self):
        self.countdown.ticking()
        self.rect.x += self.speedx
        self.rect.y += self.speedy+PLAYER_GRAV
        if self.countdown.delta > 1:
            print('time to die...')
            self.kill()



# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()

# instantiate classes
player = Player()
# print(player.rect.x)
# print(player.rect.y)
plat = Platform(180, 380, 100, 35, "normal")
plat2 = Platform(289, 180, 100, 35, "ouchie")
powerup1 = Powerup(100,350, 25, 25)
ground = Platform(0, HEIGHT-40, WIDTH, 40, "lava")
# myimage = Displayimage(WIDTH/2, HEIGHT/2)

# create groups
all_sprites = pg.sprite.Group()
all_plats = pg.sprite.Group()
mobs = pg.sprite.Group()
pewpews = pg.sprite.Group()
enemyPewpews = pg.sprite.Group()
particles = pg.sprite.Group()
powerups = pg.sprite.Group()

# instantiate lots of mobs in a for loop and add them to groups
for i in range(30):
    m = Mob(randint(0,WIDTH), randint(0,int(HEIGHT/2)), 25, 25, (colorbyte(0,150),colorbyte(0,255),colorbyte(0,255)), "normal", 5)
    all_sprites.add(m)
    mobs.add(m)
    # print(m)

for i in range(2):
    m = Mob(randint(0,WIDTH), randint(0,int(HEIGHT/3)), 50, 50, (colorbyte(0,10),colorbyte(150,255),colorbyte(0,100)), "boss", 25)
    all_sprites.add(m)
    mobs.add(m)
    # print(m)

# add things to groups...
all_sprites.add(player, plat, plat2, ground, powerup1)
powerups.add(powerup1)
all_plats.add(plat, plat2, ground)
  
############################# Game loop ###########################################
# starts timer...
start_ticks = pg.time.get_ticks()

running = True
while running:
    delta = clock.tick(FPS)
    # print(clock.get_time())
    # keep the loop running using clock
    hits = pg.sprite.spritecollide(player, all_plats, False)
    if hits:
        # if hits[0].typeof == "ouchie":
        #     print("yikes I'm dead...")
        # if hits[0].typeof == "lava":
        #     print("I'm standing on the LAVA...")
        # if hits[0].typeof == "ouchie":
        #     print("yikes I'm dead...")
        # print("ive struck a plat")
        player.pos.y = hits[0].rect.top
        player.vel.y = 0

    for p in powerups:
        powerUphit = pg.sprite.spritecollide(player, powerups, True)
        if powerUphit:
            
            print("i got a powerup...")
            player.jumppower += 10

    for p in enemyPewpews:
        for pl in pewpews:
            phit = pg.sprite.spritecollide(pl, enemyPewpews, False)
            if phit:
                print(phit[0])
                particle = Particle(phit[0].rect.x, phit[0].rect.y, randint(5,10), randint(5,12))
                all_sprites.add(particle)
                phit[0].kill()
        playerhit = pg.sprite.spritecollide(player, enemyPewpews, True)
        if playerhit:
            for i in range(3):
                particle = Particle(playerhit[0].rect.x, playerhit[0].rect.y, randint(1,3), randint(1,3))
                all_sprites.add(particle)
            print('the player has been hit')
            player.health -= 1

    for p in pewpews:
            # if phit:
            #     particle = Particle(phit[0].rect.x, phit[0].rect.y, randint(1,3), randint(1,3))
            #     all_sprites.add(particle)

        mhit = pg.sprite.spritecollide(p, mobs, False)
        # print(mhit.keys())
        if mhit:
            if p.rect.width > 10:
                mhit[0].currenthealth -= player.damage
            else:
                mhit[0].currenthealth -= player.damage + 3
            for i in range(3):
                    particle = Particle(mhit[0].rect.x, mhit[0].rect.y, randint(1,3), randint(1,3))
                    all_sprites.add(particle)
            print("mob health is " + str(mhit[0].health))
            if mhit[0].currenthealth < 1:
                for i in range(30):
                    particle = Particle(mhit[0].rect.x, mhit[0].rect.y, randint(1,7), randint(1,7))
                    all_sprites.add(particle)
                mhit[0].kill()
                SCORE += 1
            p.kill()  
        # if mhit:
        #     print('hit mob ' + str(mhit[0]))
    
    mobhits = pg.sprite.spritecollide(player, mobs, True)

    if mobhits:
        # print("ive struck a mob")
        player.health -= 1
        if player.r < 255:
            player.r += 15 

    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            running = False
        # check for mouse
        if event.type == pg.MOUSEBUTTONUP:
            if player.ammo > 0:
                player.fire()
                
            # get a list of all sprites that are under the mouse cursor
            # clicked_sprites = [s for s in mobs if s.rect.collidepoint(mpos)]
            # for m in mobs:
            #     if m.rect.collidepoint(mpos):
            #         print(m)
            #         m.kill()
            #         SCORE += 1

            # print(clicked_sprites)k 
        # check for keys
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
                if PAUSED:
                    PAUSED = False
                else:
                    PAUSED = True
            if event.key == pg.K_SPACE:
                player.jump()

    if not PAUSED:  
        ############ Update ##############
        # update all sprites
        all_sprites.update()
        ############ Draw ################
        # draw the background screen
        
        screen.fill(BLACK)
        # screen.blit(background, background_rect)
        # screen.blit(theBell, ((WIDTH/2), HEIGHT/2))
    


    # draw text
    draw_text("FPS: " + str(delta), 22, RED, 64, HEIGHT / 24)
    # draw_text("Timer: " + str(seconds), 22, RED, 64, HEIGHT / 10)
    draw_text("SCORE: " + str(SCORE), 22, WHITE, WIDTH / 2, HEIGHT / 24)
    # draw_text("HEALTH: " + str(player.health), 22, WHITE, WIDTH / 2, HEIGHT / 10)
    draw_text("Player Ammo: " + str(player.ammo), 22, WHITE, WIDTH / 2, HEIGHT / 10)
    # pg.draw.polygon(screen,BROWN,[(player.rect.x, player.rect.y), (152, 230), (1056, 230),(1056, 190)])
    
    # draw player color
    # player.image.fill((player.r,player.g,player.b))

    if not PAUSED:

        # draw all sprites
        all_sprites.draw(screen)
        for m in mobs:
            screen.blit(m.healthbar, m.rect)
        pg.draw.circle(player.image, (YELLOW), player.rect.center, player.countdown.delta)

    # buffer - after drawing everything, flip display
    pg.display.flip()

pg.quit()

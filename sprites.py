# This file was created by: Chris Cozort
# This code was inspired by Zelda and informed by Chris Bradfield
import pygame as pg
from settings import *
from utils import *
from random import choice
from random import randint
from os import path


vec =pg.math.Vector2

# needed for animated sprite
SPRITESHEET = "theBell.png"
# needed for animated sprite
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')
# needed for animated sprite
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # image = pg.transform.scale(image, (width, height))
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image

def draw_health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 32
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class HealthBar(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, target, pct):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.w = w
        self.h = h
        self.image = pg.Surface((w, h))
        self.rect = self.image.get_rect()
        self.image.fill(GREEN)
        self.rect.x = x
        self.rect.y = y
        self.target = target
        self.pct = pct
    def update(self):
        self.rect.x = self.target.rect.x
        self.rect.y = self.target.rect.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, controls):
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        # super.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # added player image to sprite from the game class...
        # needed for animated sprite
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        # needed for animated sprite
        self.load_images()
        
        # self.image = game.player_img
        # self.image.fill(GREEN)
        # needed for animated sprite
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.speed = 300
        self.status = ""
        self.hitpoints = 100
        self.hitpoints = 100
        self.healthbar = HealthBar(self.game, self.rect.x, self.rect.y, self.rect.w, 5, self, self.hitpoints)
        self.cooling = False
        self.weapon_drawn = False
        self.weapon_dir = (0,0)
        self.pos = vec(0,0)
        self.dir = vec(0,0)
        # needed for animated sprite
        self.current_frame = 0
        # needed for animated sprite
        self.last_update = 0
        self.material = True
        # needed for animated sprite
        self.jumping = False
        # needed for animated sprite
        self.walking = False
        self.weapon_type = ""
        self.weapon = Weapon(self.game, self.weapon_type,self.rect.x, self.rect.y, 16, 16, (0,0))
        self.points = 0
        self.can_collide = True
        self.controls = controls
        print("player was instantiated")
    # needed for setting directions for teleportation
    def set_dir(self, d):
        self.dir = d
        # return (0,0)
    # needed for getting directions for teleportation
    def get_dir(self):
        return self.dir
    
    # modified from co-pilot plugin suggestion
    # used to teleport player in a direction with a key press
    def teleport(self, direction):
        self.x += TILESIZE * 2 * direction[0]
        self.y += TILESIZE * 2 * direction[1]
        # if direction == "up":
        #     self.y -= TILESIZE * 3
        # elif direction == "down":
        #     self.y += TILESIZE * 3
        # elif direction == "left":
        #     self.x -= TILESIZE * 3
        # elif direction == "right":
        #     self.x += TILESIZE * 3
    def get_mouse(self):
        if pg.mouse.get_pressed()[0]:
            self.weapon = Weapon(self.game, self.weapon_type, self.rect.x+TILESIZE*self.dir[0], self.rect.y+TILESIZE*self.dir[1], abs(self.dir[0]*32+5), abs(self.dir[1]*32+5), self.dir)

        if pg.mouse.get_pressed()[1]:
            print("middle click")
        if pg.mouse.get_pressed()[2]:
            print("right click")         
    def get_keys(self):
        self.walking = False
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_e]:
            self.weapon = Weapon(self.game, self.weapon_type, self.rect.x+TILESIZE*self.dir[0], self.rect.y+TILESIZE*self.dir[1], abs(self.dir[0]*32+5), abs(self.dir[1]*32+5), self.dir)
        # passes the direction of the player in order to teleport in that direction with the space bar
        if keys[pg.K_SPACE]:
            self.teleport(self.get_dir())
        if keys[self.controls[0]]:
            self.vx = -self.speed
            self.set_dir((-1,0))
            self.walking = True
        if keys[self.controls[1]]:
            self.vx = self.speed
            self.set_dir((1,0))            
            self.walking = True
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed
            self.set_dir((0,-1))
            self.rect.y = 300
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
            self.set_dir((0,1))
        if keys[pg.K_e]:
            self.pew()
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071      
    def pew(self):
        p = PewPew(self.game, self.rect.x, self.rect.y)

    # def move(self, dx=0, dy=0):
    #     if not self.collide_with_walls(dx, dy):
    #         self.x += dx
    #         self.y += dy

    # def collide_with_walls(self, dx=0, dy=0):
    #     for wall in self.game.walls:
    #         if wall.x == self.x + dx and wall.y == self.y + dy:
    #             return True
    #     return False
            
    def collide_with_walls(self, dir):
        if self.material:
            if dir == 'x':
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                if hits:
                    if self.vx > 0:
                        self.x = hits[0].rect.left - self.rect.width
                    if self.vx < 0:
                        self.x = hits[0].rect.right
                    self.vx = 0
                    self.rect.x = self.x
            if dir == 'y':
                hits = pg.sprite.spritecollide(self, self.game.walls, False)
                if hits:
                    if self.vy > 0:
                        self.y = hits[0].rect.top - self.rect.height
                    if self.vy < 0:
                        self.y = hits[0].rect.bottom
                    self.vy = 0
                    self.rect.y = self.y
    # made possible by Aayush's question!
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
                self.points += 1
            if str(hits[0].__class__.__name__) == "PowerUp":
                # self.game.collect_sound.play()
                effect = choice(POWER_UP_EFFECTS)
                self.game.cooldown.cd = 5
                self.cooling = True
                self.speed += 200
                if effect == "Invincible":
                    self.status = "Invincible"
            if str(hits[0].__class__.__name__) == "Mob":
                self.hitpoints -= 1
                hits[0].health -= 1
                if self.status == "Invincible":
                    print("you can't hurt me")
            if str(hits[0].__class__.__name__) == "Mob2":
                self.hitpoints -= 1
                hits[0].health -= 1
                if self.status == "Invincible":
                    print("you can't hurt me")
            if str(hits[0].__class__.__name__) == "Collectible":
                print("you collected a collectible")
    # needed for animated sprite
    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32),

                                ]
        self.walking_frames = [
                                self.spritesheet.get_image(64,0, 32, 32),
                                self.spritesheet.get_image(96,0, 32, 32),
                                ]
        # for frame in self.standing_frames:
        #     frame.set_colorkey(BLACK)

        # add other frame sets for different poses etc.
    # needed for animated sprite        
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            if not self.walking:
                self.image = self.standing_frames[self.current_frame]
            else:
                self.image = self.walking_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
    def update(self):
        # needed for animated sprite
        # self.animate()
        self.get_keys()
        # self.power_up_cd.ticking()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        # this order of operations for rect settings and collision is imperative
        self.rect.x = self.x
        if self.can_collide == True:
            self.collide_with_walls('x')
        self.rect.y = self.y
        if self.can_collide == True:
            self.collide_with_walls('y')
        # get mouse after x and y are set for player to place sword correctly
        self.get_mouse()
        # added coin collection with a cooldown setting
        self.collide_with_group(self.game.coins, True)
        if self.game.cooldown.cd < 1:
            self.cooling = False
        if not self.cooling:
            self.collide_with_group(self.game.power_ups, True)
        self.collide_with_group(self.game.mobs, False)
class PewPew(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.pew_pews
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE/4, TILESIZE/4))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.dir = self.game.player.dir
        print("I created a pew pew...")
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Mob":
                hits[0].hitpoints -= 1
                # print(hits[0].hitpoints)
            if str(hits[0].__class__.__name__) == "Mob2":
                hits[0].hitpoints -= 1
            # self.kill()
    def update(self):
        self.collide_with_group(self.game.mobs, False)
        self.rect.x += self.dir[0]*self.speed
        self.rect.y += self.dir[1]*self.speed
        # pass

class Weapon(pg.sprite.Sprite):
    def __init__(self, game, typ, x, y, w, h, dir):
        self.groups = game.all_sprites, game.weapons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.w = w
        self.h = h
        self.rect.width = w
        self.rect.height = h
        self.pos = vec(x,y)
        self.dir = dir
        self.typ = typ
        print("I created a sword")
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Mob":
                print("you hurt a mob!")
                hits[0].hitpoints -= 1
            if str(hits[0].__class__.__name__) == "Mob2":
                print("you hurt a mob!")
                hits[0].hitpoints -= 1
            if str(hits[0].__class__.__name__) == "Wall":
                print("you hit a wall")
                
    def track(self, obj):
        self.vx = obj.vx
        self.vy = obj.vy
        # self.rect.width = obj.rect.x+self.dir[0]*32+5
        # self.rect.width = obj.rect.y*self.dir[1]*32+5
    def update(self):
        if self.game.player.weapon_drawn == False:
            self.kill()
        self.track(self.game.player)
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.rect.y = self.y
        self.collide_with_group(self.game.mobs, False)
        self.collide_with_group(self.game.walls, True)
        # hits = pg.sprite.spritecollide(self, self.game.mobs, False)
        # if hits:
        #     hits[0].hitpoints -= 1


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Collectible(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.collectibles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    def attach(self, player):
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        self.x = player.rect.x
        self.y = player.rect.y
    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PURPLE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y, speed):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        # self.image = self.game.mob_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = speed
        self.health = 32
        self.max_health = 32

        print("created mob at", self.rect.x, self.rect.y)
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def chasing(self):
        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
  
    def draw_health(self):
        # calculate health ratio
        health_ratio = self.health / self.max_health
        # calculate width of health bar
        health_width = int(self.rect.width * health_ratio)
        # create health bar
        health_bar = pg.Rect(0, 0, health_width, 7)
        # position health bar
        health_bar.midtop = self.rect.midtop
        # draw health bar
        pg.draw.rect(self.image, GREEN, health_bar)
    # def draw_health(self):
    #     if self.hitpoints > 31:
    #         col = GREEN
    #     elif self.hitpoints > 15:
    #         col = YELLOW
    #     else:
    #         col = RED
    #     width = int(self.rect.width * self.hitpoints / MOB_HITPOINTS)
    #     self.health_bar = pg.Rect(0, 0, width, 7)
    #     if self.hitpoints < MOB_HITPOINTS:
    #         pg.draw.rect(self.image, col, self.health_bar)

    
    def update(self):
        if self.health < 1:
            self.kill()
        # self.image.blit(self.game.screen, self.pic)
        # pass
        # # self.rect.x += 1
        # self.chasing()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

class Mob2(pg.sprite.Sprite):
    def __init__(self, game, x, y, speed):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = game.mob_img
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
        # self.image = self.game.mob_img
        # self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.chase_distance = 500
        # added
        self.speed = speed
        self.chasing = True
        # self.health = MOB_HEALTH
        self.hitpoints = MOB_HITPOINTS
        self.hitpoints = 100
        self.health = 100
    def sensor(self):
        if abs(self.rect.x - self.game.player.rect.x) < self.chase_distance and abs(self.rect.y - self.game.player.rect.y) < self.chase_distance:
            self.chasing = True
        else:
            self.chasing = False
    def update(self):
        if self.hitpoints <= 0:
            self.kill()
        self.sensor()
        if self.chasing:
            self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(self.speed, 0).rotate(-self.rot)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            # equation of motion
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            # hit_rect used to account for adjusting the square collision when image rotates
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        
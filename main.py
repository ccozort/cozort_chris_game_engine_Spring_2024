# This file was created by: Chris Cozort
# per 6 is the best period
# import libraries and modules
# my first source control edit
'''
Sources:
Kids can code: https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/part%2001 
'''
'''
Game design truths:
goals, rules, feedback, freedom, what the verb, and will it form a sentence 

'''
import pygame as pg
from settings import *
from sprites import *
from utils import *
from random import randint
import sys
from os import path

# added this math function to round down the clock
from math import floor

# added level values for multiple maps
LEVEL1 = "level1.txt"
LEVEL2 = "level2.txt"

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

# Define game class...
class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        pg.mixer.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        # self.load_data()
        self.running = True
        self.paused = False
        # added images folder and image in the load_data method for use with the player
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.snd_folder = path.join(self.game_folder, 'sounds')
        self.background_img = pg.image.load(path.join(self.img_folder, 'background.png')).convert_alpha()
        self.background_rect = self.background_img.get_rect()
        self.player_img = pg.image.load(path.join(self.img_folder, 'autobot.png')).convert_alpha()
        self.mob_img = pg.image.load(path.join(self.img_folder, 'decepticon.png')).convert_alpha()
        self.mob2_img = pg.image.load(path.join(self.img_folder, 'dragon.png')).convert_alpha()
        self.map_data = []
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(self.game_folder, LEVEL1), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)

    def test_method(self):
        print("I can be called from Sprites...")
    # added level change method
    def change_level(self, lvl):
        # kill all existing sprites first to save memory
        for s in self.all_sprites:
            s.kill()
        # reset criteria for changing level
        self.player.moneybag = 0
        # reset map data list to empty
        self.map_data = []
        # open next level
        with open(path.join(self.game_folder, lvl), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
        # repopulate the level with stuff
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'm':
                    Mob2(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row)

    # Create run method which runs the whole GAME
    def new(self):
        self.load_data()
        # loading sound for use...not used yet
        pg.mixer.music.load(path.join(self.snd_folder, 'soundtrack2.wav'))
        self.collect_sound = pg.mixer.Sound(path.join(self.snd_folder, 'sfx_sounds_powerup16.wav'))
        self.sword_sound = pg.mixer.Sound(path.join(self.snd_folder, 'SHING.wav'))
        # create timer
        self.countdown_time = 35
        self.cooldown = Timer(self)
        self.mob_timer = Timer(self)
        self.mob_timer.cd = 5
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.weapons = pg.sprite.Group()
        self.pew_pews = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        for i in range (0,10):
            Coin(self, randint(0,32), randint(0,24))
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        #     Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                # if tile == 'C':
                #     Coin(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'm':
                    Mob2(self, col, row)
                if tile == 'U':
                    PowerUp(self, col, row)
        self.run()
    def run(self):
        # start playing sound on infinite loop (loops=-1)
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    def quit(self):
         pg.quit()
         sys.exit()

    def update(self):
        # tick the test timer
        if not self.paused:
            self.cooldown.ticking()
            self.mob_timer.ticking()
            self.all_sprites.update()
            if self.player.hitpoints < 1:
                self.playing = False
            if self.player.moneybag > 2:
                self.change_level(LEVEL2)
            if self.mob_timer.cd < 1:
                Mob(self, randint(1,25), randint(1,25))
                self.mob_timer.cd = 2
    
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)
    
    def draw(self):
            pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
            self.screen.fill(BGCOLOR)
            self.screen.blit(self.background_img, self.background_rect)
            # self.draw_grid()
            self.all_sprites.draw(self.screen)
            # self.player.draw_health_bar(self.screen, self.player.rect.x, self.player.rect.y, self.player.hitpoints)
            # draw the timer
            self.draw_text(self.screen, str(self.cooldown.current_time), 24, WHITE, WIDTH/2 - 32, 2)
            self.draw_text(self.screen, str(self.mob_timer.get_countdown()), 24, WHITE, WIDTH/2 - 32, 32)
            self.draw_text(self.screen, str(self.dt), 24, WHITE, WIDTH/2 - 32, 54)
            self.draw_text(self.screen, str(self.cooldown.get_countdown()), 24, WHITE, WIDTH/2 - 32, 128)
            self.draw_text(self.screen, str(self.player.points), 24, RED, WIDTH/4 - 32, 128)
            draw_health_bar(self.screen, self.player.rect.x, self.player.rect.y-8, self.player.hitpoints)
            for m in self.mobs:
                draw_health_bar(self.screen, m.rect.x, m.rect.y-8, m.hitpoints*20)
            pg.display.flip()

    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYUP:

                if event.key == pg.K_p:
                    if not self.paused:
                        self.paused = True
                    else:
                        self.paused = False
            if event.type ==pg.MOUSEBUTTONUP:
                self.player.weapon_drawn = False
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=1)
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the start screen - press any key to play", 24, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()
    def show_go_screen(self):
        # if not self.running:
        #     return
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, "This is the GO screen - press any key to play", 24, WHITE, WIDTH/2, HEIGHT/2)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False


# Instantiate the game... 
g = Game()
# use game method run to run
g.show_start_screen()
while True:
    g.new()
    # g.run()
    g.show_go_screen()
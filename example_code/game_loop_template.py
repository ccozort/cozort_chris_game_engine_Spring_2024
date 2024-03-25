import pygame as pg
from settings import *
import sys
from os import path
vec = pg.math.Vector2

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
    def load_data(self):
        pass
    def new(self):
        self.running = True
    def run(self):
        while self.running:
            self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                print('trying to quit')
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
                    self.quit()

    def update(self):
        pass
    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill((50,50,50))
        pg.display.flip()
    def quit(self):
         pg.quit()
         sys.exit()
g = Game()

while True:
    g.new()
    g.run()

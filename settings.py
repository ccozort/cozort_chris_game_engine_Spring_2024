import pygame as pg

WIDTH = 1024
HEIGHT = 768

FPS = 30

TITLE = "My Fun Game"

TILESIZE = 32


BLACK = (0,0,0)
WHITE = (255,255,255)
BGCOLOR = (0,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIGHTBLUE = (200,200,255)
RED = (255,0,0)
ORANGE = (255,140,0)
PURPLE = (255,0,255)
YELLOW = (255,255,0)
LIGHTGREY = (75,75,75)

MOB_HIT_RECT = pg.Rect(0,0,96,96)
MOB_HITPOINTS = 32


POWER_UP_EFFECTS = ["I can fly", "I'm invincible", "I'm bulletproof"]
# Player settings
# PLAYER_SPEED = 300
# create a loop that loops through the list over and over

import pygame as pg

clock = pg.time.Clock()

FPS = 30

frames = ["frame1", "frame2", "frame3", "frame4"]

then = 0
current_frame = 0
while True:
    clock.tick(FPS)
    now = pg.time.get_ticks()
    if now - then > 200:
        # print(frames[current_frame])
        print(current_frame)
        # current_frame = (current_frame + 1) % len(frames)
        current_frame = (current_frame + 1) % 20
        # current_frame = current_frame + 1
        # print("time for a new frame")
        # print(now)
        then = now
    
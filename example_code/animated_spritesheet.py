import pygame as pg

FPS = 30

frames = ["Frame1", "Frame2", "Frame3", "Frame4"]

clock = pg.time.Clock()

current_frame = 0
last_update = 0

def animate():
    global last_update
    global current_frame
    now = pg.time.get_ticks()
    if now - last_update > 350:
        print(frames[current_frame])
        current_frame = (current_frame + 1) % len(frames)
        last_update = now

while True:
    clock.tick(FPS)
    animate()
    
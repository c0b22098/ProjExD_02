import random
import sys
import pygame as pg
import numpy as np


WIDTH, HEIGHT = 1200, 700


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rect = kk_img.get_rect()
    kk_rect.center = 900, 400
    bomb_surface = pg.Surface((20, 20))
    pg.draw.circle(bomb_surface, (255, 0, 0), (10, 10), 10)
    bomb_surface.set_colorkey((0, 0, 0))
    bomb_rect = bomb_surface.get_rect()
    bomb_rect.center = random.randint(0,WIDTH), random.randint(0, HEIGHT)
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        screen.blit(bg_img, [0, 0])
        key_lst = pg.key.get_pressed()
        move_value = np.asarray((0, 0), dtype=int)
        if key_lst[pg.K_UP]: move_value[1] -= 5
        if key_lst[pg.K_DOWN]: move_value[1] += 5
        if key_lst[pg.K_LEFT]: move_value[0] -= 5
        if key_lst[pg.K_RIGHT]: move_value[0] += 5
        kk_rect.move_ip(move_value)
        screen.blit(kk_img, kk_rect)
        bomb_rect.move_ip(5, 5)
        screen.blit(bomb_surface, bomb_rect)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
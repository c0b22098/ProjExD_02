import math
import random
import sys
import pygame as pg
import numpy as np


WIDTH, HEIGHT = 1600, 900
bomb_speed = np.asarray((5, 5))
ACCS = np.arange(1, 11)


def main():
    global WIDTH, HEIGHT, ACCS, bomb_speed
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
    while(True):
        bomb_rect.center = random.randint(10,WIDTH-10), random.randint(10, HEIGHT-10)
        if np.sqrt(np.sum((np.asarray(bomb_rect.center) - np.asarray(kk_rect.center)) ** 2)) >= 800:
            break
    distance = np.asarray(((bomb_rect.center[0] - kk_rect.center[0]) , (bomb_rect.center[1] - kk_rect.center[1]))) 
    bomb_move = distance / np.sqrt(np.sum(distance ** 2)) * np.sqrt(50)
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
        if not (is_in_screen(kk_rect)[0] and is_in_screen(kk_rect)[1]):
            kk_rect.move_ip(-move_value)
        if np.array_equal(move_value, (0, 0)):
            kk_rotation = 270
            is_flip = False
        else:
            kk_rotation = math.atan2(abs(move_value[0]) * -1, move_value[1]) * 180 / np.pi
            is_flip = move_value[0] >= 0
        kk_img_roto = pg.transform.rotozoom(kk_img, kk_rotation + 90, 1.0)
        screen.blit(pg.transform.flip(kk_img_roto, is_flip, False), kk_rect)
        """
        bomb_rect.move_ip(bomb_speed * ACCS[min(tmr // 100, 9)])
        bomb_speed *= (np.full(2, 1, dtype=int) - is_in_screen(bomb_rect) * 2) * -1
        """
        distance = np.asarray(((bomb_rect.center[0] - kk_rect.center[0]) , (bomb_rect.center[1] - kk_rect.center[1]))) 
        if np.sqrt(np.sum(distance ** 2)) >= 500:
            bomb_move = distance / np.sqrt(np.sum(distance ** 2)) * np.sqrt(50)
            pg.draw.circle(bomb_surface, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (10, 10), 10)
        bomb_move *= (np.full(2, 1, dtype=int) - is_in_screen(bomb_rect) * 2) * -1
        bomb_rect.center = (min(bomb_rect.center[0], WIDTH-10), min(bomb_rect.center[1], HEIGHT-10))
        bomb_rect.move_ip(-bomb_move)
        screen.blit(bomb_surface, bomb_rect)
        if kk_rect.colliderect(bomb_rect):
            kk_img_gameover = pg.transform.rotozoom(pg.image.load("ex02/fig/8.png"), 0, 2.0)
            kk_img_gameover.get_rect().center = kk_rect.center
            screen.blit(bg_img, [0, 0])
            screen.blit(kk_img_gameover, kk_rect)
            screen.blit(bomb_surface, bomb_rect)
            pg.display.update()
            pg.time.delay(3000)
            return # こうかとんと爆弾が接触していれば終了処理
        pg.display.update()
        tmr += 1
        clock.tick(50)


def is_in_screen(target_rect : pg.Rect) -> np.array(bool, bool):
    """
    引数：こうかとんRect or 爆弾Rect
    戻り値：横方向・縦方向の真理値タプル（True：画面内／False：画面外）
    """
    
    is_is = np.asarray((None, None), dtype=bool)
    is_is[1] = (target_rect.top >= 0 and target_rect.bottom <= HEIGHT)
    is_is[0] = (target_rect.left >= 0 and target_rect.right <= WIDTH)
    return is_is
         

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
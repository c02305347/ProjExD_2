import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0)
    }
                                                    #練習１
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def sleep(sec):
    time.sleep(sec)

def draw_gameover(screen):

     go_screen=pg.Surface((WIDTH,HEIGHT))
     go_screen.set_alpha(200)
     go_screen.fill(0)
     screen.blit(go_screen,(0,0))

     fonto = pg.font.Font(None, 80)
     txt = fonto.render("Game Over",True, (255,255,255))
     screen.blit(txt, (400,HEIGHT/2-50))

     kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.5)
     kk_rct = kk_img.get_rect()
     kk_rct.center = 550, 200
     screen.blit(kk_img, kk_rct)

     pg.display.update()


def check_bound(obj_rct:pg.Rect) -> tuple[bool,bool]:

    """
    引数：こうかとん、または、爆弾のRECT
    戻り値：真理値タプル（横判定結果,縦判定結果）
    画面内ならTrue、画面外ならFalse
    """

    wid_check, heg_check = True, True
    if obj_rct.left < 0 or  WIDTH < obj_rct.right:
        wid_check = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        heg_check = False
    return wid_check, heg_check

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20,20))             #練習２
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0,WIDTH-10)
    bb_rct.centery = random.randint(0,HEIGHT-10)
    bb_img.set_colorkey((0,0,0))

    vx,vy = +5, +5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):
            draw_gameover(screen)
            sleep(5)
            print("Game Over")
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5

        for key,tpl in DELTA.items(): #練習1
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)
        wid_check, heg_check = check_bound(bb_rct)
        if not wid_check:
            vx *= -1
        if not heg_check:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

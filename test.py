from typing import Any
import pygame as pg
from random import randint
import time

pg.init()
pg.font.init()


class Base_sprite(pg.sprite.Sprite):
    def __init__(self, pic, x, y, w, h, hb_x=0, hb_y=0):
        super().__init__()
        self.picture = pg.transform.scale(pg.image.load(pic), (w, h))
        self.image = self.picture
        self.rect = self.picture.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        
        center = self.rect.center
        self.rect.width = self.rect.width- self.rect.width/100*hb_x
        self.rect.height = self.rect.height- self.rect.height/100*hb_y
        self.rect.center = center
        self.delta_x = self.rect.x - x
        self.delta_y = self.rect.y - y


    def draw(self):
        mw.blit(self.picture, (self.rect.x-self.delta_x, self.rect.y-self.delta_y))
        #pg.draw.rect(mw, (255,0,0), self.rect, 3)

class Player(Base_sprite):
        point = 0


        def update(self):
            keys = pg.key.get_pressed()
            if keys[pg.K_a] and self.rect.y >= 5:
                self.rect.y -= self.speed

            if keys[pg.K_d] and self.rect.y <= win_h - self.rect.h:
                self.rect.y += self.speed

        def update_2(self):
            keys = pg.key.get_pressed()
            if keys[pg.K_LEFT] and self.rect.y >= 5:
                self.rect.y -= self.speed

            if keys[pg.K_RIGHT] and self.rect.y <= win_h - self.rect.h:
                self.rect.y += self.speed

class Ball(pg.sprite.Sprite):
    def __init__(self, pic, x, y, w, h, speed_y=5, speed_x=5):
            self.picture = pg.transform.scale(pg.image.load(pic), (w, h))
            self.image = self.picture
            self.rect = self.picture.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.speed_x = speed_x
            self.speed_y = speed_y
            
    def update(self):
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x

        if self.rect.y <= 0 or self.rect.y >= win_h-self.rect.height:
            self.speed_y *= -1
            

        if self.rect.x <= 0:
            roket2.point += 1
            self.rect.x = win_w/2
            self.rect.y = win_h/2
            self.speed_x *= 1 if randint(0, 1) == 0 else -1
            self.speed_y *= 1 if randint(0, 1) == 0 else -1

        if self.rect.x >= win_w-self.rect.width:
            roket1.point += 1
            self.rect.x = win_w/2
            self.rect.y = win_h/2
            self.speed_x *= 1 if randint(0, 1) == 0 else -1
            self.speed_y *= 1 if randint(0, 1) == 0 else -1
            #self.speed_x *= -1

        if self.rect.colliderect(roket1.rect) or self.rect.colliderect(roket2.rect):
            ball.speed_x *= -1
            ball.speed_y *= -1
            

    

    def draw(self):
        mw.blit(self.picture, (self.rect.x, self.rect.y))
            


class Button:
    def __init__(self, x, y, width, height, text='', color=(0, 0, 0), font_color=(255, 255, 255), font_size=20):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.font_color = font_color
        self.font_size = font_size
        self.font = pg.font.Font(None, font_size)
        self.rect = pg.Rect(x, y, width, height)

    def draw(self, win):
        pg.draw.rect(win, self.color, self.rect)

        if self.text != '':
            text_surface = self.font.render(self.text, True, self.font_color)
            win.blit(text_surface, (self.x + (self.width - text_surface.get_width()) / 2, self.y + (self.height - text_surface.get_height()) / 2))

    def is_clicked(self):
        return self.rect.collidepoint(pg.mouse.get_pos()) and pg.mouse.get_pressed()[0]
            



        
def set_text(text, x,y, color=(255,1,1)):
    mw.blit(f1.render(text, True, color), (x, y))

            



win_w = 1000
win_h = 700
mw = pg.display.set_mode((win_w, win_h))
#pg.display.set_caption("")
fon = pg.transform.scale(pg.image.load("fon4.jpg"), (win_w, win_h))

win1pl = pg.transform.scale(pg.image.load("win1pl.png"), (win_w, win_h))
win2pl = pg.transform.scale(pg.image.load("win2pl.png"), (win_w, win_h))

clock = pg.time.Clock()
mw.blit(fon, (0, 0))

roket1 = Player("ping_rocket1.png", 40, 30, 40, 150, 0, 0)
roket2 = Player("ping_rocket2.png", win_w-40-40, 30, 40, 150, 0, 0)

ball = Ball('ball2.png', win_w/2, win_h/2, 70, 70)


but1 = Button(win_w-220, 20, 200, 100, "Реванш", (27, 215, 42), (0,0,0), 50)

f1 = pg.font.Font(None, 36)

clicks = 0
ticks = 0
win = 0
game = True
play = True
while play:
    mw.blit(fon, (0, 0))


    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            play = False
    
    if game:
        roket1.draw()
        roket1.update()

        roket2.draw()
        roket2.update_2()
        
        ball.draw()
        ball.update()

        set_text(str(roket1.point), 20, 20)
        set_text(str(roket2.point), win_w-50, 20)

        if roket1.point == 10:
            win = 1
            game = False
        if roket2.point == 10:
            win = 2
            game = False

    else:
        if win == 1:
            mw.blit(win1pl, (0, 0))
        if win == 2:
            mw.blit(win2pl, (0, 0))
        
        but1.draw(mw)
        if but1.is_clicked():
            game = True
            roket1.point = 0
            roket2.point = 0
        #mw.blit(y_lose, (0, 0))
    

    pg.display.update()
    clock.tick(60)
    ticks += 1
    # print(len(stars))



#
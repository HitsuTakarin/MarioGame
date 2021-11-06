from typing import Text
import pygame
import sys
import itertools
from pygame import color
from pygame.constants import K_RETURN, K_TAB, KSCAN_KP_ENTER, TEXTINPUT
from pygame.time import Clock
import pygame as pg
pygame.init()

#Untuk Mengatur Layar Display
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
FPS = 30
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

#Mengatur Hal Yang Tidak Berubah Saat Game
ADD_NEW_FLAME_RATE = 25
cactus_img = pygame.image.load('cactus_bricks.png')
cactus_img_rect = cactus_img.get_rect()
cactus_img_rect.left = 0
fire_img = pygame.image.load('fire_bricks.png')
fire_img_rect = fire_img.get_rect()
fire_img_rect.left = 0
CLOCK = pygame.time.Clock()
font = pygame.font.SysFont('forte', 20)

canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Mario')

#Membuat Topscore (Skor Tertinggi)
class Topscore:
    def __init__(self):
        self.high_score = 0
    def top_score(self, score):
        if score > self.high_score:
            self.high_score = score
        return self.high_score

topscore = Topscore()

#Membuat Kelas dari Dragon
class Dragon:
    #Karena kita ingin memakai kelas nantinya, maka kita harus memasukan apa saja yang ada dalam dragon dengan __init__ dan self untuk pengoperasian
    def __init__(self):
        self.dragon_img = pygame.image.load('dragon.png')
        self.dragon_img_rect = self.dragon_img.get_rect()
        self.dragon_img_rect.width -= 10
        self.dragon_img_rect.height -= 10
        self.dragon_img_rect.top = WINDOW_HEIGHT/2
        self.dragon_img_rect.right = WINDOW_WIDTH
        self.up = True
        self.down = False

    def update(self):
        canvas.blit(self.dragon_img, self.dragon_img_rect)
        if self.dragon_img_rect.top <= cactus_img_rect.bottom:
            self.up = False
            self.down = True
        elif self.dragon_img_rect.bottom >= fire_img_rect.top:
            self.up = True
            self.down = False
        #Membagi Kecepatan dari Dragon per Level
        if self.up:
            if LEVEL == 1:
                self.dragon_img_rect.top -= 10
            elif LEVEL == 2:
                self.dragon_img_rect.top -= 20
            elif LEVEL == 3:
                self.dragon_img_rect.top -= 30
            elif LEVEL == 4:
                self.dragon_img_rect.top -= 40
            elif LEVEL == 5:
                self.dragon_img_rect.top -= 50
        elif self.down:
            if LEVEL == 1:
                self.dragon_img_rect.top += 10
            elif LEVEL == 2:
                self.dragon_img_rect.top += 20
            elif LEVEL == 3:
                self.dragon_img_rect.top += 30
            elif LEVEL == 4:
                self.dragon_img_rect.top += 40
            elif LEVEL == 5:
                self.dragon_img_rect.top += 50

#Membuat Kelas dari Api
class Flames:
    def __init__(self):
        self.flames = pygame.image.load('fireball.png')
        self.flames_img = pygame.transform.scale(self.flames, (20, 20))
        self.flames_img_rect = self.flames_img.get_rect()
        self.flames_img_rect.right = dragon.dragon_img_rect.left
        self.flames_img_rect.top = dragon.dragon_img_rect.top + 30
        self.flames_velocity = 20


    def update(self):
        canvas.blit(self.flames_img, self.flames_img_rect)
        #Membagi Kecepatan Api per Level
        if self.flames_img_rect.left > 0:
            if LEVEL == 1:
                self.flames_img_rect.left -= 20
            elif LEVEL == 2:
                self.flames_img_rect.left -= 25
            elif LEVEL == 3:
                self.flames_img_rect.left -= 30
            elif LEVEL == 4:
                self.flames_img_rect.left -= 35
            elif LEVEL == 5:
                self.flames_img_rect.left -= 40

#Membagi Kelas dari Mario
class Mario:
    def __init__(self):
        self.mario_img = pygame.image.load('mario.png')
        self.mario_img_rect = self.mario_img.get_rect()
        self.mario_img_rect.left = 20
        self.mario_img_rect.top = WINDOW_HEIGHT/2 - 100
        self.down = False
        self.up = False
        self.right = False
        self.left = False

    def update(self):
        #Memanggil Kelas dari Dragon dan Flames
        dragon = Dragon()
        flames = Flames()
        canvas.blit(self.mario_img, self.mario_img_rect)
        #Membuat Kondisi dimana saja Mario Kalah (Game Over)
        if self.mario_img_rect.top <= cactus_img_rect.bottom:
            game_over()
            if SCORE > self.mario_score:
                self.mario_score = SCORE
        if self.mario_img_rect.bottom >= fire_img_rect.top:
            game_over()
            if SCORE > self.mario_score:
                self.mario_score = SCORE
        if self.mario_img_rect.left < 0 or self.mario_img_rect.right >= flames.flames_img_rect.right:
            game_over()
            if SCORE > self.mario_score:
                self.mario_score = SCORE
        if SCORE == 60:
            game_finish()
            if SCORE > self.mario_score:
                self.mario_score = SCORE
        #Membuat Kecepatan dari Mario
        if self.up:
            self.mario_img_rect.top -= 10
        if self.down:
            self.mario_img_rect.bottom += 10
        if self.right:
            self.mario_img_rect.right += 10
        if self.left:
            self.mario_img_rect.left -= 10

#Membuat fungsi dari Game Over
def game_over():
    pygame.mixer.music.stop()
    music = pygame.mixer.Sound('mario_dies.wav')
    music.play()
    topscore.top_score(SCORE)
    game_over_img = pygame.image.load('end.png')
    game_over_img_rect = game_over_img.get_rect()
    game_over_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(game_over_img, game_over_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                music.stop()
                game_loop()
        pygame.display.update()

def game_finish():
    pygame.mixer.music.stop()
    topscore.top_score(SCORE)
    game_finish_img = pygame.image.load('finish.png')
    game_finish_img_rect = game_finish_img.get_rect()
    game_finish_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(game_finish_img, game_finish_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                game_loop()
        pygame.display.update()

def paused():
    pause_img = pygame.image.load('pause.png')
    pause_img_rect = pause_img.get_rect()
    pause_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(pause_img, pause_img_rect)
    is_pause = True
    while is_pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                else:
                    is_pause = False
        pygame.display.update()


def start_game():
    canvas.fill(BLACK)
    start_img = pygame.image.load('start2.png')
    start_img_rect = start_img.get_rect()
    start_img_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
    canvas.blit(start_img, start_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                game_loop()
        pygame.display.update()


def check_level(SCORE):
    global LEVEL
    speed = Flames()
    cactus_img_rect.bottom = 50
    fire_img_rect.top = WINDOW_HEIGHT - 50
    if SCORE in range(0, 10):
        LEVEL = 1
    elif SCORE in range(10, 20):
        LEVEL = 2
    elif SCORE in range(20, 30):
        LEVEL = 3
    elif SCORE in range (30,40):
        LEVEL = 4
    elif SCORE > 40:
        LEVEL = 5

def answer():
    screen = pg.display.set_mode((1200, 600))
    font = pg.font.Font(None, 32)
    clock = pg.time.Clock()
    input_box = pg.Rect(400, 250, 140, 32)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive
    active = False
    global kunjaw
    text = ''
    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        kunjaw = text.split(' ')
                        done = True
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((0, 0, 0))
        txt_surface = font.render(text, True, color)
        width = max(400, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pg.draw.rect(screen, color, input_box, 2)

        pg.display.flip()
        clock.tick(30)

def game_loop():
    while True:
            global dragon
            dragon = Dragon()
            flames = Flames()
            mario = Mario()
            add_new_flame_counter = 0
            global SCORE
            SCORE = 0
            global  HIGH_SCORE
            global nilai
            nilai = 0
            flames_list = []
            pygame.mixer.music.load('mario_theme.wav')
            pygame.mixer.music.play(-1, 0.0)
            while True:
                canvas.fill(BLACK)
                check_level(SCORE)
                dragon.update()
                add_new_flame_counter += 1

                if add_new_flame_counter == ADD_NEW_FLAME_RATE:
                    add_new_flame_counter = 0
                    new_flame = Flames()
                    flames_list.append(new_flame)
                for f in flames_list:
                    if f.flames_img_rect.left <= 0:
                        flames_list.remove(f)
                        SCORE += 1
                    f.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            paused()
                        elif event.key == pygame.K_1:
                            SCORE = 60
                        elif event.key == pygame.K_UP:
                            mario.up = True
                        elif event.key == pygame.K_DOWN:
                            mario.down = True
                        elif event.key == pygame.K_RIGHT:
                            mario.right = True
                        elif event.key == pygame.K_LEFT:
                            mario.left = True
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_UP:
                            mario.up = False
                        elif event.key == pygame.K_DOWN:
                            mario.down = False
                        elif event.key == pygame.K_RIGHT:
                            mario.right = False
                        elif event.key == pygame.K_LEFT:
                            mario.left = False    
                
                if SCORE == 10:
                    mario.up = False
                    mario.down = False
                    mario.left = False
                    mario.right = False
                    question = pygame.image.load('question1.png')
                    question_rect = question.get_rect()
                    question_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
                    canvas.blit(question,question_rect)
                    is_pause = True
                    while is_pause:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                    answer()
                                    if event.key == K_RETURN:
                                        is_pause = False
                                        SCORE += 1
                        pygame.display.update()
                    if ('29th' in kunjaw or '29' in kunjaw) and 'february' in kunjaw:
                        nilai += 1
                elif SCORE == 20:
                    mario.up = False
                    mario.down = False
                    mario.left = False
                    mario.right = False
                    question = pygame.image.load('question2.png')
                    question_rect = question.get_rect()
                    question_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
                    canvas.blit(question,question_rect)
                    is_pause = True
                    while is_pause:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                    answer()
                                    if event.key == K_RETURN:
                                        is_pause = False
                                        SCORE += 1
                        pygame.display.update()
                    if 'map' in kunjaw or 'maps' in kunjaw:
                        nilai += 1
                elif SCORE == 30:
                    mario.up = False
                    mario.down = False
                    mario.left = False
                    mario.right = False
                    question = pygame.image.load('question3.png')
                    question_rect = question.get_rect()
                    question_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
                    canvas.blit(question,question_rect)
                    is_pause = True
                    while is_pause:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                    answer()
                                    if event.key == K_RETURN:
                                        is_pause = False
                                        SCORE += 1
                        pygame.display.update()
                    if 'coin' in kunjaw or 'coins' in kunjaw:
                        nilai += 1
                elif SCORE == 40:
                    mario.up = False
                    mario.down = False
                    mario.left = False
                    mario.right = False
                    question = pygame.image.load('question4.png')
                    question_rect = question.get_rect()
                    question_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
                    canvas.blit(question,question_rect)
                    is_pause = True
                    while is_pause:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                    answer()
                                    if event.key == K_RETURN:
                                        is_pause = False
                                        SCORE += 1
                        pygame.display.update()
                    if 'age' in kunjaw or 'ages' in kunjaw:
                        nilai += 1
                elif SCORE == 50:
                    mario.up = False
                    mario.down = False
                    mario.left = False
                    mario.right = False
                    question = pygame.image.load('question5.png')
                    question_rect = question.get_rect()
                    question_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
                    canvas.blit(question,question_rect)
                    is_pause = True
                    while is_pause:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                    answer()
                                    if event.key == K_RETURN:
                                        is_pause = False
                                        SCORE += 1
                        pygame.display.update()
                    if 'in' in kunjaw and 'harmonia' in kunjaw and 'progressio' in kunjaw:
                        nilai += 1
                score_font = font.render('Score:'+str(SCORE), True, GREEN)
                score_font_rect = score_font.get_rect()
                score_font_rect.center = (200, cactus_img_rect.bottom + score_font_rect.height/2)
                canvas.blit(score_font, score_font_rect)

                level_font = font.render('Level:'+str(LEVEL), True, GREEN)
                level_font_rect = level_font.get_rect()
                level_font_rect.center = (500, cactus_img_rect.bottom + score_font_rect.height/2)
                canvas.blit(level_font, level_font_rect)

                top_score_font = font.render('Top Score:'+str(topscore.high_score),True,GREEN)
                top_score_font_rect = top_score_font.get_rect()
                top_score_font_rect.center = (800, cactus_img_rect.bottom + score_font_rect.height/2)
                canvas.blit(top_score_font, top_score_font_rect)

                top_nilai_font = font.render('Nilai:'+str(nilai),True,GREEN)
                top_nilai_font_rect = top_score_font.get_rect()
                top_nilai_font_rect.center = (1100, cactus_img_rect.bottom + score_font_rect.height/2)
                canvas.blit(top_nilai_font, top_nilai_font_rect)

                canvas.blit(cactus_img, cactus_img_rect)
                canvas.blit(fire_img, fire_img_rect)
                mario.update()
                for f in flames_list:
                    if f.flames_img_rect.colliderect(mario.mario_img_rect):
                        game_over()
                        if SCORE > mario.mario_score:
                            mario.mario_score = SCORE
                pygame.display.update()
                CLOCK.tick(FPS)


start_game()



import tkinter.messagebox

import pygame
from sys import exit
from pygame.locals import *
import random
import tkinter as tk

screen_size = (width, height) = (480, 800)
path_ = 'source/'


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_image, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_image
        self.rect = bullet_image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        self.rect.top -= self.speed


class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img,plane_down_imgs, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = plane_img
        self.down_imgs = plane_down_imgs
        self.rect = player_rect
        self.rect.topleft = init_pos
        self.speed = 8
        self.bullets = pygame.sprite.Group()
        self.img_index = 0
        self.is_hit = False
        self.model = 1

    def shoot(self, bullet_img):
        if self.model == 1:
            bullet = Bullet(bullet_img, self.rect.midtop)
            self.bullets.add(bullet)
        elif self.model >= 2:
            bullet1 = Bullet(bullet_img,(self.rect.midtop[0]-15,self.rect.midtop[1]))
            bullet2 = Bullet(bullet_img,(self.rect.midtop[0]+15,self.rect.midtop[1]))
            self.bullets.add(bullet1)
            self.bullets.add(bullet2)

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.bottom >= height:
            self.rect.bottom = height
        else:
            self.rect.bottom += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.right >= width:
            self.rect.right = width
        else:
            self.rect.right += self.speed


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_img, enemy_down_imgs, init_pos,is_plane=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 2
        self.down_index = 0
        self.is_plane = is_plane
        if is_plane:
            self.life = 50
        else:
            self.life = 2

    def move(self):
        self.rect.top += self.speed

class Clip(pygame.sprite.Sprite):
    def __init__(self,clip_img,init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = clip_img
        self.rect = self.image.get_rect()
        self.speed = 5
        self.rect.topleft = init_pos

    def move(self):
        self.rect.top += self.speed


# 游戏结束
def gameOver():
    font = pygame.font.Font(None, 48)
    text = font.render('Score:' + str(score), True, (255, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery + 24
    game_over_font = pygame.font.Font(None, 100)
    game_over_suf = game_over_font.render('Game Over!', True, (255, 0, 0))
    game_over_rect = game_over_suf.get_rect()
    game_over_rect.centerx = screen.get_rect().centerx
    game_over_rect.centery = screen.get_rect().centery - 50
    screen.blit(game_over_suf, game_over_rect)
    screen.blit(text, text_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                exit()
        pygame.display.update()


running = False
pygame.init()
def is_begin():
    global running
    begin.destroy()
    pygame.mixer.music.stop()
    running = True

begin = tkinter.Tk()
begin.title('飞机大战')
pygame.mixer.music.load(path_+'san.ogg')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
pika = tkinter.Canvas(begin, width=600, height=256)
image = tkinter.PhotoImage(file=path_+'pika.gif')
pika.create_image(0, 0,anchor='nw',image=image)
pika.pack()
tkinter.Button(text='开始游戏',command=is_begin).pack(side='bottom')

begin.mainloop()

screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('飞机大战')
bullet_sound = pygame.mixer.Sound(path_+'f_gun_1.WAV')
enemy1_down_sound = pygame.mixer.Sound(path_+'explode_1.WAV')
game_over_sound = pygame.mixer.Sound(path_+'10_1.WAV')
bullet_sound.set_volume(0.3)
enemy1_down_sound.set_volume(0.3)
game_over_sound.set_volume(0.3)
pygame.mixer.music.load(path_+'game_music_1.WAV')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.25)
background = pygame.image.load(path_+'background.jpg').convert_alpha()

player_image = pygame.image.load(path_+'player.png')
player_rect = player_image.get_rect()
player_down_img = []
player_down_img.append(pygame.image.load(path_+'playerBoom1.png'))
player_down_img.append(pygame.image.load(path_+'playerBoom2.png'))
player_down_img.append(pygame.image.load(path_+'playerBoom3.png'))
player_pos = [200, 600]
player = Player(player_image,player_down_img, player_rect, player_pos)

bullet_image = pygame.image.load(path_+'bullet2.jpg')
bullet_rect = bullet_image.get_rect()
clip_img = pygame.image.load(path_+'clip.png')
clip_rect = clip_img.get_rect()
enemy_img = pygame.image.load(path_+'enemy.png')
enemy_rect = enemy_img.get_rect()
enemy_down_img = []
enemy_down_img.append(pygame.image.load(path_+'enemy.png'))
enemy_down_img.append(pygame.image.load(path_+'enemy2.png'))
enemy_down_img.append(pygame.image.load(path_+'enemy3.png'))

enemyPlane_img = pygame.image.load(path_+'enemyPlane.png')
enemyPlane_rect = enemyPlane_img.get_rect()
enemyPlane_down_img = []
enemyPlane_down_img.append(pygame.image.load(path_+'enemyPlane.png'))
enemyPlane_down_img.append(pygame.image.load(path_+'enemyPlane1.png'))
enemyPlane_down_img.append(pygame.image.load(path_+'enemyPlaneBoom.png'))

enemies = pygame.sprite.Group()
enemies_down = pygame.sprite.Group()
clips = pygame.sprite.Group()
shoot_frequency = 15
shoot = 0
enemy_frequency = 0
player_down_index = 16
score = 0
clock = pygame.time.Clock()
game_clock = 0

while running:
    clock.tick(60)

    if not player.is_hit:
        if game_clock % shoot_frequency == 0:
            bullet_sound.play()
            player.shoot(bullet_image)
        game_clock += 1

        if game_clock > shoot_frequency * 1000:
            game_clock = 0

    for bullet in player.bullets:
        bullet.move()
        if bullet.rect.bottom < 0:
            player.bullets.remove(bullet)

    if enemy_frequency % 50 == 0:
        enemy_pos = [random.randint(0, width - enemy_rect.width), 0]
        enemy = Enemy(enemy_img, enemy_down_img, enemy_pos)
        enemies.add(enemy)
    if enemy_frequency % 750 == 0:
        enemyPlane_pos = [random.randint(0, width - enemyPlane_rect.width), 0]
        enemyPlane = Enemy(enemyPlane_img,enemyPlane_down_img,enemyPlane_pos,True)
        enemies.add(enemyPlane)

        clip_pos = [random.randint(0, width - clip_rect.width), 0]
        clip = Clip(clip_img,clip_pos)
        clips.add(clip)

    enemy_frequency += 1
    enemy_frequency %= 750

    for clip in clips:
        clip.move()
        if pygame.sprite.collide_mask(player,clip):
            player.model += 1
            if player.model >= 3:
                shoot_frequency = 5
            clips.remove(clip)
        if clip.rect.top > height:
            clips.remove(clip)

    for enemy in enemies:
        enemy.move()
        if pygame.sprite.collide_mask(enemy,player):
            enemies_down.add(enemy)
            enemies.remove(enemy)
            game_over_sound.play()
            player.is_hit = True
            while player.img_index <= 23:
                screen.blit(player.down_imgs[player.img_index // 8], player.rect)
                player.img_index += 1
                pygame.display.update(player.rect)
            break
        if enemy.rect.top > height:
            enemies.remove(enemy)

    enemies_downed = pygame.sprite.groupcollide(enemies,player.bullets,False,True)  # 返回字典，key为enemies对象，value为列表，
    for enemy_down in enemies_downed.keys():                                              # 包含与key发生碰撞的player对象组
        enemy_down.life -= len(enemies_downed[enemy_down])
        if enemy_down.life <= 0:
            enemies.remove(enemy_down)
            enemies_down.add(enemy_down)

    screen.fill(0)
    screen.blit(background,(0,0))
    # 玩家是否被击中
    if not player.is_hit:
        screen.blit(player.image,player.rect)
        #player.img_index = shoot_frequency // 8
    else:
        #player.img_index = player_down_index // 8
        #player_down_index += 1
        #if player_down_index > 47:
        is_continue = tkinter.messagebox.askyesno('您失败了','Score:'+str(score))
        if is_continue:
            score = 0
            clips.empty()
            enemies.empty()
            enemies_down.empty()
            player.is_hit = False
            player.model = 1
            player.rect.topleft = (200,600)
            player.img_index = 0
        else:
            running = False
            gameOver()

    for enemy_down in enemies_down:
        if enemy_down.down_index == 0:
            enemy1_down_sound.play()
        if enemy_down.down_index > 8:
            enemies_down.remove(enemy_down)
            score += 100
            continue
        screen.blit(enemy_down.down_imgs[enemy_down.down_index // 3],enemy_down.rect)
        enemy_down.down_index += 1
    # 绘制精灵组
    player.bullets.draw(screen)
    enemies.draw(screen)
    clips.draw(screen)
    # 分数显示
    score_font = pygame.font.Font(None,36)
    score_text = score_font.render(str(score),True,(128,128,128))
    text_rect = score_text.get_rect()
    text_rect.topleft = [10,10]
    screen.blit(score_text,text_rect)

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            exit()
    # 按键检测
    key_pressed = pygame.key.get_pressed()
    if not player.is_hit:
        if key_pressed[K_w] or key_pressed[K_UP]:
            player.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            player.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            player.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            player.moveRight()


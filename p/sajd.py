from pygame import *
from random import randint
from time import time as timer

#Шрифти і написи
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN', True, (255,255,255))
lose = font1.render('YOU LOSE', True, (180, 0, 0))
font2 = font.Font(None, 36)

#music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_bulled = 'bulled.png'
img_enemy = 'ufo.png'
img_ast = 'asteroid.png'

score = 0
goal = 10
lost = 0
max_lost = 0
life = 3

class GameSprite(sprite.Sprite):
    def init(self, player_image, player_y, player_x, size_x, size_y, player_speed):
        sprite.Sprite.init(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x = self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bulled = Bulled(img_bulled, self.rect.centerx, self.rect.top, 15, 20, -15)
        bulleds.add(bulled)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += set.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bulled(GameSprite):
    def update(self):
        self.rect.yb += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width,win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy(img_ast, randint(30, win_width -30), -40, 70, 50,randint(1,7))
    asteroids.add(asteroid)

bulleds = sprite.Group()

finish = False
run = True
rel_time = False
num_fire = 0

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()

                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        window.blit(background, (0,0))

        ship.update()
        monsters.update()
        bulleds.update()

        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bulleds.draw(window)

        if rel_time == True:
            now_time = timer()
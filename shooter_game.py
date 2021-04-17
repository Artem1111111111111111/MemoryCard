from pygame import *
from random import randint
'''Необходимые классы'''
#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
   #конструктор класса
   def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
       super().__init__()
       # каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (player_width, player_height))
       self.speed = player_speed
       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 85:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.y, 10, 15, -10)
        bullets.add(bullet)
lost = 0
class Enemy(GameSprite):
   def update(self):
       self.rect.y += self.speed
       global lost
       if self.rect.y > win_height:
           self.rect.y = 0
           self.rect.x = randint(80, win_width - 80)
           self.speed = randint(1,3)
           lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
#Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
#Персонажи игры:
player = Player('rocket.png', 5, win_height - 105,80, 100, 7)
monsters = sprite.Group()
bullets = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, win_width - 80), 0, 80, 60, randint(1,2))
    monsters.add(monster)
game = True
finish = False
clock = time.Clock()
FPS = 60
font.init()
font = font.SysFont('Arial', 30)
lost = 0
text_lose = font.render('Пропущено: ' + str(lost), True, (255,255,255))
win = font.render('YOU WIN!', True, (255,215,0))
lose = font.render('YOU LOSE!', True, (180,0,0))

score = 0
goal = 15
max_lost = 5

#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()
    if finish != True:
        window.blit(background,(0, 0))
        text_lose = font.render('Пропущено: ' + str(lost), True, (255,255,255))
        window.blit(text_lose, (30, 20))
        player.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        player.reset()
        sprites_list = sprite.spritecollide(player, monsters, False)
        if sprite.spritecollide(player, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (300, 200))
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), 0, 80, 60, randint(1,3))
            monsters.add(monster)
        if score >= goal:
            finish = True
            window.blit(win, (300, 250))
        text_score = font.render('Сбито: ' + str(score), True, (255,255,255))
        window.blit(text_score, (30, 50))



    display.update()
    clock.tick(FPS)






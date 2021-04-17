'''
#Создай собственный Шутер!
from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (90,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect_x = player_x
        self.rect_y = player_y
    def reset(self):
        window.blit(self.image, (self.rect_x, self.rect_y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect_x > 5:
            self.rect_x -= self.speed
        if keys_pressed[K_d] and self.rect_x < 595:
            self.rect_x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect_x,0,15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect_y += self.speed
        global lost
        if self.rect_y >= win_height:
            self.rect_y = 0
            self.rect_x = randint(30 , win_width - 100)
            self.speed = randint(1 , 5)
            lost += 5

class Bullet(GameSprite):
    def update(self):
        self.rect_y -= self.speed
        if self.rect_y == 0:
            self.kill()

win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter SAS")
background = transform.scale(image.load("sas.png"),(win_width, win_height))

mixer.init()
mixer.music.load('sasa.mp3')
mixer.music.play()

hero = Player('hero.png',300,400,10)
bullets = sprite.Group()
monsters = sprite.Group()
for i in range (6):
    ufo = Enemy ("cyborg.png", randint(30 , win_width - 100), 0, randint(1 , 5))
    monsters.add(ufo)
font.init()
font = font.Font(None,70)
lost = 0

game = True
clock = time.Clock()
FPS = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                hero.fire()
    if lost >= 20:
        game = False

    window.blit(background,(0,0))

    hero.update()
    monsters.update()
    bullets.update()

    hero.reset()
    monsters.draw(window)
    bullets.draw(window)

    collides = sprite.groupcollide(monsters,bullets,True,True)
    for c in collides:
        lost += 1
        ufo = Enemy ("cyborg.png", randint(30 , win_width - 100), 0, randint(1 , 5))
        monsters.add(ufo)
    if sprite.spritecollide(hero,monsters,False) or lost>=3:
        game = False

    text_lose = font.render("score: " + str(lost) , 1 , (255,150,0))
    window.blit(text_lose,(450,20))

    clock.tick(FPS)
    display.update()
    '''
from pygame import *
from random import randint

font.init()
font1 = font.SysFont("Arial", 80)
win = font1.render('ПОБЕДА!', True, (255, 255, 255))
lose = font1.render('ПРОЕГРЫШ!', True, (180, 0, 0))
font2 = font.SysFont("Arial", 36)

#фоновая музыка
mixer.init()
mixer.music.load('sasa.mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = "sas.png"
img_bullet = "bullet.png"
img_hero = "hero.png"
img_enemy = "cyborg.png"
score = 0 #сбито кораблей
goal = 50 #столько кораблей нужно сбить для победы
lost = 0 #пропущено кораблей
max_lost = 10 #проиграли, если пропустили столько
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
 #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #вызываем конструктор класса (Sprite):
       sprite.Sprite.__init__(self)

       #каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (90,65))
       self.speed = player_speed
 
       #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #метод, отрисовывающий героя на окне
   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))
 
#класс главного игрока
class Player(GameSprite):
   #метод для управления спрайтом стрелками клавиатуры
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
 #метод "выстрел" (используем место игрока, чтобы создать там пулю)
   def fire(self):
       bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
       bullets.add(bullet)

#класс спрайта-врага  
class Enemy(GameSprite):
   #движение врага
   def update(self):
       self.rect.y += self.speed
       global lost
       #исчезает, если дойдёт до края экрана
       if self.rect.y > win_height:
           self.rect.x = randint(80, win_width - 80)
           self.rect.y = 0
           lost = lost + 1
#класс спрайта-пули  
class Bullet(GameSprite):
   # движение врага
   def update(self):
       self.rect.y += self.speed
       # исчезает, если дойдет до края экрана
       if self.rect.y < 0:
           self.kill()
#создаём окошко
win_width = 700
win_height = 500
display.set_caption("Shooter SAS")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
#создаём спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
#создание группы спрайтов-врагов
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
   monsters.add(monster)
bullets = sprite.Group()
#переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
#основной цикл игры:
run = True #флаг сбрасывается кнопкой закрытия окна
while run:
   #событие нажатия на кнопку Закрыть
   for e in event.get():
       if e.type == QUIT:
           run = False
       #событие нажатия на пробел - спрайт стреляет
       elif e.type == KEYDOWN:
           if e.key == K_SPACE:
               fire_sound.play()
               ship.fire()
 #сама игра: действия спрайтов, проверка правил игры, перерисовка
   if not finish:
       #обновляем фон
       window.blit(background,(0,0))
 
       #производим движения спрайтов
       ship.update()
       monsters.update()
       bullets.update()
 
       #обновляем их в новом местоположении при каждой итерации цикла
       ship.reset()
       monsters.draw(window)
       bullets.draw(window)
       #проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
       collides = sprite.groupcollide(monsters, bullets, True, True)
       for c in collides:
           #этот цикл повторится столько раз, сколько монстров подбито
           score = score + 1
           monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
           monsters.add(monster)
 
       #возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
       if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
           finish = True #проиграли, ставим фон и больше не управляем спрайтами.
           window.blit(lose, (200, 200))
 
       #проверка выигрыша: сколько очков набрали?
       if score >= goal:
           finish = True
           window.blit(win, (200, 200))
 
       #пишем текст на экране
       text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
       window.blit(text, (10, 20))
 
       text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
       window.blit(text_lose, (10, 50))
 
       display.update()
from pygame import *
def TOTAL_UPDATE():
    global fail

    # Игровые моменты
    WIDTH, HEIGHT = 700, 500
    window = display.set_mode((WIDTH, HEIGHT))
    clock = time.Clock()
    FPS = 60
    game = True
    rel_time = False
    num_fire = 0

    #Цвета
    WHITE = (200,255,255)
    GREEN = (65,169,76)
    YELLOW = (255,255,0)
    BLUE = (80,80,255)
    DARK_BLUE = (0,0,100)
    RED = (124,10,2)
    BLACK = (0,0,0)
    LIGHT_RED = (250,128,114)
    LIGHT_GREEN = (10,250,150)

    # Кол-во монстров
    count = 6
    c = 3
    #счет
    number_of_score = 0
    fail = 0
    health = 3

    # Классы объектов
    # Главный класс: GameSprite 
    class GameSprite(sprite.Sprite):
        def __init__(self, player_image, x, y, player_x, player_y, player_speed):
            super().__init__()
            self.image = transform.scale(image.load(player_image), (player_x, player_y))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.speed = player_speed

        def reset(self):
            window.blit(self.image, (self.rect.x, self.rect.y))

    #Надпись
    class Label():
        def __init__(self, x=0, y=0, widht=10, height=10, color=None):
            self.rect = Rect(x, y, widht, height)
            self.fill_color = color
        def set_text(self,text,fsize=12,text_color=(0,0,0)):
            self.image = font.SysFont('verdana',fsize).render(text,True,text_color)

        def draw(self, shift_x=0, shift_y=0):
            window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

    ''' Интерфейс игры'''
    score_text = Label(0,0,20,20,WHITE)
    score_text.set_text('Счет:',20, WHITE)
    
    score = Label(60,0,50,40,WHITE)
    score.set_text('0', 20, WHITE)
    
    miss_text = Label(0,40,20,20,WHITE)
    miss_text.set_text('Пропущенно:',20, WHITE)

    miss_score = Label(145,40,50,40,WHITE)
    miss_score.set_text('0', 20, WHITE)

    health_text = Label(WIDTH - 150,0,20,20,GREEN)
    health_text.set_text('Здоровье:', 20, GREEN)

    health_score = Label(WIDTH-45,0,20,20,GREEN)
    health_score.set_text(str(health), 20, GREEN)

    # Класс игрока
    class Player(GameSprite):
        def update(self):
            keys_pressed = key.get_pressed()
            if keys_pressed[K_RIGHT] and self.rect.x <= 630:
                self.rect.x += self.speed

            if keys_pressed[K_LEFT] and self.rect.x >= 0:
                self.rect.x -= self.speed

    # Класс монстра
    class Enemy(GameSprite):
        def update(self):
            self.rect.y += self.speed
            global fail
            if self.rect.y >= HEIGHT:
                self.rect.y = 30
                self.rect.x = rand_x
                fail += 1
                miss_score.set_text(str(fail), 20, WHITE)

    #класс пули
    class Bullet(GameSprite):
        def update(self):
            self.rect.y -= self.speed
            if self.rect.y == 0:
                bullets.remove(self)

    # Класс астеройда
    class Asteroid(GameSprite):
        def update(self):
            self.rect.y += self.speed
            if self.rect.y >= HEIGHT:
                self.rect.y = 30
                self.rect.x = rand_x

    # Музыка
    mixer.music.load("space.ogg")
    mixer.music.play()

    fire = mixer.Sound("fire.ogg")

    # Игрок
    rocket = Player("rocket.png", WIDTH/2, HEIGHT-75, 65, 65, 10)

    # Группы 
    monsters = sprite.Group()
    bullets = sprite.Group()
    asteroids = sprite.Group()

    #отрисовка всех монстров
    for i in range(count):
        ufo = Enemy("ufo.png", randint(30, WIDTH-30), randint(30, 150), 85, 60, 1)
        monsters.add(ufo)
        count -= 1

    #отрисовка астеройдов
    for i in range(c):
        asteroid = Asteroid("asteroid.png", randint(30, WIDTH-30), randint(30, 150), 60, 60, 2)
        asteroids.add(asteroid)
        c -= 1

    # Задний фон
    back = transform.scale(image.load("galaxy.jpg"), (WIDTH, HEIGHT))

    # Основной игровой цикл
    while game:
        # Рандомные позиции врагов
        rand_x = randint(30, WIDTH-150)

        #обработка событий
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN and e.key == K_SPACE:
                num_fire += 1
                bullet = Bullet("bullet.png", rocket.rect.centerx, rocket.rect.top, 15, 15, 7)
                bullets.add(bullet)
                fire.play()

        # Отрисовка
        window.blit(back, (0, 0))

        rocket.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)

        #передвижение объектов
        rocket.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        score_of_collide = sprite.groupcollide(bullets, monsters, True, True)

        if score_of_collide:
            number_of_score += 1
            score.set_text(str(number_of_score),20,WHITE)

        if fail == 3:
            game = False
            print("YOU LOSE")
            print("Becouse you lose 3 asteroids")

        if number_of_score == 6:
            game = False
            print("YOU WIN")

        fail_sprites_list = sprite.spritecollide(rocket, asteroids, True)

        if fail_sprites_list:
            health -= 1
            health_score.set_text(str(health), 20, GREEN)

        if health == 0:
            game = False
            print("YOU LOSE")
            print("Becouse your health is very low")

        score_text.draw(0,0)
        score.draw(0,0)
        miss_text.draw(0,0)
        miss_score.draw(0,0)
        health_text.draw(0,0)
        health_score.draw(0,0)

        # Обновление экрана
        display.update()
        clock.tick(FPS)
TOTAL_UPDATE()
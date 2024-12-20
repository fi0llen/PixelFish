import pygame
import random
import os
ASSETS_DIR = "assets"

WIGTH = 800
HEIGHT = 650
FPS = 60

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#инициализация pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIGTH, HEIGHT))
pygame.display.set_caption("PixelFish")
clock = pygame.time.Clock()

# Загрузка изображений
player_images = []
fish_images = []
try:
    # Загрузка изображений игроков
    for filename in os.listdir(ASSETS_DIR):
        if filename.startswith("fish") and filename.endswith(".png"):
            img = pygame.image.load(os.path.join(ASSETS_DIR, filename)).convert_alpha()
            img = pygame.transform.scale(img, (120, 80))
            player_images.append(img)
    # Загрузка изображений рыб
    for filename in os.listdir(ASSETS_DIR):
      if filename.startswith("fish") and filename.endswith(".png"):
          img = pygame.image.load(os.path.join(ASSETS_DIR, filename)).convert_alpha()
          img = pygame.transform.scale(img, (120, 80))
          fish_images.append(img)
    #Загрузка изображения жемчуга
    perl_img = pygame.image.load(os.path.join(ASSETS_DIR, "perl.png")).convert_alpha()
    perl_img = pygame.transform.scale(perl_img, (20, 20))
    #Загрузка изображения фона
    bg_img = pygame.image.load(os.path.join(ASSETS_DIR, "PixelFish.png")).convert()
    bg_img = pygame.transform.scale(bg_img, (WIGTH,HEIGHT))
except FileNotFoundError:
    print("Ошибка: Не найдены необходимые изображения в папке 'assets'.")
    pygame.quit()
    exit()

if not player_images or not fish_images:
    print("Ошибка: Не найдены изображения рыбок и игроков")
    pygame.quit()
    exit()


# Класс для рыбки игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = random.choice(player_images) # Выбираем случайное изображение
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.left = 10
        self.rect.bottom = HEIGHT - 10
        self.radius = 25
        self.speedx = 5

    def update(self):
         self.speedx = 0
         self.speedy = 0
         keystate = pygame.key.get_pressed()
         if keystate[pygame.K_LEFT]:
             self.speedx = -8
         if keystate[pygame.K_RIGHT]:
             self.speedx = 8
         self.rect.x += self.speedx
         if self.rect.right > WIGTH:
             self.rect.right = WIGTH
         if self.rect.left < 0:
             self.rect.left = 0
         if keystate[pygame.K_UP]:
             self.speedy = -8
         if keystate[pygame.K_DOWN]:
            self.speedy = 8
         self.rect.y += self.speedy
         if self.rect.bottom > HEIGHT:
             self.rect.bottom = HEIGHT
         if self.rect.top < 0:
             self.rect.top = 0


# Класс для рыбы
class Fish(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = random.choice(fish_images)
        self.rect = self.original_image.get_rect()
        self.rect.y = random.randrange(0, HEIGHT - self.rect.height)

        if random.random() < 0.5:  # 50% шанс появления слева
            self.rect.x = -self.rect.width
            self.speedx = random.randrange(1, 4)
            self.image = self.original_image  # Если слева то не отражаем
        else:
            self.rect.x = WIGTH + self.rect.width  # Начальная позиция справа
            self.speedx = random.randrange(-4, -1)
            self.image = pygame.transform.flip(self.original_image, True, False)  # Зеркально отражаем изображение

        self.radius = 20

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0 or self.rect.left > WIGTH:
            if self.speedx > 0:  # Если рыба идет справа налево
                self.image = self.original_image  # Оригинальное изображение
                self.rect.x = -self.rect.width
            else:
                self.image = pygame.transform.flip(self.original_image, True, False)  # Зеркальное изображение
                self.rect.x = WIGTH + self.rect.width
            self.rect.y = random.randrange(0, HEIGHT - self.rect.height)

# Класс для жемчужины
class Perl(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = perl_img
        self.rect = self.image.get_rect()
        self.rect.x = WIGTH + self.rect.width # Начальная позиция справа
        self.rect.y = random.randrange(0, HEIGHT - self.rect.height)
        self.speedx = random.randrange(-3, -1)
        self.radius = 10

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0:
             self.rect.x = WIGTH + self.rect.width
             self.rect.y = random.randrange(0, HEIGHT - self.rect.height)


# Функция для создания рыбок
def newfish():
    f = Fish()
    all_sprites.add(f)
    fishes.add(f)


# Функция для создания жемчужин
def newperl():
    p = Perl()
    all_sprites.add(p)
    perls.add(p)

# Функция для отображения экрана заставки
def show_go_screen(score):
    screen.blit(bg_img, (0, 0))
    font = pygame.font.Font('PressStart2P.ttf', 25)
    text_surface1 = font.render("PixelFish", True, WHITE)
    text_rect1 = text_surface1.get_rect(center=(WIGTH / 2, HEIGHT / 3))
    text_surface2 = font.render("Съедено: " + str(score), True, WHITE)
    text_rect2 = text_surface2.get_rect(center=(WIGTH / 2, HEIGHT / 2))
    text_surface3 = font.render("Тыкните пробел чтобы начать", True, WHITE)
    text_rect3 = text_surface3.get_rect(center=(WIGTH / 2, HEIGHT * 2 / 3))
    screen.blit(text_surface1, text_rect1)
    screen.blit(text_surface2, text_rect2)
    screen.blit(text_surface3, text_rect3)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False


# Основной игровой цикл
score = 0
game_over = True
running = True
while running:
    if game_over:
        show_go_screen(score)
        game_over = False

        all_sprites = pygame.sprite.Group()
        fishes = pygame.sprite.Group()
        perls = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)

        for i in range(4):
            newfish()

        for i in range(5):
            newperl()

        score = 0

    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # обновление
    all_sprites.update()

    # Проверка поймала ли рыбка жемчужину
    hits = pygame.sprite.spritecollide(player, perls, True, pygame.sprite.collide_circle)
    if hits:
        score += len(hits)
        for hit in hits:
            newperl()

    # Проверка на столкновение с другими рыбами
    hits = pygame.sprite.spritecollide(player, fishes, False, pygame.sprite.collide_circle)
    if hits:
        game_over = True

    # Отрисовка
    screen.fill(BLACK)
    screen.blit(bg_img, (0, 0))
    all_sprites.draw(screen)

    font = pygame.font.Font('PressStart2P.ttf', 30)
    score_text = font.render("Счет: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))
    pygame.display.flip()

    clock.tick(FPS)
pygame.quit()

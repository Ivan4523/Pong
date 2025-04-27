import pygame

pygame.init()

# Класс-родитель для спрайтов 
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс-наследник для игрока (ракетки)
class Player(GameSprite):
    def update_r(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed

    def update_l(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed

# Настройки окна
back = (200, 255, 255)
win_width = 600
win_height = 500
window = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Пинг-Понг")

# Создание объектов
racket1 = Player('racket.png', 10, 200, 4, 50, 150)
racket2 = Player('racket.png', 540, 200, 4, 50, 150)
ball = GameSprite('tenis_ball.png', 200, 200, 4, 50, 50)

# Шрифты и надписи
font = pygame.font.Font(None, 35)
difficult_text = font.render('Выбери сложность от 1 до 9', True, (180, 0, 0))
lose1_text = font.render('PLAYER 1 LOX!', True, (180, 0, 0))
lose2_text = font.render('PLAYER 2 LOX!', True, (180, 0, 0))
restart_text = font.render('Нажмите ПРОБЕЛ для перезапуска', True, (0, 100, 0))

speed_x = 3
speed_y = 3

clock = pygame.time.Clock()

# Счётчики выигрышей
wins_player1 = 0
wins_player2 = 0

# Выбор сложности (FPS)
choose_difficult = True
FPS = 60  # значение по умолчанию

while choose_difficult:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            choose_difficult = False
            game = False
        if event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_9:
                FPS = 50 + (event.key - pygame.K_0) * 10
                choose_difficult = False

    window.fill(back)
    window.blit(difficult_text, (130, 200))
    pygame.display.update()

# Основной игровой цикл
game = True
finish = False

def reset_positions():
    racket1.rect.y = 200
    racket2.rect.y = 200
    ball.rect.x = win_width // 2 - ball.rect.width // 2
    ball.rect.y = win_height // 2 - ball.rect.height // 2

reset_positions()

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if finish and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                finish = False
                reset_positions()
                # Можно сбросить скорость мяча или оставить как есть
                speed_x = 3 if speed_x < 0 else -3  # меняем направление мяча при рестарте
                speed_y = 3

    if not finish:
        window.fill(back)

        # Отображаем счёт
        score_text = font.render(f"{wins_player1}  :  {wins_player2}", True, (0, 0, 0))
        window.blit(score_text, (250, 20))

        racket1.update_l()
        racket2.update_r()

        ball.rect.x += speed_x
        ball.rect.y += speed_y

        # Отражение мяча от ракеток
        if pygame.sprite.collide_rect(racket1, ball) or pygame.sprite.collide_rect(racket2, ball):
            speed_x *= -1

        # Отражение мяча от верхней и нижней границ
        if ball.rect.y <= 0 or ball.rect.y >= win_height - ball.rect.height:
            speed_y *= -1

        # Проверка выигрыша
        if ball.rect.x < 0:
            finish = True
            wins_player2 += 1
            window.blit(lose1_text, (200, 200))
            window.blit(restart_text, (120, 250))
        elif ball.rect.x > win_width:
            finish = True
            wins_player1 += 1
            window.blit(lose2_text, (200, 200))
            window.blit(restart_text, (120, 250))

        racket1.reset(window)
        racket2.reset(window)
        ball.reset(window)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
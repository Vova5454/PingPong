import pygame as pg # Imports module Pygame
import random as rand # Imports module random
import pygame.freetype as pgft # Imports module pygame.freetype


def move_player(): # функция движения игрока
    player.y += player_speed # увеличивает/уменьшает скорость игрока
    if player.top <= 0: # Условие игрока дотрагеватся с верхом 
        player.top = 0
    elif player.bottom >= HEIGHT: # Условие прикосания игрока с полом
        player.bottom = HEIGHT

def move_ball(dx, dy): # Функция движения мяча
    if ball.top <= 0 or ball.bottom >= HEIGHT: # Условие прикосания мяча с потолком или полом
        dy = -dy # меняет переменую dy
    if ball.colliderect(player) and dx < 0: # Условие прикосания меча с игроком
        pong_sound.play()
        if abs(ball.left - player.right) < 10: # Условие прикосания меча с игроком
            dx = -dx # меняет направление мяча по оси x на противоположное
        elif abs(ball.top - player.bottom) < 10 and dy < 0: # Условие мяча ниже игрока
            dy = -dy # меняет направление мяча по оси y на противоположное
        elif abs(player.top - ball.bottom) < 0 and dy > 0: # Условие мяча выше игрока
            dy = -dy # меняет направление мяча по оси y на противоположное
    if ball.colliderect(computer) and dx > 0: # Условие прикосновнее мяча с компютерэм
        pong_sound.play()
        if abs(ball.right - computer.left) < 10: # Условие прикосновения мяча с компютерэм
            dx = -dx # меняет направление мяча по оси x на противоположное
        elif abs(ball.top - computer.bottom) < 10 and dy < 0: # Условие мяча ниже компьютера
            dy = -dy # меняет направление мяча по оси y на противоположное
        elif abs(computer.top - ball.bottom) > 10 and dy > 0: # Условие мяча выше компьютера
            dx = -dx # меняет направление мяча по оси x на противоположное
    now = pg.time.get_ticks() # Создаёт переменую now
    if now - timer > delay_lenght and not game_over:
        ball.x += dx # Добавляет dx к ball.x
        ball.y +=  dy # Добавляет dy к ball.y
    return dx, dy # возращяет dx и 

def move_computer(): # Функция движения компъютера
    if ball.centerx > WIDTH//2 and ball_dx > 0: # Условие меча выше половины высоты
        if computer.top > ball.bottom: # Условие мяча выше компъютера
            computer.y -= comp_speed # Компъютер идёт верх
        if computer.bottom < ball.top: # Условия мяча ниже компъютера
            computer.y += comp_speed # Компъютер идёт вниз
        

def back_to_middle(dx, dy): # Функция которая возращяет мяч в середину экрана
    ball.center = WIDTH//2-13, HEIGHT//2 # телепортиревался в центр 
    dx = rand.choice((rand.randint(-ball_speed, -8), rand.randint(8, ball_speed))) # Выбераёт куда мяч пойдёт по оси x
    dy = rand.choice((rand.randint(-ball_speed, -8), rand.randint(8, ball_speed))) # Выбераёт куда мяч пойдёт по оси y
    return dx, dy # Возращяет dx и dy

def play_sound(): # Зоздает функцию play_sound
    if player_score == target_score: # Условие поражения компъютера
        win_sound.play() # Играет звук выиграша
    elif comp_score == target_score: # Условие поражения игрока
        lose_sound.play() # Играет звук поражения
    else:
        score_sound.play() # Играет звук гола

WIDTH = 900 # Создаёт константа ширины экрана
HEIGHT = 600 # Создаёт константа высоты экрана
BG_COLOR = (96, 168, 168) # Константа для цвета фона
PLATFORM_COLOR = (13, 37, 37) # константа цвета компьютера и игрока
BALL_COLOR = (255, 0, 10) # константа цвета меча

pg.init() # Инициалезирует модули pygame
clock = pg.time.Clock() # Создает объект часов в игре
screen = pg.display.set_mode((WIDTH, HEIGHT)) # Создаёт игровое окно
pg.display.set_caption('PingPong') # Создаёт заголовок окна

player = pg.Rect(10, HEIGHT//2-30, 20, 150) # Создаёт объект игрока
computer = pg.Rect(WIDTH-30, HEIGHT//2-30, 20, 150) # Создаёт объект компъютера
ball = pg.Rect(WIDTH//2-13, HEIGHT//2, 25, 25) # Создаёт объект мячика
font = pgft.Font(None, 42) # Создаёт объект шрифта
font2 = pgft.Font(None, 60) # Создаёт второй объект шрифта
lose_sound = pg.mixer.Sound('lose.wav') # Зоздаёт звук поражения
pong_sound = pg.mixer.Sound('pong.wav') # Зоздаёт звук удара меча с компъютерем или с игроком
score_sound = pg.mixer.Sound('score.wav')# Зоздаёт звук гола
win_sound = pg.mixer.Sound('win.wav')# Зоздаёт звук выиграша

player_speed = 0 # Создаёт переменую скорости
ball_speed = 11 # Создаёт переменую скоорости мяча
comp_speed = 8 # Создаёт переменую скорсти компъютера
player_score = 0 # Создаёт переменую очков игрока
comp_score = 0 # Создаёт переменую очков компъютера
ball_dx, ball_dy,  = -7, 7 # Скорости мяча по оси x и y
target_score = 10 # Создаёт переменую target_score
game_over = False # Создаёт переменую game_over
result_text = None # Создаёт переменую  result_text
restart_text = "Press 'R' to restart" # Cоздаёт переменую restart_text

timer = 0 # Создаёт переменую таймера
delay_lenght = 200 # Создаёт переменую длины промежутки

run = True
while run: # Игровой цикл
    for event in pg.event.get(): # отслеживание сбоытий
        if event.type == pg.QUIT: # Событие нажатия на крестик
            run = False
        if event.type == pg.KEYDOWN: # Событие нажатия кнопки
            if event.key == pg.K_r and game_over: # Условие нажатие на кнопку R и game_over = True
                player_score = 0 # - Обнуляет очки игрока и компьютера
                comp_score = 0 # ---
                game_over = False # Меняет переменую game_over на False
            if event.key == pg.K_w: # Событие нажатия кнопку W
                player_speed -= 12 # Уменьшает скорость на 12
            elif event.key == pg.K_s: # Событие нажатия на кнопку S 
                player_speed += 12 # Пребавляет 12 к скорости
        if event.type == pg.KEYUP: # Событие отжатия кнопки
            if event.key == pg.K_w: # Событие отжатия кнопки W
                player_speed += 12 # прибавление 12 к скорости
            if event.key == pg.K_s: # событие отжатия кнопку S
                player_speed -= 12 # Вычитает 12 из скорости

    move_player() # Вызывает функцию move_player
    move_computer() # Вызывает функцию move_computer
    ball_dx, ball_dy = move_ball(ball_dx, ball_dy) # Меняет переменые ball_dx и ball_dy
    if ball.left >= WIDTH: # Условие вылетанея меча из левой части игрового поля
        player_score += 1 # Добавленее 1 к comp_score
        if player_score == target_score: # Условие поражжения компъютера
            game_over = True # Заканчивает игру
            result_text = 'YOU WON!' # ВЫ ВЫИГРАЛИ
    if ball.right <= 0: # Условие вылетанея меча из правой части игрового поля
        comp_score += 1 # Добавленее 1 к player_score
        if comp_score == target_score: # Условие вашего поражения
            result_text = 'YOU LOST!' # ВЫ ПРОИГРАЛИ
            game_over = True # Заканчивает игру

    if ball.left >= WIDTH or ball.right <= 0: # Условие вылетания меча за игровое поле
        play_sound() # Вызывает функцию play_sound
        ball_dx, ball_dy = back_to_middle(ball_dx, ball_dy) # Меняет переменые ball_dx и ball_dy
        timer = pg.time.get_ticks() # Создаёт таймер
    
    screen.fill(BG_COLOR) # Окрашивает фон игры 
    font.render_to(screen, (10, 20), f'{player_score}') # Отрисовывает очки игрока
    font.render_to(screen, (WIDTH-30, 20), f'{comp_score}') # Отрисовывает очки компъютера
    pg.draw.rect(screen, PLATFORM_COLOR, player) # Рисует прямоугольник/игрока
    pg.draw.rect(screen, PLATFORM_COLOR, computer) # рисует прямоугольник/компъютера
    pg.draw.ellipse(screen, BALL_COLOR, ball) # Рисует мячик
    if game_over:
        font2.render_to(screen, (WIDTH/3.3, HEIGHT//2-70), result_text) # Отрисовывает YOU WON или YOU LOSE зависит если вы выиграли или проиграли
        font2.render_to(screen, (WIDTH/4.5, HEIGHT//2), restart_text) # Отрисовывает Press 'R' to restart

    clock.tick(60) # Подключает FPS
    pg.display.flip() # Команда обновления экрана
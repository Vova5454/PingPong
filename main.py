import pygame as pg 
import random as rand 
import pygame.freetype as pgft 


def move_player(): 
    """Движение игрока в пределах экрана."""
    player.y += player_speed 
    if player.top <= 0: 
        player.top = 0
    elif player.bottom >= HEIGHT:
        player.bottom = HEIGHT

def move_ball(dx, dy):
    """Движение, отскоки и задержка мяча после гола."""
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        dy = -dy
    if ball.colliderect(player) and dx < 0: 
        pong_sound.play()
        if abs(ball.left - player.right) < 10: 
            dx = -dx 
        elif abs(ball.top - player.bottom) < 10 and dy < 0: 
            dy = -dy 
        elif abs(player.top - ball.bottom) < 0 and dy > 0:
            dy = -dy
    if ball.colliderect(computer) and dx > 0:
        pong_sound.play()
        if abs(ball.right - computer.left) < 10: 
            dx = -dx
        elif abs(ball.top - computer.bottom) < 10 and dy < 0:
            dy = -dy
        elif abs(computer.top - ball.bottom) > 10 and dy > 0:
            dx = -dx
    now = pg.time.get_ticks()
    if now - timer > delay_lenght and not game_over:
        ball.x += dx
        ball.y +=  dy
    return dx, dy

def move_computer():
    """Движение кмпъютера в пределах границ экрана."""
    if ball.centerx > WIDTH//2 and ball_dx > 0:
        if computer.top > ball.bottom:
            computer.y -= comp_speed 
        if computer.bottom < ball.top: 
            computer.y += comp_speed 
        

def back_to_middle(dx, dy):
    """Возращение мяча в середину."""
    ball.center = WIDTH//2-13, HEIGHT//2
    dx = rand.choice((rand.randint(-ball_speed, -8), rand.randint(8, ball_speed)))
    dy = rand.choice((rand.randint(-ball_speed, -8), rand.randint(8, ball_speed))) 
    return dx, dy

def play_sound():
    """Проигрывает звуки."""
    if player_score == target_score:
        win_sound.play()
    elif comp_score == target_score:
        lose_sound.play()
    else:
        score_sound.play()

WIDTH = 900 
HEIGHT = 600
BG_COLOR = (96, 168, 168)
PLATFORM_COLOR = (13, 37, 37)
BALL_COLOR = (255, 0, 10)

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('PingPong')

player = pg.Rect(10, HEIGHT//2-30, 20, 150)
computer = pg.Rect(WIDTH-30, HEIGHT//2-30, 20, 150)
ball = pg.Rect(WIDTH//2-13, HEIGHT//2, 25, 25)
font = pgft.Font(None, 42)
font2 = pgft.Font(None, 60)
lose_sound = pg.mixer.Sound('lose.wav')
pong_sound = pg.mixer.Sound('pong.wav')
score_sound = pg.mixer.Sound('score.wav')
win_sound = pg.mixer.Sound('win.wav')

player_speed = 0
ball_speed = 11
comp_speed = 8
player_score = 0
comp_score = 0
ball_dx, ball_dy,  = -7, 7
target_score = 10
game_over = False
result_text = None
restart_text = "Press 'R' to restart"

timer = 0
delay_lenght = 200

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r and game_over:
                player_score = 0 
                comp_score = 0
                game_over = False
            if event.key == pg.K_w:
                player_speed -= 12
            elif event.key == pg.K_s:
                player_speed += 12
        if event.type == pg.KEYUP:
            if event.key == pg.K_w:
                player_speed += 12
            if event.key == pg.K_s:
                player_speed -= 12

    move_player()
    move_computer()
    ball_dx, ball_dy = move_ball(ball_dx, ball_dy)
    if ball.left >= WIDTH:
        player_score += 1
        if player_score == target_score:
            game_over = True
            result_text = 'YOU WON!'
    if ball.right <= 0:
        comp_score += 1
        if comp_score == target_score:
            result_text = 'YOU LOST!'
            game_over = True

    if ball.left >= WIDTH or ball.right <= 0:
        play_sound()
        ball_dx, ball_dy = back_to_middle(ball_dx, ball_dy)
        timer = pg.time.get_ticks()
    
    screen.fill(BG_COLOR) 
    font.render_to(screen, (10, 20), f'{player_score}')
    font.render_to(screen, (WIDTH-30, 20), f'{comp_score}')
    pg.draw.rect(screen, PLATFORM_COLOR, player)
    pg.draw.rect(screen, PLATFORM_COLOR, computer)
    pg.draw.ellipse(screen, BALL_COLOR, ball)
    if game_over:
        font2.render_to(screen, (WIDTH/3.3, HEIGHT//2-70), result_text)
        font2.render_to(screen, (WIDTH/4.5, HEIGHT//2), restart_text) 

    clock.tick(60)
    pg.display.flip()
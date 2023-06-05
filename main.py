import pygame as pg
pg.init()

import ui
import snakelib
from random import randrange, random


WHITE = 220, 220, 220
BLACK = 20, 20, 20
RED = 200, 20, 20

WIN_RESOLUTION = 500, 500
GRID = 25, 25
RECT = WIN_RESOLUTION[0]/GRID[0], WIN_RESOLUTION[1]/GRID[1]
FPS = 60
UPDATE_INTERVAL = 200 # ms
SNAKE_INIT_SIZE = 3


pg.display.set_caption("Snake")
window = pg.display.set_mode(WIN_RESOLUTION)
clock = pg.time.Clock()
square = pg.Rect( (0, 0), RECT )

snake = snakelib.Snake( (12, 12), SNAKE_INIT_SIZE )
apple = [ randrange( 0, GRID[0] ), randrange( 0, GRID[1] ) ]
cake = None
paused = game_over = False


def reset_game(snake: snakelib.Snake):
    snake.segments = [ [10+x, 12] for x in range(SNAKE_INIT_SIZE) ]
    snake.vector = pg.math.Vector2(1, 0)
    snake.alive = True
    snake.score = 0
    
    relocate_apple()
    despawn_cake()


def relocate_apple():
    global snake, apple, cake
    
    while apple in snake or apple == cake:
        apple[0] = randrange( 0, GRID[0] )
        apple[1] = randrange( 0, GRID[1] )


def spawn_cake():
    global snake, apple, cake
    cake = snakelib.Food( [ randrange( 0, GRID[0] ), randrange( 0, GRID[1] ) ], 10, 0 )
    
    while cake in snake or cake == apple:
        cake = snakelib.Food( [ randrange( 0, GRID[0] ), randrange( 0, GRID[1] ) ], 10, 0 )
    
    pg.time.set_timer(snakelib.SPECIAL_TIMER, 1000)


def despawn_cake():
    global cake
    cake = None
    pg.time.set_timer(snakelib.SPECIAL_TIMER, 0)


def constrain_snake(snake: snakelib.Snake, x_axis: list|tuple, y_axis: list|tuple):
    x, w = x_axis
    y, h = y_axis
    snake.head[0] = x if snake.head[0] >= w else w - 1 if snake.head[0] < x else snake.head[0]
    snake.head[1] = y if snake.head[1] >= h else h - 1 if snake.head[1] < y else snake.head[1]


def draw(window: pg.Surface):
    window.fill(BLACK)

    for y in range(25):
        for x in range(25):
            color = WHITE

            if not [x, y] in snake:
                if not [x, y] in [apple, cake]:
                    continue
            
            if [x, y] == cake:
                color = RED

            rect = square.move( x*RECT[0], y*RECT[1] )
            pg.draw.rect(window, color, rect)

    ui.draw_score(window, snake.score)

    if cake:
        ui.draw_countdown(window, cake.points)
    
    if paused:
        ui.draw_text(window, " PAUSED ")
    elif game_over:
        ui.draw_text(window, " GAME OVER ")


def update_window():
    pg.display.flip()
    clock.tick(FPS)


def main():
    global paused, game_over
    pg.time.set_timer(snakelib.UPDATE, UPDATE_INTERVAL)
    relocate_apple()

    apples_eaten = 0
    input_recieved = False
    run = True
    
    while run:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                run = False
            
            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_q and (paused or game_over):
                    run = False

                if game_over:
                    if ev.key == pg.K_RETURN:
                        reset_game(snake)
                        game_over = False
                    break

                if ev.key == pg.K_ESCAPE:
                    paused = not paused
                
                if paused or input_recieved:
                    continue
                
                elif ev.key == pg.K_w:
                    snake.update_vector( (0, -1) )
                elif ev.key == pg.K_a:
                    snake.update_vector( (-1, 0) )
                elif ev.key == pg.K_s:
                    snake.update_vector( (0, 1) )
                elif ev.key == pg.K_d:
                    snake.update_vector( (1, 0) )
                
                input_recieved = True
            
            elif ev.type == snakelib.UPDATE and not paused:
                snake.update()
                constrain_snake( snake, ( 0, GRID[0] ), ( 0, GRID[1] ) )

                if snake.head == apple:
                    snake.eat(apple)
                    apples_eaten += 1
                    relocate_apple()

                    if apples_eaten > 5 and not cake:
                        if random() < (apples_eaten - 5)/10:
                            spawn_cake()
                
                elif snake.head == cake:
                    snake.eat(cake)
                    despawn_cake()
                    apples_eaten = 0

                game_over = not snake.alive
                input_recieved = False
            
            elif ev.type == snakelib.SPECIAL_TIMER and cake and not paused:
                cake.points -= 1

                if cake.points == 0:
                    despawn_cake()
                    apples_eaten = 0
        
        draw(window)
        update_window()


main()
pg.quit()
import pygame as pg


score_font = pg.font.SysFont("consolas", 20)
game_over_font = pg.font.SysFont("consolas", 50, True)
countdown_font = pg.font.SysFont("consolas", 24)


def draw_score(window: pg.Surface, score: int):
    score_render = score_font.render( str(score), True, "white" )
    window.blit( score_render, (0, 0) )


def draw_text(window: pg.Surface, text: str):
    text_render = game_over_font.render(text, True, "white", "black")
    rect = text_render.get_rect( center=(250, 250) )
    window.blit(text_render, rect)


def draw_countdown(window: pg.Surface, time: int):
    time_render = countdown_font.render( str(time), True, "white" )
    rect = time_render.get_rect( center=(250, 30) )
    window.blit(time_render, rect)
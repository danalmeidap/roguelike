import const
from pygame import Rect 

def draw_panel(screen, text="Welcome to the game!"):
    panel_rect = Rect(0, const.HEIGHT - 80, const.WIDTH, 80)
    screen.draw.filled_rect(panel_rect, (30, 30, 30))
    screen.draw.text(text, (10, const.HEIGHT - 70), color="white")

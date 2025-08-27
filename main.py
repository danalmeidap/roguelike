import const
from level import Level
from entity import Player
import ui

level = Level(const.GRID_W, const.GRID_H)
player = Player(const.GRID_W // 2, const.GRID_H // 2)

def draw():
    screen.clear()
    level.draw(screen)
    player.draw(screen)
    ui.draw_message(screen, "Use WASD to move.")

def on_key_down(key):
    if key == keys.W:
        player.move(0, -1, level)
    elif key == keys.S:
        player.move(0, 1, level)
    elif key == keys.A:
        player.move(-1, 0, level)
    elif key == keys.D:
        player.move(1, 0, level)

import const
from level import Level
from entity import Player
import ui

level = Level(const.GRID_W, const.GRID_H)
player = Player(const.GRID_W // 2, const.GRID_H // 2)
log_text = "Pressione WASD para mover (em breve)."

def draw():
    screen.clear()
    level.draw(screen)
    player.draw(screen, const.TILESIZE)
    ui.draw_panel(screen, log_text)

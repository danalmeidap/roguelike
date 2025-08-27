import const
from pygame import Rect 

class Level:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        # mapa de chão simples (1 = chão, 0 = parede)
        self.tiles = [[1 for _ in range(h)] for _ in range(w)]

    def draw(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                rect = Rect(x * const.TILESIZE, y * const.TILESIZE,
                            const.TILESIZE, const.TILESIZE)
                color = const.GRAY if self.tiles[x][y] == 1 else const.BLACK
                screen.draw.filled_rect(rect, color)

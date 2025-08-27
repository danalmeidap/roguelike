import const
from pygame import Rect 


class Level:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.tiles = [[0 for _ in range(h)] for _ in range(w)]

    def draw(self, screen):
        for x in range(self.w):
            for y in range(self.h):
                rect = Rect(x * const.TILESIZE, y * const.TILESIZE,
                            const.TILESIZE, const.TILESIZE)
                color = const.GRAY if self.tiles[x][y] == 1 else const.BLACK
                screen.draw.filled_rect(rect, color)

    def is_walkable(self, x, y):
        """Retorna True se o tile for andável"""
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return False
        return self.tiles[x][y] == 0

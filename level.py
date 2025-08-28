import random
from pygame import Rect
from const import TILESIZE, GRAY, BLACK, GRID_W, GRID_H

class Level:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        # Agora a matriz é h x w (linhas x colunas)
        self.tiles = [[0 for _ in range(w)] for _ in range(h)]

        for y in range(self.h):
            for x in range(self.w):
                if x > 0 and y > 0 and x < self.w - 1 and y < self.h - 1:
                    if random.random() < 0.3:
                        # Corrigido para self.tiles[y][x]
                        self.tiles[y][x] = 1

    def draw(self, screen):
        for y in range(self.h):
            for x in range(self.w):
                # Corrigido para self.tiles[y][x]
                color = GRAY if self.tiles[y][x] == 0 else BLACK
                rect = Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
                screen.draw.filled_rect(rect, color)
    
    def is_walkable(self, x, y):
        # Acesso correto da matriz
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return False
        # Corrigido para self.tiles[y][x]
        return self.tiles[y][x] == 0
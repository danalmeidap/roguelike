class Entity:
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
    
    def draw(self, screen, tilesize):
        screen.draw.text(
            self.char,
            center=(self.x * tilesize + tilesize // 2,
                    self.y * tilesize + tilesize // 2),
            color=self.color,
            fontsize=tilesize
        )

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "@", (255, 215, 0))

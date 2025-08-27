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

class Player:
    def __init__(self, x, y, char="@"):
        self.x = x
        self.y = y
        self.char = char

    def draw(self, screen):
        screen.draw.text(
            self.char,
            (self.x * 32 + 10, self.y * 32 + 10),
            color="yellow"
        )

    def move(self, dx, dy):
        """Atualiza posição do jogador"""
        self.x += dx
        self.y += dy
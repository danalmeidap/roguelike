import const

class Entity:
    def __init__(self, x, y, char):
        self.x = x
        self.y = y
        self.char = char

    def draw(self, screen, color, tilesize):
        screen.draw.text(
            self.char,
            (self.x * tilesize + 10, self.y * tilesize + 10),
            color=color,
            fontsize=tilesize
        )

class Player(Entity):
    def __init__(self, x, y, char="@"):
        super().__init__(x, y, char)
        self.hp = 10 

    def draw(self, screen):
        super().draw(screen, "yellow", const.TILESIZE)

    def move(self, dx, dy, level):
        new_x = self.x + dx
        new_y = self.y + dy

        if level.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, "E")
        self.hp = 3

    def draw(self, screen):
        super().draw(screen, "red", const.TILESIZE)
        
        screen.draw.text(
            str(self.hp),
            (self.x * const.TILESIZE + 40, self.y * const.TILESIZE + 10),
            color="white",
            fontsize=const.TILESIZE
        )
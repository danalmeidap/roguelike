import const
from pgzero.actor import Actor

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

class Player(Actor):
    def __init__(self, x, y):
        super().__init__('player_idle', topleft=(x * const.TILESIZE, y * const.TILESIZE))
        self.x_grid = x
        self.y_grid = y
        self.hp = 10

        self.animation_frames = {
            'idle': ['player_idle'],
            'walk': ['player_walk_0', 'player_walk_1', 'player_walk_2', 'player_walk_3']
        }
        self.current_animation = 'idle'
        self.current_frame_index = 0
        self.animation_speed = 0.15
        self.animation_timer = 0.0
        self.moving = False

    @property
    def x(self):
        return self.x_grid

    @x.setter
    def x(self, value):
        self.x_grid = value
        self.left = self.x_grid * const.TILESIZE

    @property
    def y(self):
        return self.y_grid

    @y.setter
    def y(self, value):
        self.y_grid = value
        self.top = self.y_grid * const.TILESIZE

    def move(self, dx, dy, level):
        new_x = self.x_grid + dx
        new_y = self.y_grid + dy

        if level.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y
            self.moving = True
            return True
        return False
    
    def update_animation(self, dt):
        self.animation_timer += dt

        if self.moving:
            self.current_animation = 'walk'
        else:
            self.current_animation = 'idle'
        
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
        
            self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames[self.current_animation])
            self.image = self.animation_frames[self.current_animation][self.current_frame_index]
            
            if self.current_animation == 'walk' and self.current_frame_index == len(self.animation_frames['walk']) - 1:
                self.moving = False

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

    def move(self, dx, dy, level):
        if level.tiles[self.y + dy][self.x + dx] != '#':
            self.x += dx
            self.y += dy


class Item(Entity):
    def __init__(self, x, y, item_type):
        super().__init__(x, y, "*")
        self.item_type = item_type
        
    def draw(self, screen):
        super().draw(screen, "green", const.TILESIZE)
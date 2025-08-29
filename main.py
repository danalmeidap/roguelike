# main.py

import sys 
import const
import ui
from pygame import Rect
from level import Level
from entity import Player, Enemy
import random


STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_VICTORY = 3


game_state = STATE_MENU 

audio_on = True


level = None
player = None
enemies = []
items = [] 


is_music_playing = False

def draw():
    screen.clear()
    
    if game_state == STATE_MENU:
        ui.draw_menu(screen, audio_on)
    elif game_state == STATE_PLAYING:
        level.draw(screen)
        player.draw(screen)
        
        for enemy in enemies:
            enemy.draw(screen)
        
        for item in items:
            item.draw(screen)
            
        ui.draw_stats(screen, player)
        ui.draw_message(screen, "Use WASD to move.")
        

def update():
    global is_music_playing
    if not is_music_playing:
        music.play('menu.wav')
        is_music_playing = True

def on_key_down(key):
    global game_state, enemies, items

    if game_state == STATE_PLAYING:
        dx, dy = 0, 0
        if key == keys.W:
            dy = -1
        elif key == keys.S:
            dy = 1
        elif key == keys.A:
            dx = -1
        elif key == keys.D:
            dx = 1

        if dx != 0 or dy != 0:
            target_x = player.x + dx
            target_y = player.y + dy

            enemy_to_attack = None
            for enemy in enemies:
                if enemy.x == target_x and enemy.y == target_y:
                    enemy_to_attack = enemy
                    break

            if enemy_to_attack:
                enemy_to_attack.hp -= 1
                if enemy_to_attack.hp <= 0:
                    new_item = Item(enemy_to_attack.x, enemy_to_attack.y, "potion")
                    items.append(new_item)
                    enemies.remove(enemy_to_attack)
                    print("Inimigo derrotado!")

                    if not enemies:
                        game_state = STATE_VICTORY
                        print("Você venceu!")
                
            else:
                player.move(dx, dy, level)
            
            check_for_item_pickup() 
            move_enemies()

            if player.hp <= 0:
                game_state = STATE_GAME_OVER

def on_mouse_down(pos):
    global game_state, level, player, enemies
    
    if game_state == STATE_MENU:
        start_button_rect = Rect(const.WIDTH // 2 - 100, 200, 200, 50)
        exit_button_rect = Rect(const.WIDTH // 2 - 100, 340, 200, 50)

        if start_button_rect.collidepoint(pos):
            start_game()
        
        elif exit_button_rect.collidepoint(pos):
            sys.exit()
    
    elif game_state == STATE_GAME_OVER or game_state == STATE_VICTORY:
        restart_button_rect = Rect(const.WIDTH // 2 - 100, 300, 200, 50)
        exit_button_rect = Rect(const.WIDTH // 2 - 100, 370, 200, 50)

        if restart_button_rect.collidepoint(pos):
            start_game()
        
        elif exit_button_rect.collidepoint(pos):
            sys.exit()


def start_game():
    global game_state, level, player, enemies
    game_state = STATE_PLAYING
    level = Level(const.GRID_W, const.GRID_H)
    player = Player(const.GRID_W // 2, const.GRID_H // 2)
    music.play('tema_fase.wav')

    walkable_tiles = []
    for x in range(level.w):
        for y in range(level.h):
            if level.is_walkable(x, y):
                walkable_tiles.append((x, y))

    enemies = []
    for _ in range(5):
        pos = random.choice(walkable_tiles)
        new_enemy = Enemy(pos[0], pos[1])
        enemies.append(new_enemy)

def move_enemies():
    for enemy in enemies:
        dx = player.x - enemy.x
        dy = player.y - enemy.y
        
       
        if abs(dx) > abs(dy):
            new_x = enemy.x + (1 if dx > 0 else -1)
            new_y = enemy.y
        else:
            new_x = enemy.x
            new_y = enemy.y + (1 if dy > 0 else -1)

  
        if new_x == player.x and new_y == player.y:
            player.hp -= 1  
            print(f"Você foi atacado! Seu HP atual: {player.hp}")
        else:
            enemy.move(new_x - enemy.x, new_y - enemy.y, level)


def check_for_item_pickup():
    global player, items
    item_to_remove = None
    for item in items:
        if player.x == item.x and player.y == item.y:
            item_to_remove = item
            if item.item_type == "potion":
                player.hp += 2
                print(f"Você coletou uma poção! Seu HP agora é: {player.hp}")
            break
            
    if item_to_remove:
        items.remove(item_to_remove)


def check_for_collisions():
    global game_state
    for enemy in enemies:
        if player.x == enemy.x and player.y == enemy.y:
            game_state = STATE_GAME_OVER
            print("Game Over!")
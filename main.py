# -*- coding: utf-8 -*-

import sys 
import const
import ui
from pygame import Rect
from level import Level
from entity import Player, Enemy,Item
import random


STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_VICTORY = 3
ENEMY_MOVE_RATE = 3
enemy_move_counter = 0

game_state = STATE_MENU

audio_on = True
menu_selection = 0 

level = None
player = None
enemies = []
items = []

is_menu_music_playing = False
is_game_music_playing = False


def draw():
    global game_state, player, enemies, items, audio_on, menu_selection

    screen.clear()
    
    if game_state == STATE_MENU:
        # Lógica de desenho do menu
        screen.draw.text("Roguelike", center=(const.WIDTH / 2, const.HEIGHT / 2 - 50), fontsize=60, color="white")
        
        menu_items = ["Começar", "Música: On" if audio_on else "Música: Off", "Sair"]
        for i, item in enumerate(menu_items):
            text_pos = (const.WIDTH / 2, const.HEIGHT / 2 + i * 40)
            
            # Se a opção estiver selecionada, desenha o retângulo de destaque
            if i == menu_selection:
                # O get_rect() deve ser chamado em um objeto criado a partir do texto
                # Criamos um retângulo manualmente para evitar o erro
                width, height = 300, 50
                highlight_rect = Rect((text_pos[0] - width / 2, text_pos[1] - height / 2), (width, height))
                screen.draw.filled_rect(highlight_rect, (255, 255, 0)) # Amarelo preenchido
            
            # Desenha o texto do menu
            # Muda a cor para preto se estiver sobre o retângulo amarelo, para dar destaque
            color = "black" if i == menu_selection else "white"
            screen.draw.text(item, center=text_pos, fontsize=40, color=color)

    elif game_state == STATE_PLAYING:
        # Desenha o mapa do jogo
        level.draw(screen)

        # Desenha todos os itens no chão
        for item in items:
            item.draw()

        # Desenha todos os inimigos
        for enemy in enemies:
            enemy.draw()

        # Desenha o jogador por último
        player.draw()

        # Desenha o HUD (HP do jogador)
        screen.draw.text(f"HP: {player.hp}", topleft=(10, 10), fontsize=30, color="red")
    
    elif game_state == STATE_GAME_OVER:
        # Lógica da tela de Game Over
        screen.clear()
        screen.draw.text("Game Over!", center=(const.WIDTH / 2, const.HEIGHT / 2), fontsize=60, color="red")
        screen.draw.text("Pressione 'R' para reiniciar", center=(const.WIDTH / 2, const.HEIGHT / 2 + 50), fontsize=30, color="white")
    
    elif game_state == STATE_VICTORY:
        # Lógica da tela de Vitória
        screen.clear()
        screen.draw.text("Você Venceu!", center=(const.WIDTH / 2, const.HEIGHT / 2), fontsize=60, color="green")
        screen.draw.text("Pressione 'R' para jogar novamente", center=(const.WIDTH / 2, const.HEIGHT / 2 + 50), fontsize=30, color="white")


def update(dt):
    global game_state, player, enemies, audio_on, is_menu_music_playing, is_game_music_playing

    if game_state == STATE_MENU:
        if audio_on and not is_menu_music_playing:
            music.play('menu.wav')
            is_menu_music_playing = True
    
    elif game_state == STATE_PLAYING:
        if is_menu_music_playing:
            music.stop()
            is_menu_music_playing = False

        if audio_on and not is_game_music_playing:
            music.play('tema_fase.wav')
            is_game_music_playing = True
            
        for enemy in enemies:
            enemy.update_animation(dt)
            


def on_key_down(key):
    global game_state, enemies, items, audio_on, menu_selection, player, enemy_move_counter

    if key == keys.R:
        start_game()
        return

    if game_state == STATE_MENU:
        
        if key == keys.W:
            if audio_on:
                sounds.navigation.play()
            menu_selection -= 1
        elif key == keys.S:
            if audio_on:
                sounds.navigation.play()
            menu_selection += 1
        
        if menu_selection < 0:
            menu_selection = 2
        elif menu_selection > 2:
            menu_selection = 0
            
        if key == keys.RETURN:
            if audio_on:
                sounds.menu_confirm.play()
            
            if menu_selection == 0:
                start_game()
            elif menu_selection == 1:
                audio_on = not audio_on
                if audio_on:
                    music.unpause()
                else:
                    music.pause()
            elif menu_selection == 2:
                quit()

    elif game_state == STATE_PLAYING:
        dx, dy = 0, 0
        
        if key == keys.W or key == keys.UP:
            dy = -1
        elif key == keys.S or key == keys.DOWN:
            dy = 1
        elif key == keys.A or key == keys.LEFT:
            dx = -1
        elif key == keys.D or key == keys.RIGHT:
            dx = 1

        # Lógica de coleta de item com a tecla G
        if key == keys.G:
            check_for_item_pickup()
            
            move_enemies()

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
                    new_item = Item(enemy_to_attack.x, enemy_to_attack.y, 'potion')
                    items.append(new_item)
                    enemies.remove(enemy_to_attack)
                    print("Inimigo derrotado!")

                    if not enemies:
                        game_state = STATE_VICTORY
                        print("Você venceu!")
            else:
                player.moving = True
                player.move(dx, dy, level)
            
            enemy_move_counter += 1
            if enemy_move_counter >= ENEMY_MOVE_RATE:
                move_enemies()
                enemy_move_counter = 0

        
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
    global game_state, level, player, enemies, items, enemy_move_counter, is_menu_music_playing, is_game_music_playing
    
   
    game_state = STATE_PLAYING
    
   
    level = Level(const.GRID_W, const.GRID_H)
    player = Player(const.GRID_W // 2, const.GRID_H // 2)
    enemies = []
    items = [] #r
    
   
    walkable_tiles = []
    for x in range(level.w):
        for y in range(level.h):
            if level.is_walkable(x, y):
                walkable_tiles.append((x, y))

    for _ in range(5):
        pos = random.choice(walkable_tiles)
        new_enemy = Enemy(pos[0], pos[1])
        enemies.append(new_enemy)

  
    is_menu_music_playing = False
    is_game_music_playing = False
    
 
    music.stop()


    enemy_move_counter = 0

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
        if player.x == item.x_grid and player.y == item.y_grid:
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
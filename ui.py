# ui.py

import const
from pygame import Rect

def draw_menu(screen, audio_on):
    screen.clear()
    screen.draw.text("Roguelike", midtop=(const.WIDTH // 2, 100), fontsize=60, color="white")

    start_button_rect = Rect(const.WIDTH // 2 - 100, 200, 200, 50)
    sound_button_rect = Rect(const.WIDTH / 2 - 100, 270, 200, 50)
    exit_button_rect = Rect(const.WIDTH / 2 - 100, 340, 200, 50)

    
    screen.draw.filled_rect(start_button_rect, (100, 100, 100))
    screen.draw.filled_rect(sound_button_rect, (100, 100, 100))
    screen.draw.filled_rect(exit_button_rect, (100, 100, 100))

    
    screen.draw.text("Start Game", center=(start_button_rect.centerx, start_button_rect.centery), color="white")
    screen.draw.text("Music/Sound: " + ("ON" if audio_on else "OFF"), center=(sound_button_rect.centerx, sound_button_rect.centery), color="white")
    screen.draw.text("Exit", center=(exit_button_rect.centerx, exit_button_rect.centery), color="white")


def draw_panel(screen, text="Welcome to the game!"):
    panel_rect = Rect(0, const.HEIGHT - 80, const.WIDTH, 80)
    screen.draw.filled_rect(panel_rect, (30, 30, 30))
    screen.draw.text(text, (10, const.HEIGHT - 70), color="white")


def draw_message(screen, message):
    screen.draw.filled_rect(
        Rect((0, 480), (640, 120)), "black"
    )
    screen.draw.text(
        message,
        (10, 490),
        color="white",
    )


def draw_stats(screen, player):
     screen.draw.text(f"HP: {player.hp}", (10, 10), color="white", fontsize=30)


def draw_game_over(screen):
    screen.clear()
    screen.draw.text("Game Over", center=(const.WIDTH // 2, 200), fontsize=60, color="red")
    
    restart_button_rect = Rect(const.WIDTH // 2 - 100, 300, 200, 50)
    exit_button_rect = Rect(const.WIDTH // 2 - 100, 370, 200, 50)
    
    screen.draw.filled_rect(restart_button_rect, (100, 100, 100))
    screen.draw.filled_rect(exit_button_rect, (100, 100, 100))
    
    screen.draw.text("Restart", center=(restart_button_rect.centerx, restart_button_rect.centery), color="white")
    screen.draw.text("Exit", center=(exit_button_rect.centerx, exit_button_rect.centery), color="white")

def draw_victory(screen):
    screen.clear()
    screen.draw.text("You Win!", center=(const.WIDTH // 2, 200), fontsize=60, color="green")

    restart_button_rect = Rect(const.WIDTH // 2 - 100, 300, 200, 50)
    exit_button_rect = Rect(const.WIDTH // 2 - 100, 370, 200, 50)
    
    screen.draw.filled_rect(restart_button_rect, (100, 100, 100))
    screen.draw.filled_rect(exit_button_rect, (100, 100, 100))
    
    screen.draw.text("Restart", center=(restart_button_rect.centerx, restart_button_rect.centery), color="white")
    screen.draw.text("Exit", center=(exit_button_rect.centerx, exit_button_rect.centery), color="white")
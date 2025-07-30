import pygame  
from src.core import GameManager  
from src.main import main 
from src.ui.game_modes import GameModes
from src.data.save_manager import SaveManager
import sys
import ctypes

pygame.init()

save_manager = SaveManager()
load_game = save_manager.load_game()
game_modes = GameModes() # Create an instance of GameModes here
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# Create a resizable window the size of the screen
screen = pygame.display.set_mode((screen_width, screen_height - 10), pygame.RESIZABLE)
ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], 3)
pygame.display.set_caption("AI Chess Game")

font = pygame.font.SysFont(None, 36)

WHITE = (255, 255, 255)
BLUE = (70, 130, 180)
DARK_BLUE = (40, 100, 160)

def New_Game(FEN, local):
    main(FEN, local)

def run_main():
    global screen
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # Pass the 'main' function as an argument
                    game_modes.GameModes_windows(main)

                if button_rect3.collidepoint(event.pos):
                    running = False

                if button_rect2.collidepoint(event.pos):
                    FEN_ = load_game["FEN"]
                    local = False
                    New_Game(FEN_, local)

                if button_rect4.collidepoint(event.pos):
                    run_settings()


        screen_width = screen.get_width()
        screen_height = screen.get_height()

        button_width = 140 # New_Game
        button_height = 70

        button_width2 = 140 # Load_Game
        button_height2 = 70

        button_width3 = 120 # Exit
        button_height3 = 70

        button_width4 = 170 # Settings
        button_height4 = 70


        button_x = (screen_width - button_width) // 10
        button_y = (screen_height - button_height) // 8

        button_rect = pygame.Rect(button_x, button_y, button_width, button_height) # New_Game
        button_rect2 = pygame.Rect(button_x , button_y  + 150, button_width2, button_height2) # Load_Game
        button_rect3 = pygame.Rect(button_x  , button_y + 300, button_width3, button_height3)  # Exit
        button_rect4 = pygame.Rect(button_x  + 270, button_y, button_width4 - 20, button_height4)  # Settings

        # Draw everything
        screen.fill(WHITE)

        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            color = DARK_BLUE
        else:
            color = BLUE

        if button_rect2.collidepoint(mouse_pos):
            color2 = DARK_BLUE
        else:
            color2 = BLUE

        if button_rect3.collidepoint(mouse_pos):
            color3 = DARK_BLUE
        else:
            color3 = BLUE

        if button_rect4.collidepoint(mouse_pos):
            color4 = DARK_BLUE
        else:
            color4 = BLUE


        pygame.draw.rect(screen, color, button_rect, border_radius=12)
        pygame.draw.rect(screen, color2, button_rect2, border_radius=12)
        pygame.draw.rect(screen, color3, button_rect3, border_radius=12)
        pygame.draw.rect(screen, color4, button_rect4, border_radius=12)


        # New_Game
        text_surface = font.render("New Game", True, WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

        # Load_Game
        text_surface2 = font.render("Load Game", True, WHITE)
        text_rect2 = text_surface2.get_rect(center=button_rect2.center)
        screen.blit(text_surface2, text_rect2)

        # Exit
        text_surface3 = font.render("Exit", True, WHITE)
        text_rect3 = text_surface3.get_rect(center=button_rect3.center)
        screen.blit(text_surface3, text_rect3)

        # GameModes
        text_surface4 = font.render("Settings", True, WHITE)
        text_rect4 = text_surface4.get_rect(center=button_rect4.center)
        screen.blit(text_surface4, text_rect4)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

def run_settings():
    global screen
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button1_rect.collidepoint(event.pos):
                    pass

                if button2_rect.collidepoint(event.pos):
                    pass

                if button3_rect.collidepoint(event.pos):
                    run_main()


        button_width = 180
        button_height = 60
        spacing = 30
        left_margin = 40
        top_margin = 100

        # Individual button rects
        button1_rect = pygame.Rect(left_margin, top_margin, button_width, button_height)
        button2_rect = pygame.Rect(left_margin, top_margin + button_height + spacing, button_width, button_height)
        button3_rect = pygame.Rect(left_margin, top_margin + 2 * (button_height + spacing), button_width, button_height)

        # Detect mouse hover
        mouse_pos = pygame.mouse.get_pos()
        color1 = DARK_BLUE if button1_rect.collidepoint(mouse_pos) else BLUE
        color2 = DARK_BLUE if button2_rect.collidepoint(mouse_pos) else BLUE
        color3 = DARK_BLUE if button3_rect.collidepoint(mouse_pos) else BLUE

        # Draw background
        screen.fill(WHITE)

        # Draw buttons
        pygame.draw.rect(screen, color1, button1_rect, border_radius=10)
        pygame.draw.rect(screen, color2, button2_rect, border_radius=10)
        pygame.draw.rect(screen, color3, button3_rect, border_radius=10)

        # Button text
        text1 = font.render("Sounds", True, WHITE)
        text2 = font.render("Graphics", True, WHITE)
        text3 = font.render("Back To Menu", True, WHITE)

        screen.blit(text1, text1.get_rect(center=button1_rect.center))
        screen.blit(text2, text2.get_rect(center=button2_rect.center))
        screen.blit(text3, text3.get_rect(center=button3_rect.center))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    run_main()
# src/main.py

import pygame
import sys
from ui.board_renderer import BoardRenderer  # Imports the board rendering module
from ui.asset_manager import AssetManager  # Imports the asset management module
from ui.audio_manager import AudioManager  # Imports the audio management module

# Set global constants for the game
SCREEN_WIDTH = 800 
SCREEN_HEIGHT = 800
BOARD_SIZE = 8      
SQUARE_SIZE = SCREEN_WIDTH // BOARD_SIZE  

def main():
    pygame.init()  # Initializes Pygame
    pygame.mixer.init()  # Initializes the audio mixer

    # Creates the main game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI Chess Game")

    # Clock to control the FPS
    clock = pygame.time.Clock()

    audio_manager = AudioManager()  # ⬅️ instancia o AudioManager
    asset_manager = AssetManager(square_size=SQUARE_SIZE)  # ⬅️ instancia o AssetManager
    board_renderer = BoardRenderer(screen, SQUARE_SIZE, asset_manager, audio_manager)  # ⬅️ passa ele para o renderizador

    running = True
    while running:
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board_renderer.start_drag(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                board_renderer.end_drag(event.pos)

            elif event.type == pygame.MOUSEMOTION:
                board_renderer.update_mouse_pos(event.pos)

        # Draw the chessboard
        board_renderer.draw_board()

        # Update the display
        pygame.display.flip()

        # Set the frame rate
        clock.tick(60)

    # Finalize Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
# src/main.py

import pygame
import sys
from src.ui.board_renderer import BoardRenderer  # Imports the board rendering module
from src.ui.asset_manager import AssetManager  # Imports the asset management module
from src.ui.audio_manager import AudioManager  # Imports the audio management module
from src.ia.easy_ai import EasyAI  # Imports the AI module

# Set global constants for the game
SCREEN_WIDTH = 600 
SCREEN_HEIGHT = 600
BOARD_SIZE = 8      
SQUARE_SIZE = SCREEN_WIDTH // BOARD_SIZE  

def main():
    pygame.init()  # Initializes Pygame
    pygame.mixer.init()  # Initializes the audio mixer

    # Create the main game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI Chess Game")

    # Clock to control the FPS
    clock = pygame.time.Clock()

    audio_manager = AudioManager()  # Instantiates the AudioManager
    asset_manager = AssetManager(square_size=SQUARE_SIZE)  # Instantiates the AssetManager
    board_renderer = BoardRenderer(screen, SQUARE_SIZE, asset_manager, audio_manager)  # Passes it to the renderer

    running = True
    while running:
        screen.fill((30, 30, 30))
        if board_renderer.turn:
            # If it's the AI's turn, get the best move and apply it
            ai = EasyAI(depth=2)
            best_move = ai.get_best_move(board_renderer.chess_game.board)
            if best_move:
                move_uci = best_move.uci()  # e.g., "e2e4"
                board_renderer.from_chess_square(move_uci)  # parse the move
                piece = board_renderer.test_board[board_renderer.row_ai][board_renderer.col_ai]
                if piece:
                    ai_piece = piece
                    board_renderer.test_board[board_renderer.row_ai][board_renderer.col_ai] = None  # temporarily remove the piece from the board

                board_renderer.test_board[board_renderer.new_row_ai][board_renderer.new_col_ai] = ai_piece

                board_renderer.chess_game.make_move(move_uci)
                board_renderer.turn = False

            else:
                board_renderer.test_board[board_renderer.row][board_renderer.col] = board_renderer.dragging_piece
        

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
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
            # Mostra a mensagem 'Turno das Pretas' antes da IA jogar | Show 'Black's Turn' before AI moves
            board_renderer.draw_board()
            pygame.display.flip()  # Atualiza a tela imediatamente
            pygame.time.delay(1500)  # Aguarda 1.5 segundos | Wait 1.5 seconds

            # Após delay, IA faz o movimento | After delay, AI plays
            ai = EasyAI(depth=2)
            best_move = ai.get_best_move(board_renderer.chess_game.board)
            if best_move:
                move_uci = best_move.uci()  # e.g., "e2e4"
                board_renderer.from_chess_square(move_uci)
                piece = board_renderer.test_board[board_renderer.row_ai][board_renderer.col_ai]

                if piece:
                    ai_piece = piece
                    board_renderer.test_board[board_renderer.row_ai][board_renderer.col_ai] = None

                captured_piece = board_renderer.test_board[board_renderer.new_row_ai][board_renderer.new_col_ai]
                board_renderer.test_board[board_renderer.new_row_ai][board_renderer.new_col_ai] = ai_piece
                board_renderer.chess_game.make_move(move_uci)
                board_renderer.turn = False
                board_renderer.last_move = move_uci  # Registra último movimento da IA | Records AI's last move
                
                if board_renderer.audio_manager:
                    if captured_piece:
                        board_renderer.audio_manager.play("capture")
                    else:
                        board_renderer.audio_manager.play("move")
                    if board_renderer.chess_game.is_checkmate():
                        board_renderer.audio_manager.play("checkmate")
            else:
                board_renderer.test_board[board_renderer.row][board_renderer.col] = board_renderer.dragging_piece

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board_renderer.handle_click(event.pos)  # <--- show moves on click
                board_renderer.start_drag(event.pos)    # <--- começa o arraste se quiser mover 

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
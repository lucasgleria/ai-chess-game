import pygame
import sys
import chess
import json
import os
import ctypes
from src.ui.board_renderer import BoardRenderer
from src.ui.asset_manager import AssetManager
from src.ui.audio_manager import AudioManager
from src.ia.easy_ai import EasyAI
from src.ia.medium_ai import MediumAI
from src.ia.stockfish_ai import StockfishAI
from src.data.Save_Manager import SaveManager
from src.utils import load_config, save_config
BOARD_SIZE = 8
MENU_HEIGHT = 80
SQUARE_SIZE = 75
BOARD_WIDTH = SQUARE_SIZE * BOARD_SIZE
BOARD_HEIGHT = BOARD_WIDTH + MENU_HEIGHT

TIME_CONTROLS = {
    'classic': 90 * 60,
    'rapid': 15 * 60,
    'blitz': 5 * 60,
    'bullet': 1 * 60
}



def main(FEN, local, selected_ai_type=None, time_control=None, white_time_left=None, black_time_left=None, loaded_save_name=None):
    pygame.init()
    pygame.mixer.init()

    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h

    screen = pygame.display.set_mode((screen_w, screen_h - 10), pygame.RESIZABLE)
    ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], 3)
    pygame.display.set_caption("AI Chess Game")

    font = pygame.font.SysFont(None, 24)
    large_font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()

    audio_manager = AudioManager()
    asset_manager = AssetManager(square_size=SQUARE_SIZE)
    save_manager = SaveManager()

    # IMPORTED HERE: Ensures ChessGame is defined when main is executed
    from src.core.chess_game import ChessGame
    chess_game = ChessGame(FEN)
    board_renderer = BoardRenderer(screen, SQUARE_SIZE, chess_game, local, asset_manager, audio_manager)

    config = load_config()
    current_ai_type = selected_ai_type if selected_ai_type else config["selected_ai"]
    skill_level = config["skill_level"]
    thinking_time = config["thinking_time"]

    ai = None
    ai_thinking = False

    game_over_state = False
    game_result_text = ""

    player_white_time = white_time_left if white_time_left is not None else (TIME_CONTROLS.get(time_control, 0) if local else 0)
    player_black_time = black_time_left if black_time_left is not None else (TIME_CONTROLS.get(time_control, 0) if local else 0)
    last_tick_time = pygame.time.get_ticks()

    save_message_text = ""
    save_message_display_time = 0

    def update_ai():
        nonlocal ai
        if current_ai_type == "easy":
            ai = EasyAI(depth=1)
        elif current_ai_type == "medium":
            ai = MediumAI(depth=2)
        elif current_ai_type == "stockfish":
            ai = StockfishAI(skill_level=skill_level, thinking_time=thinking_time)

    def on_ai_move(best_move):
        nonlocal ai_thinking, game_over_state, game_result_text
        if best_move:
            move_uci = best_move.uci()
            board_renderer.chess_game.make_move(move_uci)
            board_renderer.last_move = move_uci

            board_renderer.load_pieces()

            if board_renderer.audio_manager:
                board_renderer.audio_manager.play("move")

            if chess_game.is_game_over():
                game_over_state = True
                outcome = chess_game.outcome()
                
                # Determine specific game end type for better theming
                if chess_game.is_checkmate():
                    if outcome and outcome.winner == chess.WHITE:
                        game_result_text = "White Wins by Checkmate!"
                    elif outcome and outcome.winner == chess.BLACK:
                        game_result_text = "Black Wins by Checkmate!"
                    else:
                        game_result_text = "Checkmate!"
                elif chess_game.is_stalemate():
                    game_result_text = "Stalemate!"
                elif chess_game.board.is_insufficient_material():
                    game_result_text = "Draw by Insufficient Material!"
                elif chess_game.board.is_fifty_moves():
                    game_result_text = "Draw by Fifty-Move Rule!"
                elif chess_game.board.is_repetition():
                    game_result_text = "Draw by Repetition!"
                elif outcome:
                    if outcome.winner == chess.WHITE:
                        game_result_text = "White Wins!"
                    elif outcome.winner == chess.BLACK:
                        game_result_text = "Black Wins!"
                    else:
                        game_result_text = "Draw!"
                else:
                    game_result_text = "Game Over!"
                    
                if board_renderer.audio_manager:
                    board_renderer.audio_manager.play("checkmate")

        ai_thinking = False

    def draw_button(rect, text, selected=False):
        pygame.draw.rect(screen, (100, 100, 100) if selected else (60, 60, 60), rect)
        label = font.render(text, True, (255, 255, 255))
        screen.blit(label, (rect.x + 10, rect.y + 8))

    def draw_slider(x, y, label_text, value, min_val, max_val, step, width=150):
        pygame.draw.rect(screen, (90, 90, 90), (x, y + 25, width, 6))
        knob_x = x + int((value - min_val) / (max_val - min_val) * width)
        pygame.draw.circle(screen, (200, 200, 200), (knob_x, y + 28), 8)
        label = font.render(f"{label_text}: {value}", True, (255, 255, 255))
        screen.blit(label, (x, y))
        return pygame.Rect(x, y + 25, width, 16)

    def draw_end_game_screen(result_text):
        # Chess-themed colors
        CHESS_BROWN = (139, 69, 19)  # Dark brown for chess board
        CHESS_CREAM = (245, 245, 220)  # Light cream for chess board
        CHESS_GOLD = (255, 215, 0)  # Gold for highlights
        CHESS_SILVER = (192, 192, 192)  # Silver for secondary elements
        CHESS_DARK = (47, 79, 79)  # Dark slate gray
        CHESS_LIGHT = (240, 248, 255)  # Alice blue
        
        # Determine game end type for specific theming
        is_checkmate = "Checkmate" in result_text
        is_draw = "Draw" in result_text and "Checkmate" not in result_text
        is_stalemate = "Stalemate" in result_text
        is_insufficient_material = "Insufficient Material" in result_text
        is_fifty_moves = "Fifty-Move Rule" in result_text
        is_repetition = "Repetition" in result_text
        is_time_up = "Time is Up" in result_text
        
        # Create overlay with enhanced chess-themed background
        overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Slightly more transparent for better visibility
        screen.blit(overlay, (0, 0))
        
        # Draw enhanced chess board pattern background with better spacing
        pattern_size = 50  # Increased for better visual appeal
        for y in range(0, screen_h, pattern_size):
            for x in range(0, screen_w, pattern_size):
                color = CHESS_BROWN if (x + y) // pattern_size % 2 == 0 else CHESS_CREAM
                pygame.draw.rect(screen, color, (x, y, pattern_size, pattern_size))
        
        # Main dialog box with enhanced chess theme
        box_width = 550  # Increased width for better proportions
        box_height = 450  # Increased height for better spacing
        box_x = (screen_w - box_width) // 2
        box_y = (screen_h - box_height) // 2
        
        # Draw main box with enhanced chess board border
        pygame.draw.rect(screen, CHESS_DARK, (box_x, box_y, box_width, box_height), border_radius=25)
        pygame.draw.rect(screen, CHESS_GOLD, (box_x, box_y, box_width, box_height), 5, border_radius=25)
        
        # Draw inner border with alternating colors like chess board
        inner_margin = 10  # Increased margin
        inner_rect = pygame.Rect(box_x + inner_margin, box_y + inner_margin, 
                                box_width - 2*inner_margin, box_height - 2*inner_margin)
        pygame.draw.rect(screen, CHESS_LIGHT, inner_rect, border_radius=20)
        
        # Title with enhanced chess-themed styling
        title_font = pygame.font.SysFont(None, 72, bold=True)  # Increased font size
        if is_checkmate:
            title_text = "CHECKMATE"
            title_color = CHESS_GOLD
        elif is_stalemate:
            title_text = "STALEMATE"
            title_color = CHESS_SILVER
        elif is_insufficient_material:
            title_text = "INSUFFICIENT MATERIAL"
            title_color = CHESS_SILVER
        elif is_fifty_moves:
            title_text = "FIFTY-MOVE RULE"
            title_color = CHESS_SILVER
        elif is_repetition:
            title_text = "REPETITION DRAW"
            title_color = CHESS_SILVER
        elif is_draw:
            title_text = "DRAW"
            title_color = CHESS_SILVER
        elif is_time_up:
            title_text = "TIME'S UP"
            title_color = CHESS_GOLD
        else:
            title_text = "Game Over"
            title_color = CHESS_DARK
            
        title_surface = title_font.render(title_text, True, title_color)
        title_rect = title_surface.get_rect(center=(screen_w // 2, box_y + 70))  # Better positioned
        screen.blit(title_surface, title_rect)
        
        # Result message with enhanced styling
        result_font = pygame.font.SysFont(None, 38)  # Slightly larger font
        if is_checkmate:
            if "White" in result_text:
                result_display = "White King Wins!"
            else:
                result_display = "Black King Wins!"
        elif is_stalemate:
            result_display = "Game Ended in Stalemate"
        elif is_insufficient_material:
            result_display = "Draw by Insufficient Material"
        elif is_fifty_moves:
            result_display = "Draw by Fifty-Move Rule"
        elif is_repetition:
            result_display = "Draw by Repetition"
        elif is_draw:
            result_display = "Game Ended in Draw"
        elif is_time_up:
            if "White" in result_text:
                result_display = "White's Time is Up! Black Wins!"
            else:
                result_display = "Black's Time is Up! White Wins!"
        else:
            result_display = result_text
            
        result_surface = result_font.render(result_display, True, CHESS_DARK)
        result_rect = result_surface.get_rect(center=(screen_w // 2, box_y + 140))  # Better positioned
        screen.blit(result_surface, result_rect)
        
        # Chess-themed decorative elements with enhanced positioning
        if is_checkmate:
            # Draw crown symbols with enhanced positioning
            crown_font = pygame.font.SysFont(None, 56)  # Larger font
            crown_left = crown_font.render("KING", True, CHESS_GOLD)
            crown_right = crown_font.render("KING", True, CHESS_GOLD)
            screen.blit(crown_left, (box_x + 50, box_y + 70))  # Better positioned
            screen.blit(crown_right, (box_x + box_width - 80, box_y + 70))  # Better positioned
        elif is_stalemate:
            # Draw bishop symbols for stalemate with enhanced positioning
            piece_font = pygame.font.SysFont(None, 56)  # Larger font
            piece_left = piece_font.render("BISHOP", True, CHESS_SILVER)
            piece_right = piece_font.render("BISHOP", True, CHESS_SILVER)
            screen.blit(piece_left, (box_x + 50, box_y + 70))  # Better positioned
            screen.blit(piece_right, (box_x + box_width - 80, box_y + 70))  # Better positioned
        elif is_draw or is_insufficient_material or is_fifty_moves or is_repetition:
            # Draw rook symbols for draws with enhanced positioning
            piece_font = pygame.font.SysFont(None, 56)  # Larger font
            piece_left = piece_font.render("ROOK", True, CHESS_SILVER)
            piece_right = piece_font.render("ROOK", True, CHESS_SILVER)
            screen.blit(piece_left, (box_x + 50, box_y + 70))  # Better positioned
            screen.blit(piece_right, (box_x + box_width - 80, box_y + 70))  # Better positioned
        elif is_time_up:
            # Draw clock symbols for time up with enhanced positioning
            clock_font = pygame.font.SysFont(None, 56)  # Larger font
            clock_left = clock_font.render("TIME", True, CHESS_GOLD)
            clock_right = clock_font.render("TIME", True, CHESS_GOLD)
            screen.blit(clock_left, (box_x + 50, box_y + 70))  # Better positioned
            screen.blit(clock_right, (box_x + box_width - 80, box_y + 70))  # Better positioned
        
        # Enhanced buttons with chess theme and better positioning
        button_width_end = 240  # Increased width
        button_height_end = 65   # Increased height
        button_spacing_end = 35  # Increased spacing between buttons
        
        # Play Again button with enhanced positioning
        play_again_rect = pygame.Rect(
            (screen_w - button_width_end) // 2,
            box_y + 240,  # Better positioned
            button_width_end,
            button_height_end
        )
        
        # Main Menu button with enhanced positioning
        main_menu_rect = pygame.Rect(
            (screen_w - button_width_end) // 2,
            play_again_rect.bottom + button_spacing_end,
            button_width_end,
            button_height_end
        )
        
        # Exit button with enhanced positioning
        exit_rect = pygame.Rect(
            (screen_w - button_width_end) // 2,
            main_menu_rect.bottom + button_spacing_end,
            button_width_end,
            button_height_end
        )
        
        # Enhanced button styling with hover effects and chess theme
        mouse_pos = pygame.mouse.get_pos()
        
        # Play Again button with enhanced styling
        if play_again_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, CHESS_GOLD, play_again_rect, border_radius=15)
            pygame.draw.rect(screen, CHESS_DARK, play_again_rect, 4, border_radius=15)
            # Add glow effect
            glow_rect = pygame.Rect(play_again_rect.x - 3, play_again_rect.y - 3, 
                                   play_again_rect.width + 6, play_again_rect.height + 6)
            pygame.draw.rect(screen, CHESS_GOLD, glow_rect, border_radius=18)
        else:
            pygame.draw.rect(screen, CHESS_DARK, play_again_rect, border_radius=15)
            pygame.draw.rect(screen, CHESS_GOLD, play_again_rect, 3, border_radius=15)
        
        # Main Menu button with enhanced styling
        if main_menu_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, CHESS_SILVER, main_menu_rect, border_radius=15)
            pygame.draw.rect(screen, CHESS_DARK, main_menu_rect, 4, border_radius=15)
            # Add glow effect
            glow_rect = pygame.Rect(main_menu_rect.x - 3, main_menu_rect.y - 3, 
                                   main_menu_rect.width + 6, main_menu_rect.height + 6)
            pygame.draw.rect(screen, CHESS_SILVER, glow_rect, border_radius=18)
        else:
            pygame.draw.rect(screen, CHESS_DARK, main_menu_rect, border_radius=15)
            pygame.draw.rect(screen, CHESS_SILVER, main_menu_rect, 3, border_radius=15)
        
        # Exit button with enhanced styling
        if exit_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (220, 20, 60), exit_rect, border_radius=15)
            pygame.draw.rect(screen, CHESS_DARK, exit_rect, 4, border_radius=15)
            # Add glow effect
            glow_rect = pygame.Rect(exit_rect.x - 3, exit_rect.y - 3, 
                                   exit_rect.width + 6, exit_rect.height + 6)
            pygame.draw.rect(screen, (220, 20, 60), glow_rect, border_radius=18)
        else:
            pygame.draw.rect(screen, CHESS_DARK, exit_rect, border_radius=15)
            pygame.draw.rect(screen, (220, 20, 60), exit_rect, 3, border_radius=15)
        
        # Enhanced button text with chess symbols and better styling
        button_font = pygame.font.SysFont(None, 34, bold=True)  # Larger font
        
        text_play_again = button_font.render("Play Again", True, CHESS_LIGHT)
        text_main_menu = button_font.render("Main Menu", True, CHESS_LIGHT)
        text_exit = button_font.render("Exit Game", True, CHESS_LIGHT)
        
        # Add text shadows for better readability
        shadow_color = (0, 0, 0, 100)
        shadow_play_again = button_font.render("Play Again", True, shadow_color)
        shadow_main_menu = button_font.render("Main Menu", True, shadow_color)
        shadow_exit = button_font.render("Exit Game", True, shadow_color)
        
        # Draw shadows
        screen.blit(shadow_play_again, (play_again_rect.centerx - shadow_play_again.get_width()//2 + 1, 
                                       play_again_rect.centery - shadow_play_again.get_height()//2 + 1))
        screen.blit(shadow_main_menu, (main_menu_rect.centerx - shadow_main_menu.get_width()//2 + 1, 
                                      main_menu_rect.centery - shadow_main_menu.get_height()//2 + 1))
        screen.blit(shadow_exit, (exit_rect.centerx - shadow_exit.get_width()//2 + 1, 
                                 exit_rect.centery - shadow_exit.get_height()//2 + 1))
        
        # Draw main text
        screen.blit(text_play_again, text_play_again.get_rect(center=play_again_rect.center))
        screen.blit(text_main_menu, text_main_menu.get_rect(center=main_menu_rect.center))
        screen.blit(text_exit, text_exit.get_rect(center=exit_rect.center))
        
        return play_again_rect, main_menu_rect, exit_rect

    def format_time(seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"

    def get_user_input(prompt_text, max_length=20):
        input_box_active = True
        input_text = ""
        input_font = pygame.font.SysFont(None, 32)
        input_rect = pygame.Rect(screen_w // 2 - 150, screen_h // 2 - 50, 300, 40)
        color_inactive = (100, 100, 100)
        color_active = (150, 150, 150)
        color = color_inactive

        ok_button_rect = pygame.Rect(input_rect.x, input_rect.y + 60, 140, 40)
        cancel_button_rect = pygame.Rect(input_rect.x + 160, input_rect.y + 60, 140, 40)

        while input_box_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "", False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        color = color_active
                    else:
                        color = color_inactive
                    if ok_button_rect.collidepoint(event.pos):
                        return input_text, True
                    if cancel_button_rect.collidepoint(event.pos):
                        return "", False
                if event.type == pygame.KEYDOWN:
                    if color == color_active:
                        if event.key == pygame.K_RETURN:
                            return input_text, True
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        else:
                            if len(input_text) < max_length:
                                input_text += event.unicode

            overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            pygame.draw.rect(screen, (50, 50, 50), (input_rect.x - 10, input_rect.y - 40, input_rect.width + 20, input_rect.height + 120), border_radius=10)
            pygame.draw.rect(screen, color, input_rect, border_radius=5)
            pygame.draw.rect(screen, (200, 200, 200), input_rect, 2, border_radius=5)

            text_surface = input_font.render(input_text, True, (255, 255, 255))
            screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
            input_rect.w = max(300, text_surface.get_width() + 10)

            prompt_surface = input_font.render(prompt_text, True, (255, 255, 255))
            screen.blit(prompt_surface, (input_rect.x, input_rect.y - 30))

            pygame.draw.rect(screen, (60, 179, 113), ok_button_rect, border_radius=5)
            pygame.draw.rect(screen, (220, 20, 60), cancel_button_rect, border_radius=5)

            ok_text = input_font.render("OK", True, (255, 255, 255))
            cancel_text = input_font.render("Cancel", True, (255, 255, 255))
            screen.blit(ok_text, ok_text.get_rect(center=ok_button_rect.center))
            screen.blit(cancel_text, cancel_text.get_rect(center=cancel_button_rect.center))

            pygame.display.flip()
            clock.tick(30)

        return "", False

    update_ai()
    running = True

    # Helper function to handle game end actions (Play Again, Main Menu, Exit)
    def handle_game_end_action(action_type):
        nonlocal running, save_message_text, save_message_display_time

        # If the game was loaded from a save, delete that save
        if loaded_save_name:
            save_manager.delete_save(loaded_save_name)
            save_message_text = f"Save '{loaded_save_name}' deleted!"
            save_message_display_time = pygame.time.get_ticks() + 1500 # Show for 1.5 seconds

            # Draw message before proceeding
            screen.fill((30, 30, 30))
            message_surface = large_font.render(save_message_text, True, (255, 255, 255))
            message_rect = message_surface.get_rect(center=(screen_w // 2, screen_h // 2 - 100))
            screen.blit(message_surface, message_rect)
            pygame.display.flip()
            pygame.time.delay(1500) # Wait for message to be seen

        # Perform the requested action
        if action_type == "play_again":
            if local:
                main(FEN, local, None, time_control)
            else:
                main(FEN, local, current_ai_type)
            return # This will exit the current main call and start a new one
        elif action_type == "main_menu":
            save_config(current_ai_type, skill_level, thinking_time) # Save current AI config
            running = False # This will exit the current main loop and return to GameModes
        elif action_type == "exit":
            save_config(current_ai_type, skill_level, thinking_time) # Save current AI config
            running = False
            sys.exit() # Exit the entire application


    while running:
        current_time_ms = pygame.time.get_ticks()
        delta_time_ms = current_time_ms - last_tick_time
        last_tick_time = current_time_ms

        if local and not game_over_state:
            if chess_game.board.turn == chess.WHITE:
                player_white_time -= delta_time_ms / 1000.0
                if player_white_time <= 0:
                    player_white_time = 0
                    game_over_state = True
                    game_result_text = "White's Time is Up! Black Wins by Time!"
                    if board_renderer.audio_manager:
                        board_renderer.audio_manager.play("checkmate")
            else:
                player_black_time -= delta_time_ms / 1000.0
                if player_black_time <= 0:
                    player_black_time = 0
                    game_over_state = True
                    game_result_text = "Black's Time is Up! White Wins by Time!"
                    if board_renderer.audio_manager:
                        board_renderer.audio_manager.play("checkmate")


        screen.fill((30, 30, 30))
        window_width, window_height = screen.get_size()

        board_x = (window_width - BOARD_WIDTH) // 2
        board_y = (window_height - BOARD_HEIGHT) // 2

        board_surface = pygame.Surface((BOARD_WIDTH, BOARD_WIDTH))
        board_renderer.screen = board_surface
        board_renderer.draw_board()
        screen.blit(board_surface, (board_x, board_y))

        pygame.draw.rect(screen, (40, 40, 40), (board_x, board_y + BOARD_WIDTH, BOARD_WIDTH, MENU_HEIGHT))

        if not local and current_ai_type == "stockfish":
            skill_rect = draw_slider(board_x + 320, board_y + BOARD_WIDTH + 5, "Skill", skill_level, 0, 20, 1)
            time_rect = draw_slider(board_x + 320, board_y + BOARD_WIDTH + 35, "Time", round(thinking_time, 1), 0.5, 5.0, 0.5)
        else:
            skill_rect = pygame.Rect(0,0,0,0)
            time_rect = pygame.Rect(0,0,0,0)

        if local:
            white_time_text = font.render(f"White: {format_time(player_white_time)}", True, (255, 255, 255))
            black_time_text = font.render(f"Black: {format_time(player_black_time)}", True, (255, 255, 255))

            white_time_rect = white_time_text.get_rect(center=(board_x + BOARD_WIDTH // 4, board_y + BOARD_WIDTH + MENU_HEIGHT // 2))
            black_time_rect = black_time_text.get_rect(center=(board_x + BOARD_WIDTH * 3 // 4, board_y + BOARD_WIDTH + MENU_HEIGHT // 2))

            screen.blit(white_time_text, white_time_rect)
            screen.blit(black_time_text, black_time_rect)


        # Save_Game button
        button_width2 = 140
        button_height2 = 70

        screen_width = screen.get_width()
        screen_height = screen.get_height()

        button_x2 = (screen_width) // 20
        button_y2 = (screen_height) // 20

        DARK_BLUE = (40, 100, 160)
        BLUE = (70, 130, 180)
        color = BLUE
        button_rect2 = pygame.Rect(button_x2 , button_y2, button_width2, button_height2)

        mouse_pos = pygame.mouse.get_pos()
        if button_rect2.collidepoint(mouse_pos):
            color = DARK_BLUE
        else:
            color = BLUE

        pygame.draw.rect(screen, color, button_rect2, border_radius=12)
        text_surface2 = font.render("Save Game", True, (255, 255, 255))
        text_rect2 = text_surface2.get_rect(center=button_rect2.center)
        screen.blit(text_surface2, text_rect2)

        # The save message is drawn here in the main loop
        if save_message_text and pygame.time.get_ticks() < save_message_display_time:
            message_surface = large_font.render(save_message_text, True, (255, 255, 255))
            message_rect = message_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
            screen.blit(message_surface, message_rect)

        if not local and chess_game.board.turn == chess.BLACK and not ai_thinking and not game_over_state:
            ai_thinking = True
            pygame.display.flip()
            pygame.time.delay(1000)

            if isinstance(ai, StockfishAI):
                ai.get_best_move(chess_game.board, callback=on_ai_move)
            else:
                best_move = ai.get_best_move(chess_game.board)
                on_ai_move(best_move)

        if chess_game.is_game_over() and not game_over_state:
            game_over_state = True
            outcome = chess_game.outcome()
            
            # Determine specific game end type for better theming
            if chess_game.is_checkmate():
                if outcome and outcome.winner == chess.WHITE:
                    game_result_text = "White Wins by Checkmate!"
                elif outcome and outcome.winner == chess.BLACK:
                    game_result_text = "Black Wins by Checkmate!"
                else:
                    game_result_text = "Checkmate!"
            elif chess_game.is_stalemate():
                game_result_text = "Stalemate!"
            elif chess_game.board.is_insufficient_material():
                game_result_text = "Draw by Insufficient Material!"
            elif chess_game.board.is_fifty_moves():
                game_result_text = "Draw by Fifty-Move Rule!"
            elif chess_game.board.is_repetition():
                game_result_text = "Draw by Repetition!"
            elif outcome:
                if outcome.winner == chess.WHITE:
                    game_result_text = "White Wins!"
                elif outcome.winner == chess.BLACK:
                    game_result_text = "Black Wins!"
                else:
                    game_result_text = "Draw!"
            else:
                game_result_text = "Game Over!"
                
            if board_renderer.audio_manager:
                board_renderer.audio_manager.play("checkmate")


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_config(current_ai_type, skill_level, thinking_time)
                running = False

            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_over_state:
                    play_again_rect, main_menu_rect, exit_rect = draw_end_game_screen(game_result_text)
                    if play_again_rect.collidepoint(event.pos):
                        handle_game_end_action("play_again")
                        return # Exit current main call to start a new one
                    elif main_menu_rect.collidepoint(event.pos):
                        handle_game_end_action("main_menu")
                        return # Exit current main loop to return to GameModes
                    elif exit_rect.collidepoint(event.pos):
                        handle_game_end_action("exit")
                        # sys.exit() is called inside handle_game_end_action, so no need for return here.
                else:
                    # Handle promotion dialog clicks first
                    if board_renderer.is_promotion_active():
                        if board_renderer.handle_promotion_click(event.pos):
                            continue  # Skip other click handling if promotion was handled
                    
                    if not local and current_ai_type == "stockfish":
                        if skill_rect.collidepoint(event.pos):
                            rel_x = max(0, min(skill_rect.width, event.pos[0] - skill_rect.x))
                            skill_level = int((rel_x / skill_rect.width) * 20)
                            update_ai()
                        if time_rect.collidepoint(event.pos):
                            rel_x = max(0, min(time_rect.width, event.pos[0] - time_rect.x))
                            thinking_time = round((rel_x / time_rect.width) * 4.5 + 0.5, 1)
                            update_ai()
                    if board_x <= event.pos[0] < board_x + BOARD_WIDTH and board_y <= event.pos[1] < board_y + BOARD_WIDTH:
                        board_before_move = chess_game.board.copy()
                        board_renderer.handle_click((event.pos[0] - board_x, event.pos[1] - board_y))
                        board_renderer.start_drag((event.pos[0] - board_x, event.pos[1] - board_y))
                        if board_before_move.fen() != chess_game.board.fen():
                            pass

                    if button_rect2.collidepoint(event.pos):
                        # Logic to save the game
                        if loaded_save_name: # If the game was loaded, save with the same name
                            save_name = loaded_save_name
                            confirmed = True # No confirmation needed
                        else: # If it's a new game, ask for a name
                            save_name, confirmed = get_user_input("Saved Game Name:")
                        
                        if confirmed and save_name:
                            current_fen = chess_game.board.fen()
                            current_local = local
                            current_ai_type_for_save = current_ai_type if not local else None
                            current_skill_level = skill_level if not local and current_ai_type == "stockfish" else None
                            current_thinking_time = thinking_time if not local and current_ai_type == "stockfish" else None
                            current_time_control = time_control if local else None
                            current_white_time_left = player_white_time if local else None
                            current_black_time_left = player_black_time if local else None

                            save_manager.save_game(
                                save_name,
                                current_fen,
                                current_local,
                                current_ai_type_for_save,
                                current_skill_level,
                                current_thinking_time,
                                current_time_control,
                                current_white_time_left,
                                current_black_time_left
                            )
                            # Set the message and display time
                            save_message_text = f"Game successfully saved as '{save_name}'!"
                            save_message_display_time = pygame.time.get_ticks() + 2000 # Display for 2 seconds

                            # Draw the screen immediately to show the message
                            screen.fill((30, 30, 30)) # Clear the screen
                            # Redraw the board and menu (optional, but good for context)
                            board_surface = pygame.Surface((BOARD_WIDTH, BOARD_WIDTH))
                            board_renderer.screen = board_surface
                            board_renderer.draw_board()
                            screen.blit(board_surface, (board_x, board_y))
                            pygame.draw.rect(screen, (40, 40, 40), (board_x, board_y + BOARD_WIDTH, BOARD_WIDTH, MENU_HEIGHT))
                            
                            # Draw the save message in the center
                            message_surface = large_font.render(save_message_text, True, (255, 255, 255))
                            message_rect = message_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
                            screen.blit(message_surface, message_rect)
                            
                            pygame.display.flip() # Update the screen to show the message
                            pygame.time.delay(2000) # Wait 2 seconds for the user to see the message

                            running = False # Exit the game loop to return to the main menu
                        # Redraw the screen to remove the input box (if the user cancels or the name is empty)
                        # This final flip is important if get_user_input is canceled
                        pygame.display.flip()


            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if not game_over_state and board_x <= event.pos[0] < board_x + BOARD_WIDTH and board_y <= event.pos[1] < board_y + BOARD_WIDTH:
                    board_before_move = chess_game.board.copy()
                    board_renderer.end_drag((event.pos[0] - board_x, event.pos[1] - board_y))
                    if board_before_move.fen() != chess_game.board.fen():
                        pass

            elif event.type == pygame.MOUSEMOTION:
                if not game_over_state:
                    board_renderer.update_mouse_pos((event.pos[0] - board_x, event.pos[1] - board_y))


        if game_over_state:
            draw_end_game_screen(game_result_text)

        # Draw promotion dialog if active (must be drawn on main screen, not board surface)
        if board_renderer.is_promotion_active():
            board_renderer.promotion_dialog.screen = screen  # Set the main screen as target
            board_renderer.promotion_dialog.draw()

        pygame.display.flip()
        clock.tick(60)
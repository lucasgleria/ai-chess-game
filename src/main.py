# import pygame
# import sys
# import chess
# import json
# import os
# from src.ui.board_renderer import BoardRenderer
# from src.ui.asset_manager import AssetManager
# from src.ui.audio_manager import AudioManager
# from src.ia.easy_ai import EasyAI
# from src.ia.medium_ai import MediumAI
# from src.ia.stockfish_ai import StockfishAI
# from src.data.save_manager import SaveManager
# from src.core.chess_game import ChessGame
# import ctypes

# CONFIG_PATH = "config.json"
# BOARD_SIZE = 8
# MENU_HEIGHT = 80
# SQUARE_SIZE = 75  # Fixed square size for board (8 * 75 = 600)
# BOARD_WIDTH = SQUARE_SIZE * BOARD_SIZE
# BOARD_HEIGHT = BOARD_WIDTH + MENU_HEIGHT

# def load_config():
#     if os.path.exists(CONFIG_PATH):
#         with open(CONFIG_PATH, "r") as f:
#             return json.load(f)
#     return {"selected_ai": "stockfish", "skill_level": 8, "thinking_time": 1.5}

# def save_config(selected_ai, skill_level, thinking_time):
#     with open(CONFIG_PATH, "w") as f:
#         json.dump({
#             "selected_ai": selected_ai,
#             "skill_level": skill_level,
#             "thinking_time": thinking_time
#         }, f)

# # A função main agora recebe 'selected_ai_type'
# def main(FEN, local, selected_ai_type=None):
#     pygame.init()
#     pygame.mixer.init()

#     info = pygame.display.Info()
#     screen_w, screen_h = info.current_w, info.current_h

#     # Create a resizable window the size of the screen
#     screen = pygame.display.set_mode((screen_w, screen_h - 10), pygame.RESIZABLE)
#     ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], 3)
#     pygame.display.set_caption("AI Chess Game")

#     font = pygame.font.SysFont(None, 24)
#     large_font = pygame.font.SysFont(None, 48) # New font for game over message
#     clock = pygame.time.Clock()

#     audio_manager = AudioManager()
#     asset_manager = AssetManager(square_size=SQUARE_SIZE)
#     board_renderer = BoardRenderer(screen, SQUARE_SIZE, FEN, local, asset_manager, audio_manager)
#     save_manager = SaveManager()
#     chess_game = ChessGame(FEN)

#     config = load_config()
#     # Usamos o selected_ai_type passado, ou o do config se não for fornecido (para compatibilidade)
#     current_ai_type = selected_ai_type if selected_ai_type else config["selected_ai"]
#     skill_level = config["skill_level"]
#     thinking_time = config["thinking_time"]

#     ai = None # Inicializa como None, será definido em update_ai
#     ai_thinking = False

#     # Game state variables for end game screen
#     game_over_state = False
#     game_result_text = ""

#     def update_ai():
#         nonlocal ai
#         # Define a IA baseada no tipo selecionado
#         if current_ai_type == "easy":
#             ai = EasyAI(depth=1)
#         elif current_ai_type == "medium":
#             ai = MediumAI(depth=2)
#         elif current_ai_type == "stockfish":
#             ai = StockfishAI(skill_level=skill_level, thinking_time=thinking_time)

#     def on_ai_move(best_move):
#         nonlocal ai_thinking, game_over_state, game_result_text
#         if best_move:
#             move_uci = best_move.uci()
#             board_renderer.from_chess_square(move_uci)
#             piece = board_renderer.test_board[board_renderer.row_ai][board_renderer.col_ai]
#             if piece and board_renderer.turn == True:
#                 ai_piece = piece
#                 board_renderer.test_board[board_renderer.row_ai][board_renderer.col_ai] = None
#             captured_piece = board_renderer.test_board[board_renderer.new_row_ai][board_renderer.new_col_ai]
#             board_renderer.test_board[board_renderer.new_row_ai][board_renderer.new_col_ai] = ai_piece
#             board_renderer.chess_game.make_move(move_uci)
#             board_renderer.turn = False
#             board_renderer.last_move = move_uci

#             if board_renderer.audio_manager:
#                 if captured_piece:
#                     board_renderer.audio_manager.play("capture")
#                 else:
#                     board_renderer.audio_manager.play("move")

#             if chess_game.is_game_over():
#                 game_over_state = True
#                 outcome = chess_game.outcome()
#                 if outcome:
#                     if outcome.winner == chess.WHITE:
#                         game_result_text = "Brancas Venceram!"
#                     elif outcome.winner == chess.BLACK:
#                         game_result_text = "Pretas Venceram!"
#                     else:
#                         game_result_text = "Empate!"
#                 else:
#                     game_result_text = "Jogo Encerrado!"
#                 if board_renderer.audio_manager:
#                     board_renderer.audio_manager.play("checkmate") # Or a specific game over sound

#         ai_thinking = False

#     # A função draw_button e draw_slider permanecem, mas os botões de IA serão removidos do loop principal
#     def draw_button(rect, text, selected=False):
#         pygame.draw.rect(screen, (100, 100, 100) if selected else (60, 60, 60), rect)
#         label = font.render(text, True, (255, 255, 255))
#         screen.blit(label, (rect.x + 10, rect.y + 8))

#     def draw_slider(x, y, label_text, value, min_val, max_val, step, width=150):
#         pygame.draw.rect(screen, (90, 90, 90), (x, y + 25, width, 6))
#         knob_x = x + int((value - min_val) / (max_val - min_val) * width)
#         pygame.draw.circle(screen, (200, 200, 200), (knob_x, y + 28), 8)
#         label = font.render(f"{label_text}: {value}", True, (255, 255, 255))
#         screen.blit(label, (x, y))
#         return pygame.Rect(x, y + 25, width, 16)

#     def draw_end_game_screen(result_text):
#         # Dark overlay
#         overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
#         overlay.fill((0, 0, 0, 180)) # Semi-transparent black
#         screen.blit(overlay, (0, 0))

#         # Box for content
#         box_width = 400
#         box_height = 300
#         box_x = (screen_w - box_width) // 2
#         box_y = (screen_h - box_height) // 2
#         pygame.draw.rect(screen, (50, 50, 50), (box_x, box_y, box_width, box_height), border_radius=15)
#         pygame.draw.rect(screen, (80, 80, 80), (box_x, box_y, box_width, box_height), 3, border_radius=15) # Border

#         # Result message
#         result_surface = large_font.render(result_text, True, (255, 255, 255))
#         result_rect = result_surface.get_rect(center=(screen_w // 2, box_y + 50))
#         screen.blit(result_surface, result_rect)

#         # Buttons
#         button_width_end = 200
#         button_height_end = 50
#         button_spacing_end = 20

#         play_again_rect = pygame.Rect(
#             (screen_w - button_width_end) // 2,
#             box_y + 120,
#             button_width_end,
#             button_height_end
#         )
#         main_menu_rect = pygame.Rect(
#             (screen_w - button_width_end) // 2,
#             play_again_rect.bottom + button_spacing_end,
#             button_width_end,
#             button_height_end
#         )
#         exit_rect = pygame.Rect(
#             (screen_w - button_width_end) // 2,
#             main_menu_rect.bottom + button_spacing_end,
#             button_width_end,
#             button_height_end
#         )

#         # Hover effect
#         mouse_pos = pygame.mouse.get_pos()
#         color_play_again = (90, 90, 90) if play_again_rect.collidepoint(mouse_pos) else (60, 60, 60)
#         color_main_menu = (90, 90, 90) if main_menu_rect.collidepoint(mouse_pos) else (60, 60, 60)
#         color_exit = (90, 90, 90) if exit_rect.collidepoint(mouse_pos) else (60, 60, 60)

#         pygame.draw.rect(screen, color_play_again, play_again_rect, border_radius=10)
#         pygame.draw.rect(screen, color_main_menu, main_menu_rect, border_radius=10)
#         pygame.draw.rect(screen, color_exit, exit_rect, border_radius=10)

#         text_play_again = font.render("Jogar Novamente", True, (255, 255, 255))
#         text_main_menu = font.render("Menu Principal", True, (255, 255, 255))
#         text_exit = font.render("Sair do Jogo", True, (255, 255, 255))

#         screen.blit(text_play_again, text_play_again.get_rect(center=play_again_rect.center))
#         screen.blit(text_main_menu, text_main_menu.get_rect(center=main_menu_rect.center))
#         screen.blit(text_exit, text_exit.get_rect(center=exit_rect.center))

#         return play_again_rect, main_menu_rect, exit_rect


#     update_ai() # Chama update_ai para inicializar a IA com base em current_ai_type
#     running = True

#     while running:
#         screen.fill((30, 30, 30))
#         window_width, window_height = screen.get_size()

#         # Centering X
#         board_x = (window_width - BOARD_WIDTH) // 2
#         board_y = (window_height - BOARD_HEIGHT) // 2

#         board_surface = pygame.Surface((BOARD_WIDTH, BOARD_WIDTH))
#         board_renderer.screen = board_surface
#         board_renderer.draw_board()
#         screen.blit(board_surface, (board_x, board_y))

#         # Draw menu
#         pygame.draw.rect(screen, (40, 40, 40), (board_x, board_y + BOARD_WIDTH, BOARD_WIDTH, MENU_HEIGHT))

#         # Sliders (permanecem, pois são para Stockfish)
#         # Só desenha os sliders se a IA selecionada for Stockfish
#         if current_ai_type == "stockfish":
#             skill_rect = draw_slider(board_x + 320, board_y + BOARD_WIDTH + 5, "Skill", skill_level, 0, 20, 1)
#             time_rect = draw_slider(board_x + 320, board_y + BOARD_WIDTH + 35, "Tempo", round(thinking_time, 1), 0.5, 5.0, 0.5)
#         else:
#             # Se não for Stockfish, definimos retângulos vazios para evitar NameError
#             skill_rect = pygame.Rect(0,0,0,0)
#             time_rect = pygame.Rect(0,0,0,0)


#         # Save_Game button
#         button_width2 = 140
#         button_height2 = 70

#         screen_width = screen.get_width()
#         screen_height = screen.get_height()

#         button_x2 = (screen_width) // 20
#         button_y2 = (screen_height) // 20

#         #colors
#         DARK_BLUE = (40, 100, 160)
#         BLUE = (70, 130, 180)
#         color = BLUE
#         button_rect2 = pygame.Rect(button_x2 , button_y2, button_width2, button_height2)

#         mouse_pos = pygame.mouse.get_pos()
#         if button_rect2.collidepoint(mouse_pos):
#             color = DARK_BLUE
#         else:
#             color = BLUE

#         pygame.draw.rect(screen, color, button_rect2, border_radius=12)
#         text_surface2 = font.render("Salvar Jogo", True, (255, 255, 255))
#         text_rect2 = text_surface2.get_rect(center=button_rect2.center)
#         screen.blit(text_surface2, text_rect2)

#         # AI move logic
#         # A IA só joga se não for um jogo local (Player vs Player) e o jogo não tiver acabado
#         if not local and board_renderer.turn and not ai_thinking and not game_over_state:
#             ai_thinking = True
#             pygame.display.flip()
#             pygame.time.delay(1000)

#             if isinstance(ai, StockfishAI):
#                 ai.get_best_move(board_renderer.chess_game.board, callback=on_ai_move)
#             else:
#                 best_move = ai.get_best_move(board_renderer.chess_game.board)
#                 on_ai_move(best_move)

#         # Check for game over after each move (player or AI)
#         if chess_game.is_game_over() and not game_over_state:
#             game_over_state = True
#             outcome = chess_game.outcome()
#             if outcome:
#                 if outcome.winner == chess.WHITE:
#                     game_result_text = "Brancas Venceram!"
#                 elif outcome.winner == chess.BLACK:
#                     game_result_text = "Pretas Venceram!"
#                 else:
#                     game_result_text = "Empate!"
#             else:
#                 game_result_text = "Jogo Encerrado!"
#             if board_renderer.audio_manager:
#                 board_renderer.audio_manager.play("checkmate") # Or a specific game over sound


#         # Event handling
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 save_config(current_ai_type, skill_level, thinking_time) # Salva o tipo de IA atual
#                 running = False

#             elif event.type == pygame.VIDEORESIZE:
#                 screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

#             elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                 if game_over_state:
#                     play_again_rect, main_menu_rect, exit_rect = draw_end_game_screen(game_result_text) # Get rects for click detection
#                     if play_again_rect.collidepoint(event.pos):
#                         chess_game.new_game() # Reset the board
#                         board_renderer.FEN = chess_game.board.fen() # Update renderer FEN
#                         board_renderer.load_pieces() # Reload pieces
#                         board_renderer.turn = False # Reset turn for AI if applicable
#                         game_over_state = False # Exit end game state
#                         game_result_text = "" # Clear result text
#                         ai_thinking = False # Reset AI thinking state
#                     elif main_menu_rect.collidepoint(event.pos):
#                         save_config(current_ai_type, skill_level, thinking_time) # Salva o tipo de IA atual
#                         running = False # Sai do loop do jogo para retornar ao menu principal
#                     elif exit_rect.collidepoint(event.pos):
#                         save_config(current_ai_type, skill_level, thinking_time) # Salva o tipo de IA atual
#                         running = False
#                         sys.exit() # Exit the entire application
#                 else: # Normal game interaction (apenas se o jogo não tiver acabado)
#                     # Removidos os botões de seleção de IA daqui
#                     if current_ai_type == "stockfish": # Apenas lida com sliders se for Stockfish
#                         if skill_rect.collidepoint(event.pos):
#                             rel_x = max(0, min(skill_rect.width, event.pos[0] - skill_rect.x))
#                             skill_level = int((rel_x / skill_rect.width) * 20)
#                             update_ai()
#                         if time_rect.collidepoint(event.pos):
#                             rel_x = max(0, min(time_rect.width, event.pos[0] - time_rect.x))
#                             thinking_time = round((rel_x / time_rect.width) * 4.5 + 0.5, 1)
#                             update_ai()
#                     if board_x <= event.pos[0] < board_x + BOARD_WIDTH and board_y <= event.pos[1] < board_y + BOARD_WIDTH:
#                         board_renderer.handle_click((event.pos[0] - board_x, event.pos[1] - board_y))
#                         board_renderer.start_drag((event.pos[0] - board_x, event.pos[1] - board_y))

#                     if button_rect2.collidepoint(event.pos):
#                         save_manager.save_game(board_renderer.chess_game.board.fen())

#             elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
#                 if not game_over_state and board_x <= event.pos[0] < board_x + BOARD_WIDTH and board_y <= event.pos[1] < board_y + BOARD_WIDTH:
#                     board_renderer.end_drag((event.pos[0] - board_x, event.pos[1] - board_y))

#             elif event.type == pygame.MOUSEMOTION:
#                 if not game_over_state:
#                     board_renderer.update_mouse_pos((event.pos[0] - board_x, event.pos[1] - board_y))


#         # Draw end game screen if game is over
#         if game_over_state:
#             draw_end_game_screen(game_result_text)

#         pygame.display.flip()
#         clock.tick(60)

#     pygame.quit()
#     # Não chama sys.exit() aqui para permitir que run_main no main.py chame GameModes_windows novamente
#     # ou saia do programa completamente.

######################

# import pygame
# import sys
# import chess
# import json
# import os
# from src.ui.board_renderer import BoardRenderer
# from src.ui.asset_manager import AssetManager
# from src.ui.audio_manager import AudioManager
# from src.ia.easy_ai import EasyAI
# from src.ia.medium_ai import MediumAI
# from src.ia.stockfish_ai import StockfishAI
# from src.data.save_manager import SaveManager
# from src.core.chess_game import ChessGame
# import ctypes

# CONFIG_PATH = "config.json"
# BOARD_SIZE = 8
# MENU_HEIGHT = 80
# SQUARE_SIZE = 75  # Fixed square size for board (8 * 75 = 600)
# BOARD_WIDTH = SQUARE_SIZE * BOARD_SIZE
# BOARD_HEIGHT = BOARD_WIDTH + MENU_HEIGHT

# # Mapeamento de controle de tempo para segundos
# TIME_CONTROLS = {
#     'classic': 90 * 60,  # 90 minutos
#     'rapid': 15 * 60,    # 15 minutos (ajustado para um valor comum)
#     'blitz': 5 * 60,     # 5 minutos
#     'bullet': 1 * 60     # 1 minuto
# }

# def load_config():
#     if os.path.exists(CONFIG_PATH):
#         with open(CONFIG_PATH, "r") as f:
#             return json.load(f)
#     return {"selected_ai": "stockfish", "skill_level": 8, "thinking_time": 1.5}

# def save_config(selected_ai, skill_level, thinking_time):
#     with open(CONFIG_PATH, "w") as f:
#         json.dump({
#             "selected_ai": selected_ai,
#             "skill_level": skill_level,
#             "thinking_time": thinking_time
#         }, f)

# # A função main agora recebe 'selected_ai_type' e 'time_control'
# def main(FEN, local, selected_ai_type=None, time_control=None):
#     pygame.init()
#     pygame.mixer.init()

#     info = pygame.display.Info()
#     screen_w, screen_h = info.current_w, info.current_h

#     # Create a resizable window the size of the screen
#     screen = pygame.display.set_mode((screen_w, screen_h - 10), pygame.RESIZABLE)
#     ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], 3)
#     pygame.display.set_caption("AI Chess Game")

#     font = pygame.font.SysFont(None, 24)
#     large_font = pygame.font.SysFont(None, 48) # New font for game over message
#     clock = pygame.time.Clock()

#     audio_manager = AudioManager()
#     asset_manager = AssetManager(square_size=SQUARE_SIZE)
#     board_renderer = BoardRenderer(screen, SQUARE_SIZE, FEN, local, asset_manager, audio_manager)
#     save_manager = SaveManager()
#     chess_game = ChessGame(FEN)

#     config = load_config()
#     current_ai_type = selected_ai_type if selected_ai_type else config["selected_ai"]
#     skill_level = config["skill_level"]
#     thinking_time = config["thinking_time"]

#     ai = None # Inicializa como None, será definido em update_ai
#     ai_thinking = False

#     # Game state variables for end game screen
#     game_over_state = False
#     game_result_text = ""

#     # Timer variables for Player vs Player mode
#     player_white_time = TIME_CONTROLS.get(time_control, 0) if local else 0
#     player_black_time = TIME_CONTROLS.get(time_control, 0) if local else 0
#     last_tick_time = pygame.time.get_ticks() # Tempo do último tick para cálculo do delta

#     def update_ai():
#         nonlocal ai
#         # Define a IA baseada no tipo selecionado
#         if current_ai_type == "easy":
#             ai = EasyAI(depth=1)
#         elif current_ai_type == "medium":
#             ai = MediumAI(depth=2)
#         elif current_ai_type == "stockfish":
#             ai = StockfishAI(skill_level=skill_level, thinking_time=thinking_time)

#     def on_ai_move(best_move):
#         nonlocal ai_thinking, game_over_state, game_result_text
#         if best_move:
#             move_uci = best_move.uci()
#             board_renderer.from_chess_square(move_uci)
#             piece = board_renderer.test_board[board_renderer.row_ai][board_renderer.col_ai]
#             if piece and board_renderer.turn == True:
#                 ai_piece = piece
#                 board_renderer.test_board[board_renderer.row_ai][board_renderer.col_ai] = None
#             captured_piece = board_renderer.test_board[board_renderer.new_row_ai][board_renderer.new_col_ai]
#             board_renderer.test_board[board_renderer.new_row_ai][board_renderer.new_col_ai] = ai_piece
#             board_renderer.chess_game.make_move(move_uci)
#             board_renderer.turn = False
#             board_renderer.last_move = move_uci

#             if board_renderer.audio_manager:
#                 if captured_piece:
#                     board_renderer.audio_manager.play("capture")
#                 else:
#                     board_renderer.audio_manager.play("move")

#             if chess_game.is_game_over():
#                 game_over_state = True
#                 outcome = chess_game.outcome()
#                 if outcome:
#                     if outcome.winner == chess.WHITE:
#                         game_result_text = "Brancas Venceram!"
#                     elif outcome.winner == chess.BLACK:
#                         game_result_text = "Pretas Venceram!"
#                     else:
#                         game_result_text = "Empate!"
#                 else:
#                     game_result_text = "Jogo Encerrado!"
#                 if board_renderer.audio_manager:
#                     board_renderer.audio_manager.play("checkmate") # Or a specific game over sound

#         ai_thinking = False

#     def draw_button(rect, text, selected=False):
#         pygame.draw.rect(screen, (100, 100, 100) if selected else (60, 60, 60), rect)
#         label = font.render(text, True, (255, 255, 255))
#         screen.blit(label, (rect.x + 10, rect.y + 8))

#     def draw_slider(x, y, label_text, value, min_val, max_val, step, width=150):
#         pygame.draw.rect(screen, (90, 90, 90), (x, y + 25, width, 6))
#         knob_x = x + int((value - min_val) / (max_val - min_val) * width)
#         pygame.draw.circle(screen, (200, 200, 200), (knob_x, y + 28), 8)
#         label = font.render(f"{label_text}: {value}", True, (255, 255, 255))
#         screen.blit(label, (x, y))
#         return pygame.Rect(x, y + 25, width, 16)

#     def draw_end_game_screen(result_text):
#         # Dark overlay
#         overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
#         overlay.fill((0, 0, 0, 180)) # Semi-transparent black
#         screen.blit(overlay, (0, 0))

#         # Box for content
#         box_width = 400
#         box_height = 300
#         box_x = (screen_w - box_width) // 2
#         box_y = (screen_h - box_height) // 2
#         pygame.draw.rect(screen, (50, 50, 50), (box_x, box_y, box_width, box_height), border_radius=15)
#         pygame.draw.rect(screen, (80, 80, 80), (box_x, box_y, box_width, box_height), 3, border_radius=15) # Border

#         # Result message
#         result_surface = large_font.render(result_text, True, (255, 255, 255))
#         result_rect = result_surface.get_rect(center=(screen_w // 2, box_y + 50))
#         screen.blit(result_surface, result_rect)

#         # Buttons
#         button_width_end = 200
#         button_height_end = 50
#         button_spacing_end = 20

#         play_again_rect = pygame.Rect(
#             (screen_w - button_width_end) // 2,
#             box_y + 120,
#             button_width_end,
#             button_height_end
#         )
#         main_menu_rect = pygame.Rect(
#             (screen_w - button_width_end) // 2,
#             play_again_rect.bottom + button_spacing_end,
#             button_width_end,
#             button_height_end
#         )
#         exit_rect = pygame.Rect(
#             (screen_w - button_width_end) // 2,
#             main_menu_rect.bottom + button_spacing_end,
#             button_width_end,
#             button_height_end
#         )

#         # Hover effect
#         mouse_pos = pygame.mouse.get_pos()
#         color_play_again = (90, 90, 90) if play_again_rect.collidepoint(mouse_pos) else (60, 60, 60)
#         color_main_menu = (90, 90, 90) if main_menu_rect.collidepoint(mouse_pos) else (60, 60, 60)
#         color_exit = (90, 90, 90) if exit_rect.collidepoint(mouse_pos) else (60, 60, 60)

#         pygame.draw.rect(screen, color_play_again, play_again_rect, border_radius=10)
#         pygame.draw.rect(screen, color_main_menu, main_menu_rect, border_radius=10)
#         pygame.draw.rect(screen, color_exit, exit_rect, border_radius=10)

#         text_play_again = font.render("Jogar Novamente", True, (255, 255, 255))
#         text_main_menu = font.render("Menu Principal", True, (255, 255, 255))
#         text_exit = font.render("Sair do Jogo", True, (255, 255, 255))

#         screen.blit(text_play_again, text_play_again.get_rect(center=play_again_rect.center))
#         screen.blit(text_main_menu, text_main_menu.get_rect(center=main_menu_rect.center))
#         screen.blit(text_exit, text_exit.get_rect(center=exit_rect.center))

#         return play_again_rect, main_menu_rect, exit_rect

#     # Função para formatar o tempo em MM:SS
#     def format_time(seconds):
#         minutes = int(seconds // 60)
#         seconds = int(seconds % 60)
#         return f"{minutes:02}:{seconds:02}"


#     update_ai() # Chama update_ai para inicializar a IA com base em current_ai_type
#     running = True

#     while running:
#         current_time_ms = pygame.time.get_ticks()
#         delta_time_ms = current_time_ms - last_tick_time
#         last_tick_time = current_time_ms

#         if local and not game_over_state:
#             if chess_game.board.turn == chess.WHITE:
#                 player_white_time -= delta_time_ms / 1000.0
#                 if player_white_time <= 0:
#                     player_white_time = 0
#                     game_over_state = True
#                     game_result_text = "Tempo das Brancas Esgotado! Pretas Venceram!"
#                     if board_renderer.audio_manager:
#                         board_renderer.audio_manager.play("checkmate")
#             else: # chess.BLACK
#                 player_black_time -= delta_time_ms / 1000.0
#                 if player_black_time <= 0:
#                     player_black_time = 0
#                     game_over_state = True
#                     game_result_text = "Tempo das Pretas Esgotado! Brancas Venceram!"
#                     if board_renderer.audio_manager:
#                         board_renderer.audio_manager.play("checkmate")


#         screen.fill((30, 30, 30))
#         window_width, window_height = screen.get_size()

#         # Centering X
#         board_x = (window_width - BOARD_WIDTH) // 2
#         board_y = (window_height - BOARD_HEIGHT) // 2

#         board_surface = pygame.Surface((BOARD_WIDTH, BOARD_WIDTH))
#         board_renderer.screen = board_surface
#         board_renderer.draw_board()
#         screen.blit(board_surface, (board_x, board_y))

#         # Draw menu
#         pygame.draw.rect(screen, (40, 40, 40), (board_x, board_y + BOARD_WIDTH, BOARD_WIDTH, MENU_HEIGHT))

#         # Sliders (permanecem, pois são para Stockfish)
#         # Só desenha os sliders se a IA selecionada for Stockfish E NÃO for um jogo local
#         if not local and current_ai_type == "stockfish":
#             skill_rect = draw_slider(board_x + 320, board_y + BOARD_WIDTH + 5, "Habilidade", skill_level, 0, 20, 1)
#             time_rect = draw_slider(board_x + 320, board_y + BOARD_WIDTH + 35, "Tempo", round(thinking_time, 1), 0.5, 5.0, 0.5)
#         else:
#             # Se não for Stockfish ou for jogo local, definimos retângulos vazios para evitar NameError
#             skill_rect = pygame.Rect(0,0,0,0)
#             time_rect = pygame.Rect(0,0,0,0)

#         # Exibir temporizadores se for um jogo local (Player vs Player)
#         if local:
#             white_time_text = font.render(f"Brancas: {format_time(player_white_time)}", True, (255, 255, 255))
#             black_time_text = font.render(f"Pretas: {format_time(player_black_time)}", True, (255, 255, 255))

#             # Ajustar a posição para que fique no centro da área do menu
#             white_time_rect = white_time_text.get_rect(center=(board_x + BOARD_WIDTH // 4, board_y + BOARD_WIDTH + MENU_HEIGHT // 2))
#             black_time_rect = black_time_text.get_rect(center=(board_x + BOARD_WIDTH * 3 // 4, board_y + BOARD_WIDTH + MENU_HEIGHT // 2))

#             screen.blit(white_time_text, white_time_rect)
#             screen.blit(black_time_text, black_time_rect)


#         # Save_Game button
#         button_width2 = 140
#         button_height2 = 70

#         screen_width = screen.get_width()
#         screen_height = screen.get_height()

#         button_x2 = (screen_width) // 20
#         button_y2 = (screen_height) // 20

#         #colors
#         DARK_BLUE = (40, 100, 160)
#         BLUE = (70, 130, 180)
#         color = BLUE
#         button_rect2 = pygame.Rect(button_x2 , button_y2, button_width2, button_height2)

#         mouse_pos = pygame.mouse.get_pos()
#         if button_rect2.collidepoint(mouse_pos):
#             color = DARK_BLUE
#         else:
#             color = BLUE

#         pygame.draw.rect(screen, color, button_rect2, border_radius=12)
#         text_surface2 = font.render("Salvar Jogo", True, (255, 255, 255))
#         text_rect2 = text_surface2.get_rect(center=button_rect2.center)
#         screen.blit(text_surface2, text_rect2)

#         # AI move logic
#         # A IA só joga se não for um jogo local (Player vs Player) e o jogo não tiver acabado
#         if not local and board_renderer.turn and not ai_thinking and not game_over_state:
#             ai_thinking = True
#             pygame.display.flip()
#             pygame.time.delay(1000)

#             if isinstance(ai, StockfishAI):
#                 ai.get_best_move(board_renderer.chess_game.board, callback=on_ai_move)
#             else:
#                 best_move = ai.get_best_move(board_renderer.chess_game.board)
#                 on_ai_move(best_move)

#         # Check for game over after each move (player or AI)
#         if chess_game.is_game_over() and not game_over_state:
#             game_over_state = True
#             outcome = chess_game.outcome()
#             if outcome:
#                 if outcome.winner == chess.WHITE:
#                     game_result_text = "Brancas Venceram!"
#                 elif outcome.winner == chess.BLACK:
#                     game_result_text = "Pretas Venceram!"
#                 else:
#                     game_result_text = "Empate!"
#             else:
#                 game_result_text = "Jogo Encerrado!"
#             if board_renderer.audio_manager:
#                 board_renderer.audio_manager.play("checkmate") # Or a specific game over sound


#         # Event handling
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 save_config(current_ai_type, skill_level, thinking_time) # Salva o tipo de IA atual
#                 running = False

#             elif event.type == pygame.VIDEORESIZE:
#                 screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

#             elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#                 if game_over_state:
#                     play_again_rect, main_menu_rect, exit_rect = draw_end_game_screen(game_result_text) # Get rects for click detection
#                     if play_again_rect.collidepoint(event.pos):
#                         # Se for um jogo local, reinicia com o mesmo controle de tempo
#                         if local:
#                             main(FEN, local, None, time_control)
#                         else: # Se for contra IA, reinicia com a mesma IA
#                             main(FEN, local, current_ai_type)
#                         return # Sai da função main atual para iniciar uma nova
#                     elif main_menu_rect.collidepoint(event.pos):
#                         save_config(current_ai_type, skill_level, thinking_time) # Salva o tipo de IA atual
#                         running = False # Sai do loop do jogo para retornar ao menu principal
#                     elif exit_rect.collidepoint(event.pos):
#                         save_config(current_ai_type, skill_level, thinking_time) # Salva o tipo de IA atual
#                         running = False
#                         sys.exit() # Exit the entire application
#                 else: # Normal game interaction (apenas se o jogo não tiver acabado)
#                     # Removidos os botões de seleção de IA daqui
#                     if not local and current_ai_type == "stockfish": # Apenas lida com sliders se for Stockfish e não for jogo local
#                         if skill_rect.collidepoint(event.pos):
#                             rel_x = max(0, min(skill_rect.width, event.pos[0] - skill_rect.x))
#                             skill_level = int((rel_x / skill_rect.width) * 20)
#                             update_ai()
#                         if time_rect.collidepoint(event.pos):
#                             rel_x = max(0, min(time_rect.width, event.pos[0] - time_rect.x))
#                             thinking_time = round((rel_x / time_rect.width) * 4.5 + 0.5, 1)
#                             update_ai()
#                     if board_x <= event.pos[0] < board_x + BOARD_WIDTH and board_y <= event.pos[1] < board_y + BOARD_WIDTH:
#                         # Se for um jogo local, a troca de turno é feita após um movimento válido
#                         if local:
#                             # Captura o estado do tabuleiro antes do movimento para verificar se houve um movimento válido
#                             board_before_move = chess_game.board.copy()
#                             board_renderer.handle_click((event.pos[0] - board_x, event.pos[1] - board_y))
#                             board_renderer.start_drag((event.pos[0] - board_x, event.pos[1] - board_y))
#                             # Se o tabuleiro mudou, significa que um movimento válido foi feito
#                             if board_before_move.fen() != chess_game.board.fen():
#                                 board_renderer.turn = not board_renderer.turn # Troca o turno para o próximo jogador
#                         else: # Jogo contra IA, a lógica de turno já é diferente
#                             board_renderer.handle_click((event.pos[0] - board_x, event.pos[1] - board_y))
#                             board_renderer.start_drag((event.pos[0] - board_x, event.pos[1] - board_y))


#                     if button_rect2.collidepoint(event.pos):
#                         save_manager.save_game(board_renderer.chess_game.board.fen())

#             elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
#                 if not game_over_state and board_x <= event.pos[0] < board_x + BOARD_WIDTH and board_y <= event.pos[1] < board_y + BOARD_WIDTH:
#                     # Se for um jogo local, a troca de turno é feita após um movimento válido
#                     if local:
#                         board_before_move = chess_game.board.copy()
#                         board_renderer.end_drag((event.pos[0] - board_x, event.pos[1] - board_y))
#                         if board_before_move.fen() != chess_game.board.fen():
#                             board_renderer.turn = not board_renderer.turn # Troca o turno para o próximo jogador
#                     else:
#                         board_renderer.end_drag((event.pos[0] - board_x, event.pos[1] - board_y))

#             elif event.type == pygame.MOUSEMOTION:
#                 if not game_over_state:
#                     board_renderer.update_mouse_pos((event.pos[0] - board_x, event.pos[1] - board_y))


#         # Draw end game screen if game is over
#         if game_over_state:
#             draw_end_game_screen(game_result_text)

#         pygame.display.flip()
#         clock.tick(60)

#     pygame.quit()
#     # Não chama sys.exit() aqui para permitir que run_main no main.py chame GameModes_windows novamente
#     # ou saia do programa completamente.

import pygame
import sys
import chess
import json
import os
from src.ui.board_renderer import BoardRenderer
from src.ui.asset_manager import AssetManager
from src.ui.audio_manager import AudioManager
from src.ia.easy_ai import EasyAI
from src.ia.medium_ai import MediumAI
from src.ia.stockfish_ai import StockfishAI
from src.data.save_manager import SaveManager
from src.core.chess_game import ChessGame
import ctypes

CONFIG_PATH = "config.json"
BOARD_SIZE = 8
MENU_HEIGHT = 80
SQUARE_SIZE = 75  # Fixed square size for board (8 * 75 = 600)
BOARD_WIDTH = SQUARE_SIZE * BOARD_SIZE
BOARD_HEIGHT = BOARD_WIDTH + MENU_HEIGHT

# Mapeamento de controle de tempo para segundos
TIME_CONTROLS = {
    'classic': 90 * 60,  # 90 minutos
    'rapid': 15 * 60,    # 15 minutos (ajustado para um valor comum)
    'blitz': 5 * 60,     # 5 minutos
    'bullet': 1 * 60     # 1 minuto
}

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {"selected_ai": "stockfish", "skill_level": 8, "thinking_time": 1.5}

def save_config(selected_ai, skill_level, thinking_time):
    with open(CONFIG_PATH, "w") as f:
        json.dump({
            "selected_ai": selected_ai,
            "skill_level": skill_level,
            "thinking_time": thinking_time
        }, f)

# A função main agora recebe 'selected_ai_type' e 'time_control'
def main(FEN, local, selected_ai_type=None, time_control=None):
    pygame.init()
    pygame.mixer.init()

    info = pygame.display.Info()
    screen_w, screen_h = info.current_w, info.current_h

    # Create a resizable window the size of the screen
    screen = pygame.display.set_mode((screen_w, screen_h - 10), pygame.RESIZABLE)
    ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], 3)
    pygame.display.set_caption("AI Chess Game")

    font = pygame.font.SysFont(None, 24)
    large_font = pygame.font.SysFont(None, 48) # New font for game over message
    clock = pygame.time.Clock()

    audio_manager = AudioManager()
    asset_manager = AssetManager(square_size=SQUARE_SIZE)
    save_manager = SaveManager()

    # Crie a instância de ChessGame AQUI
    chess_game = ChessGame(FEN)
    # Passe a instância de chess_game para o BoardRenderer
    board_renderer = BoardRenderer(screen, SQUARE_SIZE, chess_game, local, asset_manager, audio_manager)


    config = load_config()
    current_ai_type = selected_ai_type if selected_ai_type else config["selected_ai"]
    skill_level = config["skill_level"]
    thinking_time = config["thinking_time"]

    ai = None # Inicializa como None, será definido em update_ai
    ai_thinking = False

    # Game state variables for end game screen
    game_over_state = False
    game_result_text = ""

    # Timer variables for Player vs Player mode
    player_white_time = TIME_CONTROLS.get(time_control, 0) if local else 0
    player_black_time = TIME_CONTROLS.get(time_control, 0) if local else 0
    last_tick_time = pygame.time.get_ticks() # Tempo do último tick para cálculo do delta

    def update_ai():
        nonlocal ai
        # Define a IA baseada no tipo selecionado
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
            # A chamada para board_renderer.from_chess_square e manipulação de test_board
            # deve ser revisada se board_renderer já usa self.chess_game.board
            # Por enquanto, vamos manter a lógica de movimento do tabuleiro principal
            board_renderer.chess_game.make_move(move_uci) # Isso atualiza chess_game.board.turn
            board_renderer.last_move = move_uci # Isso é para o renderizador

            # Atualizar o estado visual do tabuleiro após o movimento da IA
            # (Assumindo que board_renderer.draw_board() usa o estado atual de chess_game.board)
            board_renderer.load_pieces() # Recarrega as peças para refletir o novo FEN

            if board_renderer.audio_manager:
                # Não há como saber se capturou apenas pelo best_move, mas o make_move já cuida disso
                board_renderer.audio_manager.play("move") # Toca som de movimento

            if chess_game.is_game_over():
                game_over_state = True
                outcome = chess_game.outcome()
                if outcome:
                    if outcome.winner == chess.WHITE:
                        game_result_text = "Brancas Venceram!"
                    elif outcome.winner == chess.BLACK:
                        game_result_text = "Pretas Venceram!"
                    else:
                        game_result_text = "Empate!"
                else:
                    game_result_text = "Jogo Encerrado!"
                if board_renderer.audio_manager:
                    board_renderer.audio_manager.play("checkmate") # Or a specific game over sound

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
        # Dark overlay
        overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180)) # Semi-transparent black
        screen.blit(overlay, (0, 0))

        # Box for content
        box_width = 400
        box_height = 300
        box_x = (screen_w - box_width) // 2
        box_y = (screen_h - box_height) // 2
        pygame.draw.rect(screen, (50, 50, 50), (box_x, box_y, box_width, box_height), border_radius=15)
        pygame.draw.rect(screen, (80, 80, 80), (box_x, box_y, box_width, box_height), 3, border_radius=15) # Border

        # Result message
        result_surface = large_font.render(result_text, True, (255, 255, 255))
        result_rect = result_surface.get_rect(center=(screen_w // 2, box_y + 50))
        screen.blit(result_surface, result_rect)

        # Buttons
        button_width_end = 200
        button_height_end = 50
        button_spacing_end = 20

        play_again_rect = pygame.Rect(
            (screen_w - button_width_end) // 2,
            box_y + 120,
            button_width_end,
            button_height_end
        )
        main_menu_rect = pygame.Rect(
            (screen_w - button_width_end) // 2,
            play_again_rect.bottom + button_spacing_end,
            button_width_end,
            button_height_end
        )
        exit_rect = pygame.Rect(
            (screen_w - button_width_end) // 2,
            main_menu_rect.bottom + button_spacing_end,
            button_width_end,
            button_height_end
        )

        # Hover effect
        mouse_pos = pygame.mouse.get_pos()
        color_play_again = (90, 90, 90) if play_again_rect.collidepoint(mouse_pos) else (60, 60, 60)
        color_main_menu = (90, 90, 90) if main_menu_rect.collidepoint(mouse_pos) else (60, 60, 60)
        color_exit = (90, 90, 90) if exit_rect.collidepoint(mouse_pos) else (60, 60, 60)

        pygame.draw.rect(screen, color_play_again, play_again_rect, border_radius=10)
        pygame.draw.rect(screen, color_main_menu, main_menu_rect, border_radius=10)
        pygame.draw.rect(screen, color_exit, exit_rect, border_radius=10)

        text_play_again = font.render("Jogar Novamente", True, (255, 255, 255))
        text_main_menu = font.render("Menu Principal", True, (255, 255, 255))
        text_exit = font.render("Sair do Jogo", True, (255, 255, 255))

        screen.blit(text_play_again, text_play_again.get_rect(center=play_again_rect.center))
        screen.blit(text_main_menu, text_main_menu.get_rect(center=main_menu_rect.center))
        screen.blit(text_exit, text_exit.get_rect(center=exit_rect.center))

        return play_again_rect, main_menu_rect, exit_rect

    # Função para formatar o tempo em MM:SS
    def format_time(seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02}:{seconds:02}"


    update_ai() # Chama update_ai para inicializar a IA com base em current_ai_type
    running = True

    while running:
        current_time_ms = pygame.time.get_ticks()
        delta_time_ms = current_time_ms - last_tick_time
        last_tick_time = current_time_ms

        # Lógica do temporizador
        if local and not game_over_state:
            # O tempo decrementa de acordo com o turno do tabuleiro (chess_game.board.turn)
            if chess_game.board.turn == chess.WHITE:
                player_white_time -= delta_time_ms / 1000.0
                if player_white_time <= 0:
                    player_white_time = 0
                    game_over_state = True
                    game_result_text = "Tempo das Brancas Esgotado! Pretas Venceram!"
                    if board_renderer.audio_manager:
                        board_renderer.audio_manager.play("checkmate")
            else: # chess.BLACK
                player_black_time -= delta_time_ms / 1000.0
                if player_black_time <= 0:
                    player_black_time = 0
                    game_over_state = True
                    game_result_text = "Tempo das Pretas Esgotado! Brancas Venceram!"
                    if board_renderer.audio_manager:
                        board_renderer.audio_manager.play("checkmate")


        screen.fill((30, 30, 30))
        window_width, window_height = screen.get_size()

        # Centering X
        board_x = (window_width - BOARD_WIDTH) // 2
        board_y = (window_height - BOARD_HEIGHT) // 2

        board_surface = pygame.Surface((BOARD_WIDTH, BOARD_WIDTH))
        board_renderer.screen = board_surface
        board_renderer.draw_board()
        screen.blit(board_surface, (board_x, board_y))

        # Draw menu
        pygame.draw.rect(screen, (40, 40, 40), (board_x, board_y + BOARD_WIDTH, BOARD_WIDTH, MENU_HEIGHT))

        # Sliders (permanecem, pois são para Stockfish)
        # Só desenha os sliders se a IA selecionada for Stockfish E NÃO for um jogo local
        if not local and current_ai_type == "stockfish":
            skill_rect = draw_slider(board_x + 320, board_y + BOARD_WIDTH + 5, "Habilidade", skill_level, 0, 20, 1)
            time_rect = draw_slider(board_x + 320, board_y + BOARD_WIDTH + 35, "Tempo", round(thinking_time, 1), 0.5, 5.0, 0.5)
        else:
            # Se não for Stockfish ou for jogo local, definimos retângulos vazios para evitar NameError
            skill_rect = pygame.Rect(0,0,0,0)
            time_rect = pygame.Rect(0,0,0,0)

        # Exibir temporizadores se for um jogo local (Player vs Player)
        if local:
            white_time_text = font.render(f"Brancas: {format_time(player_white_time)}", True, (255, 255, 255))
            black_time_text = font.render(f"Pretas: {format_time(player_black_time)}", True, (255, 255, 255))

            # Ajustar a posição para que fique no centro da área do menu
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

        #colors
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
        text_surface2 = font.render("Salvar Jogo", True, (255, 255, 255))
        text_rect2 = text_surface2.get_rect(center=button_rect2.center)
        screen.blit(text_surface2, text_rect2)

        # AI move logic
        # A IA só joga se não for um jogo local (Player vs Player) e o jogo não tiver acabado
        # A IA joga quando for a vez das pretas (chess.BLACK)
        if not local and chess_game.board.turn == chess.BLACK and not ai_thinking and not game_over_state:
            ai_thinking = True
            pygame.display.flip()
            pygame.time.delay(1000)

            if isinstance(ai, StockfishAI):
                ai.get_best_move(chess_game.board, callback=on_ai_move)
            else:
                best_move = ai.get_best_move(chess_game.board)
                on_ai_move(best_move)

        # Check for game over after each move (player or AI)
        if chess_game.is_game_over() and not game_over_state:
            game_over_state = True
            outcome = chess_game.outcome()
            if outcome:
                if outcome.winner == chess.WHITE:
                    game_result_text = "Brancas Venceram!"
                elif outcome.winner == chess.BLACK:
                    game_result_text = "Pretas Venceram!"
                else:
                    game_result_text = "Empate!"
            else:
                game_result_text = "Jogo Encerrado!"
            if board_renderer.audio_manager:
                board_renderer.audio_manager.play("checkmate") # Or a specific game over sound


        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_config(current_ai_type, skill_level, thinking_time) # Salva o tipo de IA atual
                running = False

            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_over_state:
                    play_again_rect, main_menu_rect, exit_rect = draw_end_game_screen(game_result_text) # Get rects for click detection
                    if play_again_rect.collidepoint(event.pos):
                        # Se for um jogo local, reinicia com o mesmo controle de tempo
                        if local:
                            main(FEN, local, None, time_control)
                        else: # Se for contra IA, reinicia com a mesma IA
                            main(FEN, local, current_ai_type)
                        return # Sai da função main atual para iniciar uma nova
                    elif main_menu_rect.collidepoint(event.pos):
                        save_config(current_ai_type, skill_level, thinking_time) # Salva o tipo de IA atual
                        running = False # Sai do loop do jogo para retornar ao menu principal
                    elif exit_rect.collidepoint(event.pos):
                        save_config(current_ai_type, skill_level, thinking_time) # Salva o tipo de IA atual
                        running = False
                        sys.exit() # Exit the entire application
                else: # Normal game interaction (apenas se o jogo não tiver acabado)
                    # Apenas lida com sliders se for Stockfish e não for jogo local
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
                        # Captura o estado do tabuleiro antes do movimento para verificar se houve um movimento válido
                        board_before_move = chess_game.board.copy()
                        board_renderer.handle_click((event.pos[0] - board_x, event.pos[1] - board_y))
                        board_renderer.start_drag((event.pos[0] - board_x, event.pos[1] - board_y))
                        # Se o tabuleiro mudou, significa que um movimento válido foi feito
                        if board_before_move.fen() != chess_game.board.fen():
                            # O turno do Pygame é atualizado para refletir o turno do tabuleiro de xadrez
                            # board_renderer.turn = chess_game.board.turn == chess.BLACK # REMOVIDO: Isso era uma duplicação
                            pass # A troca de turno já é feita por chess_game.make_move()

                    if button_rect2.collidepoint(event.pos):
                        save_manager.save_game(board_renderer.chess_game.board.fen())

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if not game_over_state and board_x <= event.pos[0] < board_x + BOARD_WIDTH and board_y <= event.pos[1] < board_y + BOARD_WIDTH:
                    board_before_move = chess_game.board.copy()
                    board_renderer.end_drag((event.pos[0] - board_x, event.pos[1] - board_y))
                    if board_before_move.fen() != chess_game.board.fen():
                        # O turno do Pygame é atualizado para refletir o turno do tabuleiro de xadrez
                        # board_renderer.turn = chess_game.board.turn == chess.BLACK # REMOVIDO: Isso era uma duplicação
                        pass # A troca de turno já é feita por chess_game.make_move()


            elif event.type == pygame.MOUSEMOTION:
                if not game_over_state:
                    board_renderer.update_mouse_pos((event.pos[0] - board_x, event.pos[1] - board_y))


        # Draw end game screen if game is over
        if game_over_state:
            draw_end_game_screen(game_result_text)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    # Não chama sys.exit() aqui para permitir que run_main no main.py chame GameModes_windows novamente
    # ou saia do programa completamente.

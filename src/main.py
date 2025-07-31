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
from src.data.save_manager import SaveManager


CONFIG_PATH = "config.json"
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

def main(FEN, local, selected_ai_type=None, time_control=None, white_time_left=None, black_time_left=None, loaded_save_name=None):
    # DEBUG: Mostra o valor de loaded_save_name ao entrar na função main
    print(f"DEBUG: main function entered. loaded_save_name: {loaded_save_name}")

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

    # IMPORTADO AQUI: Garante que ChessGame esteja definido quando main é executada
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
        overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        box_width = 400
        box_height = 300
        box_x = (screen_w - box_width) // 2
        box_y = (screen_h - box_height) // 2
        pygame.draw.rect(screen, (50, 50, 50), (box_x, box_y, box_width, box_height), border_radius=15)
        pygame.draw.rect(screen, (80, 80, 80), (box_x, box_y, box_width, box_height), 3, border_radius=15)

        result_surface = large_font.render(result_text, True, (255, 255, 255))
        result_rect = result_surface.get_rect(center=(screen_w // 2, box_y + 50))
        screen.blit(result_surface, result_rect)

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
            cancel_text = input_font.render("Cancelar", True, (255, 255, 255))
            screen.blit(ok_text, ok_text.get_rect(center=ok_button_rect.center))
            screen.blit(cancel_text, cancel_text.get_rect(center=cancel_button_rect.center))

            pygame.display.flip()
            clock.tick(30)

        return "", False

    update_ai()
    running = True

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
                    game_result_text = "Tempo das Brancas Esgotado! Pretas Venceram!"
                    if board_renderer.audio_manager:
                        board_renderer.audio_manager.play("checkmate")
            else:
                player_black_time -= delta_time_ms / 1000.0
                if player_black_time <= 0:
                    player_black_time = 0
                    game_over_state = True
                    game_result_text = "Tempo das Pretas Esgotado! Brancas Venceram!"
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
            skill_rect = draw_slider(board_x + 320, board_y + BOARD_WIDTH + 5, "Habilidade", skill_level, 0, 20, 1)
            time_rect = draw_slider(board_x + 320, board_y + BOARD_WIDTH + 35, "Tempo", round(thinking_time, 1), 0.5, 5.0, 0.5)
        else:
            skill_rect = pygame.Rect(0,0,0,0)
            time_rect = pygame.Rect(0,0,0,0)

        if local:
            white_time_text = font.render(f"Brancas: {format_time(player_white_time)}", True, (255, 255, 255))
            black_time_text = font.render(f"Pretas: {format_time(player_black_time)}", True, (255, 255, 255))

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
        text_surface2 = font.render("Salvar Jogo", True, (255, 255, 255))
        text_rect2 = text_surface2.get_rect(center=button_rect2.center)
        screen.blit(text_surface2, text_rect2)

        # A mensagem de save é desenhada aqui no loop principal
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
                        if local:
                            main(FEN, local, None, time_control)
                        else:
                            main(FEN, local, current_ai_type)
                        return
                    elif main_menu_rect.collidepoint(event.pos):
                        save_config(current_ai_type, skill_level, thinking_time)
                        running = False
                    elif exit_rect.collidepoint(event.pos):
                        save_config(current_ai_type, skill_level, thinking_time)
                        running = False
                        sys.exit()
                else:
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
                        # DEBUG: Valor de loaded_save_name no momento do clique no botão Salvar
                        print(f"DEBUG: Save button clicked. loaded_save_name: {loaded_save_name}")
                        
                        # Lógica para salvar o jogo
                        if loaded_save_name: # Se o jogo foi carregado, salva com o mesmo nome
                            save_name = loaded_save_name
                            confirmed = True # Não precisa de confirmação
                        else: # Se for um jogo novo, pede o nome
                            save_name, confirmed = get_user_input("Nome do Jogo Salvo:")
                        
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
                            # Define a mensagem e o tempo de exibição
                            save_message_text = f"Jogo salvo com sucesso em '{save_name}'!"
                            save_message_display_time = pygame.time.get_ticks() + 2000 # Exibe por 2 segundos

                            # Desenha a tela imediatamente para mostrar a mensagem
                            screen.fill((30, 30, 30)) # Limpa a tela
                            # Redesenha o tabuleiro e o menu (opcional, mas bom para contexto)
                            board_surface = pygame.Surface((BOARD_WIDTH, BOARD_WIDTH))
                            board_renderer.screen = board_surface
                            board_renderer.draw_board()
                            screen.blit(board_surface, (board_x, board_y))
                            pygame.draw.rect(screen, (40, 40, 40), (board_x, board_y + BOARD_WIDTH, BOARD_WIDTH, MENU_HEIGHT))
                            
                            # Desenha a mensagem de save no centro
                            message_surface = large_font.render(save_message_text, True, (255, 255, 255))
                            message_rect = message_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
                            screen.blit(message_surface, message_rect)
                            
                            pygame.display.flip() # Atualiza a tela para mostrar a mensagem
                            pygame.time.delay(2000) # Espera 2 segundos para o usuário ver a mensagem

                            running = False # Sai do loop do jogo para retornar ao menu principal
                        # Redesenha a tela para remover o input box (se o usuário cancelar ou o nome for vazio)
                        # Este flip final é importante se o get_user_input for cancelado
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

        pygame.display.flip()
        clock.tick(60)

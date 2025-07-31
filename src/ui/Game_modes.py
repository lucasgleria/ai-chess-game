import pygame
import sys
import chess
from src.main import main # Importa a função main do src/main.py
from src.data.save_manager import SaveManager # Importa o SaveManager

class GameModes:
    def __init__(self, screen, save_manager):
        self.screen = screen
        self.save_manager = save_manager

        self.screen_width, self.screen_height = self.screen.get_size()
        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 48)

        self.WHITE = (255, 255, 255)
        self.BLUE = (70, 130, 180)
        self.DARK_BLUE = (40, 100, 160)
        self.GRAY = (150, 150, 150)
        self.LIGHT_GRAY = (180, 180, 180)
        self.RED = (200, 50, 50)
        self.DARK_RED = (150, 30, 30)

        self.FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        # Variáveis de estado para controlar qual tela está ativa
        self.current_state = 'main_menu' # 'main_menu', 'pvp_setup_menu', 'pvai_setup_menu', 'load_game_menu', 'settings_menu'

        # Configurações para o menu de Jogador vs IA
        self.selected_ai_mode = "stockfish"
        self.ai_modes = ["easy", "medium", "stockfish"] # Não inclui "local_player" aqui

        # Configurações para o menu de Jogador vs Jogador (e talvez IA se for tempo)
        self.selected_time_control = "classic"
        self.time_controls = ["classic", "rapid", "blitz", "bullet"]

        # Variáveis para a tela de carregamento de jogos
        self.saved_games = {} # Será preenchido ao entrar na tela de load
        self.scroll_offset = 0 # Para rolagem da lista de saves
        self.item_height = 60 # Altura de cada item na lista de saves

        self.run() # Inicia o loop principal do menu

    def run(self):
        running = True
        while running:
            self.screen_width, self.screen_height = self.screen.get_size() # Atualiza as dimensões da tela
            self._handle_events()
            self._draw_screen()
            pygame.display.flip()
            pygame.time.Clock().tick(60)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Botão esquerdo do mouse
                    self._handle_click(event.pos)
                elif event.button == 4: # Roda do mouse para cima
                    if self.current_state == 'load_game_menu':
                        self.scroll_offset = max(0, self.scroll_offset - self.item_height)
                elif event.button == 5: # Roda do mouse para baixo
                    if self.current_state == 'load_game_menu':
                        total_height = len(self.saved_games) * self.item_height
                        display_area_height = self.screen_height - 180 # Ajuste para o botão "Voltar"
                        max_scroll = max(0, total_height - display_area_height)
                        self.scroll_offset = min(max_scroll, self.scroll_offset + self.item_height)

    def _handle_click(self, pos):
        if self.current_state == 'main_menu':
            if self.pvp_button_rect.collidepoint(pos):
                self.current_state = 'pvp_setup_menu'
            elif self.pvai_button_rect.collidepoint(pos):
                self.current_state = 'pvai_setup_menu'
            elif self.load_game_button_rect.collidepoint(pos):
                self.current_state = 'load_game_menu'
                self.saved_games = self.save_manager.load_all_saves() # Carrega os saves ao entrar no menu
                self.scroll_offset = 0 # Reseta a rolagem
            elif self.settings_button_rect.collidepoint(pos):
                self._run_settings() # Placeholder para futuras configurações
            elif self.exit_button_rect.collidepoint(pos):
                pygame.quit()
                sys.exit()
        elif self.current_state == 'pvp_setup_menu':
            # Lógica para botões de seleção de controle de tempo (PvP)
            for i, control in enumerate(self.time_controls):
                rect = self._get_time_control_button_rect(i)
                if rect.collidepoint(pos):
                    self.selected_time_control = control

            if self.start_game_button_rect.collidepoint(pos):
                self._start_pvp_game()
            elif self.back_button_rect.collidepoint(pos):
                self.current_state = 'main_menu'
        elif self.current_state == 'pvai_setup_menu':
            # Lógica para botões de seleção de IA (PvAI)
            for i, mode in enumerate(self.ai_modes):
                rect = self._get_ai_mode_button_rect(i)
                if rect.collidepoint(pos):
                    self.selected_ai_mode = mode

            if self.start_game_button_rect.collidepoint(pos):
                self._start_pvai_game()
            elif self.back_button_rect.collidepoint(pos):
                self.current_state = 'main_menu'
        elif self.current_state == 'load_game_menu':
            self._handle_load_game_click(pos)

    def _handle_load_game_click(self, pos):
        # Botão Voltar
        if self.back_button_rect_load.collidepoint(pos):
            self.current_state = 'main_menu'
            return

        # Lógica para botões de carregamento de jogo
        y_offset = 100 - self.scroll_offset # Posição inicial da lista ajustada pela rolagem
        for name, data in self.saved_games.items():
            button_rect = pygame.Rect(
                (self.screen_width - 400) // 2, y_offset, 400, self.item_height - 10
            )
            # Verifica se o botão está visível na tela antes de verificar o clique
            if button_rect.collidepoint(pos) and y_offset >= 100 and y_offset < self.screen_height - 80:
                self._load_saved_game(name, data)
                return # Sai após carregar o jogo
            y_offset += self.item_height # Incrementa para o próximo item

    def _draw_screen(self):
        self.screen.fill((30, 30, 30)) # Fundo escuro para todas as telas

        if self.current_state == 'main_menu':
            self._draw_main_menu()
        elif self.current_state == 'pvp_setup_menu':
            self._draw_pvp_setup_menu()
        elif self.current_state == 'pvai_setup_menu':
            self._draw_pvai_setup_menu()
        elif self.current_state == 'load_game_menu':
            self._draw_load_game_menu()
        # elif self.current_state == 'settings_menu':
        #     self._draw_settings_menu() # Para futuras implementações

    def _draw_main_menu(self):
        title_text = self.big_font.render("AI Chess Game", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        self.screen.blit(title_text, title_rect)

        button_width = 250
        button_height = 60
        spacing = 20
        start_y = self.screen_height // 2 - (button_height * 2.5 + spacing * 2) / 2 # Ajuste para 4 botões

        # Player vs Player Button
        self.pvp_button_rect = pygame.Rect(
            (self.screen_width - button_width) // 2, start_y, button_width, button_height
        )
        self._draw_button(self.pvp_button_rect, "Jogador vs Jogador")

        # Player vs AI Button
        self.pvai_button_rect = pygame.Rect(
            (self.screen_width - button_width) // 2, self.pvp_button_rect.bottom + spacing, button_width, button_height
        )
        self._draw_button(self.pvai_button_rect, "Jogador vs IA")

        # Load Game Button
        self.load_game_button_rect = pygame.Rect(
            (self.screen_width - button_width) // 2, self.pvai_button_rect.bottom + spacing, button_width, button_height
        )
        self._draw_button(self.load_game_button_rect, "Carregar Jogo")

        # Settings Button
        self.settings_button_rect = pygame.Rect(
            (self.screen_width - button_width) // 2, self.load_game_button_rect.bottom + spacing, button_width, button_height
        )
        self._draw_button(self.settings_button_rect, "Configurações")

        # Exit Button
        self.exit_button_rect = pygame.Rect(
            (self.screen_width - button_width) // 2, self.settings_button_rect.bottom + spacing, button_width, button_height
        )
        self._draw_button(self.exit_button_rect, "Sair")

    def _draw_pvp_setup_menu(self):
        title_text = self.big_font.render("Jogador vs Jogador", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(title_text, title_rect)

        # Time Control Selection
        time_label = self.font.render("Selecione o Controle de Tempo:", True, self.WHITE)
        self.screen.blit(time_label, (self.screen_width // 2 - 200, 150))
        for i, control in enumerate(self.time_controls):
            rect = self._get_time_control_button_rect(i)
            self._draw_button(rect, control, self.selected_time_control == control)

        # Start Game Button
        self.start_game_button_rect = pygame.Rect(
            (self.screen_width - 200) // 2, self.screen_height - 150, 200, 60
        )
        self._draw_button(self.start_game_button_rect, "Iniciar Partida")

        # Back Button
        self.back_button_rect = pygame.Rect(
            (self.screen_width - 200) // 2, self.screen_height - 80, 200, 60
        )
        self._draw_button(self.back_button_rect, "Voltar")

    def _draw_pvai_setup_menu(self):
        title_text = self.big_font.render("Jogador vs IA", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(title_text, title_rect)

        # AI Mode Selection
        ai_label = self.font.render("Selecione a Dificuldade da IA:", True, self.WHITE)
        self.screen.blit(ai_label, (self.screen_width // 2 - 200, 150))
        for i, mode in enumerate(self.ai_modes):
            rect = self._get_ai_mode_button_rect(i)
            self._draw_button(rect, mode, self.selected_ai_mode == mode)

        # Start Game Button
        self.start_game_button_rect = pygame.Rect(
            (self.screen_width - 200) // 2, self.screen_height - 150, 200, 60
        )
        self._draw_button(self.start_game_button_rect, "Iniciar Partida")

        # Back Button
        self.back_button_rect = pygame.Rect(
            (self.screen_width - 200) // 2, self.screen_height - 80, 200, 60
        )
        self._draw_button(self.back_button_rect, "Voltar")

    def _draw_load_game_menu(self):
        title_text = self.big_font.render("Carregar Jogo", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(title_text, title_rect)

        # Desenha a lista de jogos salvos
        display_area_start_y = 100
        display_area_height = self.screen_height - 180 # Ajuste para o botão "Voltar"
        
        # Cria uma superfície temporária para desenhar os itens roláveis
        temp_surface = pygame.Surface((self.screen_width, max(display_area_height, len(self.saved_games) * self.item_height)), pygame.SRCALPHA)
        temp_surface.fill((0,0,0,0)) # Transparente

        y_offset_in_temp = 0
        if not self.saved_games:
            no_saves_text = self.font.render("Nenhum jogo salvo.", True, self.GRAY)
            no_saves_rect = no_saves_text.get_rect(center=(self.screen_width // 2, display_area_height // 2))
            temp_surface.blit(no_saves_text, no_saves_rect)
        else:
            for name, data in self.saved_games.items():
                item_rect = pygame.Rect(
                    (self.screen_width - 400) // 2, y_offset_in_temp, 400, self.item_height - 10
                )
                self._draw_button_on_surface(temp_surface, item_rect, name)
                y_offset_in_temp += self.item_height
            
        # Blit a superfície temporária na tela, aplicando o scroll_offset
        self.screen.blit(temp_surface, (0, display_area_start_y - self.scroll_offset))


        # Botão Voltar
        self.back_button_rect_load = pygame.Rect(
            (self.screen_width - 200) // 2, self.screen_height - 80, 200, 60
        )
        self._draw_button(self.back_button_rect_load, "Voltar")


    def _draw_button(self, rect, text, selected=False):
        color = self.DARK_BLUE if selected else self.BLUE
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            color = self.BLUE if selected else self.DARK_BLUE # Inverte as cores no hover
        
        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        label = self.font.render(text, True, self.WHITE)
        label_rect = label.get_rect(center=rect.center)
        self.screen.blit(label, label_rect)

    def _draw_button_on_surface(self, surface, rect, text, selected=False):
        color = self.DARK_BLUE if selected else self.BLUE
        # Não verifica mouse_pos aqui, pois é uma superfície temporária
        
        pygame.draw.rect(surface, color, rect, border_radius=12)
        label = self.font.render(text, True, self.WHITE)
        label_rect = label.get_rect(center=rect.center)
        surface.blit(label, label_rect)


    def _get_ai_mode_button_rect(self, index):
        button_width = 150
        button_height = 50
        spacing = 10
        x_start = self.screen_width // 2 - (len(self.ai_modes) * (button_width + spacing) - spacing) // 2
        return pygame.Rect(x_start + index * (button_width + spacing), 200, button_width, button_height)

    def _get_time_control_button_rect(self, index):
        button_width = 150
        button_height = 50
        spacing = 10
        x_start = self.screen_width // 2 - (len(self.time_controls) * (button_width + spacing) - spacing) // 2
        return pygame.Rect(x_start + index * (button_width + spacing), 200, button_width, button_height)

    def _start_pvp_game(self):
        # Inicia um jogo Jogador vs Jogador
        print(f"DEBUG: Starting PvP game with time control: {self.selected_time_control}")
        main(self.FEN, True, None, self.selected_time_control, None, None, loaded_save_name=None)
        self.current_state = 'main_menu' # Volta para o menu principal após a partida

    def _start_pvai_game(self):
        # Inicia um jogo Jogador vs IA
        config = self.load_config_from_main()
        skill_level = config["skill_level"]
        thinking_time = config["thinking_time"]
        print(f"DEBUG: Starting PvAI game with AI: {self.selected_ai_mode}, Skill: {skill_level}, Time: {thinking_time}")
        main(self.FEN, False, self.selected_ai_mode, None, None, None, loaded_save_name=None)
        self.current_state = 'main_menu' # Volta para o menu principal após a partida

    def _load_saved_game(self, save_name, save_data):
        print(f"DEBUG: _load_saved_game called. Loading save: {save_name}")
        FEN = save_data.get("FEN", self.FEN)
        local = save_data.get("local", False)
        ai_type = save_data.get("ai_type", None)
        skill_level = save_data.get("skill_level", None)
        thinking_time = save_data.get("thinking_time", None)
        time_control = save_data.get("time_control", None)
        white_time_left = save_data.get("white_time_left", None)
        black_time_left = save_data.get("black_time_left", None)

        main(FEN, local, ai_type, time_control, white_time_left, black_time_left, loaded_save_name=save_name)
        self.current_state = 'main_menu' # Volta para o menu principal após a partida

    def _run_settings(self):
        print("Abrindo configurações...")
        # self.current_state = 'settings_menu' # Para futuras implementações
        pass

    def load_config_from_main(self):
        from src.main import load_config as main_load_config
        return main_load_config()


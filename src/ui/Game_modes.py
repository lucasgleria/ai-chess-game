# # import pygame
# # import ctypes
# # import sys

# # class GameModes():

# #     def __init__(self):
# #         pygame.init()

# #         self.info = pygame.display.Info()
# #         self.screen_width, self.screen_height = self.info.current_w, self.info.current_h
# #         self.FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# #         # Create a resizable window the size of the screen
# #         self.screen = pygame.display.set_mode((self.screen_width, self.screen_height - 10), pygame.RESIZABLE)
# #         ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], 3)
# #         pygame.display.set_caption("AI Chess Game")

# #         self.font = pygame.font.SysFont(None, 36)

# #         self.WHITE = (255, 255, 255)
# #         self.BLUE = (70, 130, 180)
# #         self.DARK_BLUE = (40, 100, 160)

# #     def GameModes_windows(self, main_function_ref): # Adicionado main_function_ref como argumento
# #         # A função New_Game agora receberá a referência para a função main
# #         def New_Game(FEN, local):
# #             main_function_ref(FEN, local) # Usa a função passada como argumento

# #         self.running = True
# #         while self.running:
# #             for event in pygame.event.get():
# #                 if event.type == pygame.QUIT:
# #                     self.running = False

# #                 elif event.type == pygame.VIDEORESIZE:
# #                     self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

# #                 elif event.type == pygame.MOUSEBUTTONDOWN:
# #                     if self.button_rect.collidepoint(event.pos):
# #                         self.local = False
# #                         New_Game(self.FEN, self.local)

# #                     if self.button_rect2.collidepoint(event.pos):
# #                         self.local = True
# #                         New_Game(self.FEN, self.local)

# #             self.screen_width = self.screen.get_width()
# #             self.screen_height = self.screen.get_height()

# #             self.button_width = 180
# #             self.button_height = 70
# #             self.spacing = 30

# #             self.total_height = 2 * self.button_height + self.spacing
# #             self.start_y = (self.screen_height - self.total_height) // 2
# #             self.button_x = (self.screen_width - self.button_width) // 2

# #             self.button_rect = pygame.Rect(self.button_x, self.start_y, self.button_width, self.button_height)# AI VS player
# #             self.button_rect2 = pygame.Rect(self.button_x - 10, self.start_y + self.button_height + self.spacing, self.button_width + 20, self.button_height)# Local_multiplayer

# #             self.screen.fill(self.WHITE)

# #             self.mouse_pos = pygame.mouse.get_pos()

# #             if self.button_rect.collidepoint(self.mouse_pos):
# #                 self.color = self.DARK_BLUE
# #             else:
# #                 self.color = self.BLUE

# #             if self.button_rect2.collidepoint(self.mouse_pos):
# #                 self.color2 = self.DARK_BLUE
# #             else:
# #                 self.color2 = self.BLUE

# #             pygame.draw.rect(self.screen, self.color, self.button_rect, border_radius=12)
# #             pygame.draw.rect(self.screen, self.color2, self.button_rect2, border_radius=12)

# #             self.text_surface = self.font.render("AI VS Player", True, self.WHITE)
# #             self.text_rect = self.text_surface.get_rect(center=self.button_rect.center)
# #             self.screen.blit(self.text_surface, self.text_rect)

# #             self.text_surface2 = self.font.render("Player VS Player", True, self.WHITE)
# #             self.text_rect2 = self.text_surface2.get_rect(center=self.button_rect2.center)
# #             self.screen.blit(self.text_surface2, self.text_rect2)

# #             pygame.display.flip()

# #         pygame.quit()
# #         sys.exit()


# import pygame
# import ctypes
# import sys

# class GameModes():

#     def __init__(self):
#         pygame.init()

#         self.info = pygame.display.Info()
#         self.screen_width, self.screen_height = self.info.current_w, self.info.current_h
#         self.FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

#         # Define a tela inicial
#         self.current_screen = 'main_menu' # 'main_menu' ou 'ai_difficulty_selection'

#         # Cria uma janela redimensionável do tamanho da tela
#         self.screen = pygame.display.set_mode((self.screen_width, self.screen_height - 10), pygame.RESIZABLE)
#         ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], 3)
#         pygame.display.set_caption("AI Chess Game")

#         self.font = pygame.font.SysFont(None, 36)
#         self.small_font = pygame.font.SysFont(None, 28) # Fonte menor para botões

#         self.WHITE = (255, 255, 255)
#         self.BLUE = (70, 130, 180)
#         self.DARK_BLUE = (40, 100, 160)

#     def GameModes_windows(self, main_function_ref): # Agora recebe main_function_ref
#         # Função interna para iniciar o jogo
#         def New_Game(FEN, local, ai_type=None): # Adicionado ai_type
#             main_function_ref(FEN, local, ai_type) # Usa a função passada como argumento

#         self.running = True
#         while self.running:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     self.running = False
#                     pygame.quit()
#                     sys.exit()

#                 elif event.type == pygame.VIDEORESIZE:
#                     self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
#                     self.screen_width, self.screen_height = event.w, event.h

#                 elif event.type == pygame.MOUSEBUTTONDOWN:
#                     if self.current_screen == 'main_menu':
#                         if self.button_ai_vs_player_rect.collidepoint(event.pos):
#                             self.current_screen = 'ai_difficulty_selection' # Mudar para tela de dificuldade
#                         elif self.button_player_vs_player_rect.collidepoint(event.pos):
#                             New_Game(self.FEN, True) # Inicia Player vs Player
#                     elif self.current_screen == 'ai_difficulty_selection':
#                         if self.button_easy_rect.collidepoint(event.pos):
#                             New_Game(self.FEN, False, 'easy')
#                         elif self.button_medium_rect.collidepoint(event.pos):
#                             New_Game(self.FEN, False, 'medium')
#                         elif self.button_stockfish_rect.collidepoint(event.pos):
#                             New_Game(self.FEN, False, 'stockfish')
#                         elif self.button_back_rect.collidepoint(event.pos):
#                             self.current_screen = 'main_menu' # Voltar ao menu principal

#             self.screen_width = self.screen.get_width()
#             self.screen_height = self.screen.get_height()

#             self.screen.fill(self.WHITE) # Limpa a tela

#             if self.current_screen == 'main_menu':
#                 self._draw_main_menu()
#             elif self.current_screen == 'ai_difficulty_selection':
#                 self._draw_ai_difficulty_menu()

#             pygame.display.flip()

#         pygame.quit()
#         sys.exit()

#     def _draw_main_menu(self):
#         # Configurações de botões para o menu principal
#         button_width = 180
#         button_height = 70
#         spacing = 30
#         total_height = 2 * button_height + spacing
#         start_y = (self.screen_height - total_height) // 2
#         button_x = (self.screen_width - button_width) // 2

#         self.button_ai_vs_player_rect = pygame.Rect(button_x, start_y, button_width, button_height)
#         self.button_player_vs_player_rect = pygame.Rect(button_x - 10, start_y + button_height + spacing, button_width + 20, button_height)

#         mouse_pos = pygame.mouse.get_pos()

#         # Desenha botões do menu principal
#         color_ai_vs_player = self.DARK_BLUE if self.button_ai_vs_player_rect.collidepoint(mouse_pos) else self.BLUE
#         color_player_vs_player = self.DARK_BLUE if self.button_player_vs_player_rect.collidepoint(mouse_pos) else self.BLUE

#         pygame.draw.rect(self.screen, color_ai_vs_player, self.button_ai_vs_player_rect, border_radius=12)
#         pygame.draw.rect(self.screen, color_player_vs_player, self.button_player_vs_player_rect, border_radius=12)

#         text_surface_ai_vs_player = self.font.render("IA VS Jogador", True, self.WHITE)
#         text_rect_ai_vs_player = text_surface_ai_vs_player.get_rect(center=self.button_ai_vs_player_rect.center)
#         self.screen.blit(text_surface_ai_vs_player, text_rect_ai_vs_player)

#         text_surface_player_vs_player = self.font.render("Jogador VS Jogador", True, self.WHITE)
#         text_rect_player_vs_player = text_surface_player_vs_player.get_rect(center=self.button_player_vs_player_rect.center)
#         self.screen.blit(text_surface_player_vs_player, text_rect_player_vs_player)

#     def _draw_ai_difficulty_menu(self):
#         # Configurações de botões para a seleção de dificuldade
#         button_width = 200
#         button_height = 60
#         spacing = 20
#         total_height = 3 * button_height + 2 * spacing + 50 # +50 para o botão Voltar
#         start_y = (self.screen_height - total_height) // 2
#         button_x = (self.screen_width - button_width) // 2

#         # Título
#         title_surface = self.font.render("Escolha a Dificuldade da IA", True, (50, 50, 50))
#         title_rect = title_surface.get_rect(center=(self.screen_width // 2, start_y - 40))
#         self.screen.blit(title_surface, title_rect)

#         self.button_easy_rect = pygame.Rect(button_x, start_y, button_width, button_height)
#         self.button_medium_rect = pygame.Rect(button_x, start_y + button_height + spacing, button_width, button_height)
#         self.button_stockfish_rect = pygame.Rect(button_x, start_y + 2 * (button_height + spacing), button_width, button_height)

#         # Botão Voltar
#         self.button_back_rect = pygame.Rect(button_x, self.button_stockfish_rect.bottom + spacing * 1.5, button_width, button_height)


#         mouse_pos = pygame.mouse.get_pos()

#         # Desenha botões de dificuldade
#         color_easy = self.DARK_BLUE if self.button_easy_rect.collidepoint(mouse_pos) else self.BLUE
#         color_medium = self.DARK_BLUE if self.button_medium_rect.collidepoint(mouse_pos) else self.BLUE
#         color_stockfish = self.DARK_BLUE if self.button_stockfish_rect.collidepoint(mouse_pos) else self.BLUE
#         color_back = self.DARK_BLUE if self.button_back_rect.collidepoint(mouse_pos) else self.BLUE


#         pygame.draw.rect(self.screen, color_easy, self.button_easy_rect, border_radius=12)
#         pygame.draw.rect(self.screen, color_medium, self.button_medium_rect, border_radius=12)
#         pygame.draw.rect(self.screen, color_stockfish, self.button_stockfish_rect, border_radius=12)
#         pygame.draw.rect(self.screen, color_back, self.button_back_rect, border_radius=12)


#         text_surface_easy = self.font.render("Fácil", True, self.WHITE)
#         text_rect_easy = text_surface_easy.get_rect(center=self.button_easy_rect.center)
#         self.screen.blit(text_surface_easy, text_rect_easy)

#         text_surface_medium = self.font.render("Médio", True, self.WHITE)
#         text_rect_medium = text_surface_medium.get_rect(center=self.button_medium_rect.center)
#         self.screen.blit(text_surface_medium, text_rect_medium)

#         text_surface_stockfish = self.font.render("Stockfish", True, self.WHITE)
#         text_rect_stockfish = text_surface_stockfish.get_rect(center=self.button_stockfish_rect.center)
#         self.screen.blit(text_surface_stockfish, text_rect_stockfish)

#         text_surface_back = self.small_font.render("Voltar", True, self.WHITE)
#         text_rect_back = text_surface_back.get_rect(center=self.button_back_rect.center)
#         self.screen.blit(text_surface_back, text_rect_back)


import pygame
import ctypes
import sys
# REMOVIDO: from src.main import main # Esta linha causava a importação circular!

class GameModes():

    def __init__(self):
        pygame.init()

        self.info = pygame.display.Info()
        self.screen_width, self.screen_height = self.info.current_w, self.info.current_h
        self.FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        # Define a tela inicial
        self.current_screen = 'main_menu' # 'main_menu', 'ai_difficulty_selection' ou 'time_control_selection'

        # Cria uma janela redimensionável do tamanho da tela
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height - 10), pygame.RESIZABLE)
        ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], 3)
        pygame.display.set_caption("AI Chess Game")

        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 28) # Fonte menor para botões

        self.WHITE = (255, 255, 255)
        self.BLUE = (70, 130, 180)
        self.DARK_BLUE = (40, 100, 160)

    def GameModes_windows(self, main_function_ref): # Agora recebe main_function_ref
        # Função interna para iniciar o jogo
        # Adicionado time_control como argumento
        def New_Game(FEN, local, ai_type=None, time_control=None):
            main_function_ref(FEN, local, ai_type, time_control) # Passa time_control para a função main

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.screen_width, self.screen_height = event.w, event.h

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_screen == 'main_menu':
                        if self.button_ai_vs_player_rect.collidepoint(event.pos):
                            self.current_screen = 'ai_difficulty_selection' # Mudar para tela de dificuldade
                        elif self.button_player_vs_player_rect.collidepoint(event.pos):
                            self.current_screen = 'time_control_selection' # Mudar para tela de controle de tempo
                    elif self.current_screen == 'ai_difficulty_selection':
                        if self.button_easy_rect.collidepoint(event.pos):
                            New_Game(self.FEN, False, 'easy')
                        elif self.button_medium_rect.collidepoint(event.pos):
                            New_Game(self.FEN, False, 'medium')
                        elif self.button_stockfish_rect.collidepoint(event.pos):
                            New_Game(self.FEN, False, 'stockfish')
                        elif self.button_back_rect.collidepoint(event.pos):
                            self.current_screen = 'main_menu' # Voltar ao menu principal
                    elif self.current_screen == 'time_control_selection':
                        if self.button_classic_rect.collidepoint(event.pos):
                            New_Game(self.FEN, True, None, 'classic')
                        elif self.button_rapid_rect.collidepoint(event.pos):
                            New_Game(self.FEN, True, None, 'rapid')
                        elif self.button_blitz_rect.collidepoint(event.pos):
                            New_Game(self.FEN, True, None, 'blitz')
                        elif self.button_bullet_rect.collidepoint(event.pos):
                            New_Game(self.FEN, True, None, 'bullet')
                        elif self.button_back_time_rect.collidepoint(event.pos):
                            self.current_screen = 'main_menu' # Voltar ao menu principal

            self.screen_width = self.screen.get_width()
            self.screen_height = self.screen.get_height()

            self.screen.fill(self.WHITE) # Limpa a tela

            if self.current_screen == 'main_menu':
                self._draw_main_menu()
            elif self.current_screen == 'ai_difficulty_selection':
                self._draw_ai_difficulty_menu()
            elif self.current_screen == 'time_control_selection':
                self._draw_time_control_menu()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def _draw_main_menu(self):
        # Configurações de botões para o menu principal
        button_width = 180
        button_height = 70
        spacing = 30
        total_height = 2 * button_height + spacing
        start_y = (self.screen_height - total_height) // 2
        button_x = (self.screen_width - button_width) // 2

        self.button_ai_vs_player_rect = pygame.Rect(button_x, start_y, button_width, button_height)
        self.button_player_vs_player_rect = pygame.Rect(button_x - 10, start_y + button_height + spacing, button_width + 20, button_height)

        mouse_pos = pygame.mouse.get_pos()

        # Desenha botões do menu principal
        color_ai_vs_player = self.DARK_BLUE if self.button_ai_vs_player_rect.collidepoint(mouse_pos) else self.BLUE
        color_player_vs_player = self.DARK_BLUE if self.button_player_vs_player_rect.collidepoint(mouse_pos) else self.BLUE

        pygame.draw.rect(self.screen, color_ai_vs_player, self.button_ai_vs_player_rect, border_radius=12)
        pygame.draw.rect(self.screen, color_player_vs_player, self.button_player_vs_player_rect, border_radius=12)

        text_surface_ai_vs_player = self.font.render("IA VS Jogador", True, self.WHITE)
        text_rect_ai_vs_player = text_surface_ai_vs_player.get_rect(center=self.button_ai_vs_player_rect.center)
        self.screen.blit(text_surface_ai_vs_player, text_rect_ai_vs_player)

        text_surface_player_vs_player = self.font.render("Jogador VS Jogador", True, self.WHITE)
        text_rect_player_vs_player = text_surface_player_vs_player.get_rect(center=self.button_player_vs_player_rect.center)
        self.screen.blit(text_surface_player_vs_player, text_rect_player_vs_player)

    def _draw_ai_difficulty_menu(self):
        # Configurações de botões para a seleção de dificuldade
        button_width = 200
        button_height = 60
        spacing = 20
        total_height = 3 * button_height + 2 * spacing + 50 # +50 para o botão Voltar
        start_y = (self.screen_height - total_height) // 2
        button_x = (self.screen_width - button_width) // 2

        # Título
        title_surface = self.font.render("Escolha a Dificuldade da IA", True, (50, 50, 50))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, start_y - 40))
        self.screen.blit(title_surface, title_rect)

        self.button_easy_rect = pygame.Rect(button_x, start_y, button_width, button_height)
        self.button_medium_rect = pygame.Rect(button_x, start_y + button_height + spacing, button_width, button_height)
        self.button_stockfish_rect = pygame.Rect(button_x, start_y + 2 * (button_height + spacing), button_width, button_height)

        # Botão Voltar
        self.button_back_rect = pygame.Rect(button_x, self.button_stockfish_rect.bottom + spacing * 1.5, button_width, button_height)


        mouse_pos = pygame.mouse.get_pos()

        # Desenha botões de dificuldade
        color_easy = self.DARK_BLUE if self.button_easy_rect.collidepoint(mouse_pos) else self.BLUE
        color_medium = self.DARK_BLUE if self.button_medium_rect.collidepoint(mouse_pos) else self.BLUE
        color_stockfish = self.DARK_BLUE if self.button_stockfish_rect.collidepoint(mouse_pos) else self.BLUE
        color_back = self.DARK_BLUE if self.button_back_rect.collidepoint(mouse_pos) else self.BLUE


        pygame.draw.rect(self.screen, color_easy, self.button_easy_rect, border_radius=12)
        pygame.draw.rect(self.screen, color_medium, self.button_medium_rect, border_radius=12)
        pygame.draw.rect(self.screen, color_stockfish, self.button_stockfish_rect, border_radius=12)
        pygame.draw.rect(self.screen, color_back, self.button_back_rect, border_radius=12)


        text_surface_easy = self.font.render("Fácil", True, self.WHITE)
        text_rect_easy = text_surface_easy.get_rect(center=self.button_easy_rect.center)
        self.screen.blit(text_surface_easy, text_rect_easy)

        text_surface_medium = self.font.render("Médio", True, self.WHITE)
        text_rect_medium = text_surface_medium.get_rect(center=self.button_medium_rect.center)
        self.screen.blit(text_surface_medium, text_rect_medium)

        text_surface_stockfish = self.font.render("Stockfish", True, self.WHITE)
        text_rect_stockfish = text_surface_stockfish.get_rect(center=self.button_stockfish_rect.center)
        self.screen.blit(text_surface_stockfish, text_rect_stockfish)

        text_surface_back = self.small_font.render("Voltar", True, self.WHITE)
        text_rect_back = text_surface_back.get_rect(center=self.button_back_rect.center)
        self.screen.blit(text_surface_back, text_rect_back)

    def _draw_time_control_menu(self):
        # Configurações de botões para a seleção de controle de tempo
        button_width = 200
        button_height = 60
        spacing = 20
        total_height = 4 * button_height + 3 * spacing + 50 # +50 para o botão Voltar
        start_y = (self.screen_height - total_height) // 2
        button_x = (self.screen_width - button_width) // 2

        # Título
        title_surface = self.font.render("Escolha o Controle de Tempo", True, (50, 50, 50))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, start_y - 40))
        self.screen.blit(title_surface, title_rect)

        self.button_classic_rect = pygame.Rect(button_x, start_y, button_width, button_height)
        self.button_rapid_rect = pygame.Rect(button_x, start_y + button_height + spacing, button_width, button_height)
        self.button_blitz_rect = pygame.Rect(button_x, start_y + 2 * (button_height + spacing), button_width, button_height)
        self.button_bullet_rect = pygame.Rect(button_x, start_y + 3 * (button_height + spacing), button_width, button_height)

        # Botão Voltar
        self.button_back_time_rect = pygame.Rect(button_x, self.button_bullet_rect.bottom + spacing * 1.5, button_width, button_height)

        mouse_pos = pygame.mouse.get_pos()

        # Desenha botões de controle de tempo
        color_classic = self.DARK_BLUE if self.button_classic_rect.collidepoint(mouse_pos) else self.BLUE
        color_rapid = self.DARK_BLUE if self.button_rapid_rect.collidepoint(mouse_pos) else self.BLUE
        color_blitz = self.DARK_BLUE if self.button_blitz_rect.collidepoint(mouse_pos) else self.BLUE
        color_bullet = self.DARK_BLUE if self.button_bullet_rect.collidepoint(mouse_pos) else self.BLUE
        color_back_time = self.DARK_BLUE if self.button_back_time_rect.collidepoint(mouse_pos) else self.BLUE

        pygame.draw.rect(self.screen, color_classic, self.button_classic_rect, border_radius=12)
        pygame.draw.rect(self.screen, color_rapid, self.button_rapid_rect, border_radius=12)
        pygame.draw.rect(self.screen, color_blitz, self.button_blitz_rect, border_radius=12)
        pygame.draw.rect(self.screen, color_bullet, self.button_bullet_rect, border_radius=12)
        pygame.draw.rect(self.screen, color_back_time, self.button_back_time_rect, border_radius=12)

        text_surface_classic = self.font.render("Clássico", True, self.WHITE)
        text_rect_classic = text_surface_classic.get_rect(center=self.button_classic_rect.center)
        self.screen.blit(text_surface_classic, text_rect_classic)

        text_surface_rapid = self.font.render("Rápido", True, self.WHITE)
        text_rect_rapid = text_surface_rapid.get_rect(center=self.button_rapid_rect.center)
        self.screen.blit(text_surface_rapid, text_rect_rapid)

        text_surface_blitz = self.font.render("Blitz", True, self.WHITE)
        text_rect_blitz = text_surface_blitz.get_rect(center=self.button_blitz_rect.center)
        self.screen.blit(text_surface_blitz, text_rect_blitz)

        text_surface_bullet = self.font.render("Bullet", True, self.WHITE)
        text_rect_bullet = text_surface_bullet.get_rect(center=self.button_bullet_rect.center)
        self.screen.blit(text_surface_bullet, text_rect_bullet)

        text_surface_back_time = self.small_font.render("Voltar", True, self.WHITE)
        text_rect_back_time = text_surface_back_time.get_rect(center=self.button_back_time_rect.center)
        self.screen.blit(text_surface_back_time, text_rect_back_time)

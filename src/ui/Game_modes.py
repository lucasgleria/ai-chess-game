import pygame
import ctypes
import sys

class GameModes():

    def __init__(self):
        pygame.init()

        self.info = pygame.display.Info()
        self.screen_width, self.screen_height = self.info.current_w, self.info.current_h
        self.FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

        # Create a resizable window the size of the screen
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height - 10), pygame.RESIZABLE)
        ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()['window'], 3)
        pygame.display.set_caption("AI Chess Game")

        self.font = pygame.font.SysFont(None, 36)

        self.WHITE = (255, 255, 255)
        self.BLUE = (70, 130, 180)
        self.DARK_BLUE = (40, 100, 160)

    def GameModes_windows(self, main_function_ref): # Adicionado main_function_ref como argumento
        # A função New_Game agora receberá a referência para a função main
        def New_Game(FEN, local):
            main_function_ref(FEN, local) # Usa a função passada como argumento

        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_rect.collidepoint(event.pos):
                        self.local = False
                        New_Game(self.FEN, self.local)

                    if self.button_rect2.collidepoint(event.pos):
                        self.local = True
                        New_Game(self.FEN, self.local)

            self.screen_width = self.screen.get_width()
            self.screen_height = self.screen.get_height()

            self.button_width = 180
            self.button_height = 70
            self.spacing = 30

            self.total_height = 2 * self.button_height + self.spacing
            self.start_y = (self.screen_height - self.total_height) // 2
            self.button_x = (self.screen_width - self.button_width) // 2

            self.button_rect = pygame.Rect(self.button_x, self.start_y, self.button_width, self.button_height)# AI VS player
            self.button_rect2 = pygame.Rect(self.button_x - 10, self.start_y + self.button_height + self.spacing, self.button_width + 20, self.button_height)# Local_multiplayer

            self.screen.fill(self.WHITE)

            self.mouse_pos = pygame.mouse.get_pos()

            if self.button_rect.collidepoint(self.mouse_pos):
                self.color = self.DARK_BLUE
            else:
                self.color = self.BLUE

            if self.button_rect2.collidepoint(self.mouse_pos):
                self.color2 = self.DARK_BLUE
            else:
                self.color2 = self.BLUE

            pygame.draw.rect(self.screen, self.color, self.button_rect, border_radius=12)
            pygame.draw.rect(self.screen, self.color2, self.button_rect2, border_radius=12)

            self.text_surface = self.font.render("AI VS Player", True, self.WHITE)
            self.text_rect = self.text_surface.get_rect(center=self.button_rect.center)
            self.screen.blit(self.text_surface, self.text_rect)

            self.text_surface2 = self.font.render("Player VS Player", True, self.WHITE)
            self.text_rect2 = self.text_surface2.get_rect(center=self.button_rect2.center)
            self.screen.blit(self.text_surface2, self.text_rect2)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

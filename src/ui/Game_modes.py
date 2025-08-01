import pygame
import sys
import chess
from src.main import main # Imports the main function from src/main.py
from src.data.save_manager import SaveManager # Imports the SaveManager

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

        # State variables to control which screen is active
        self.current_state = 'main_menu' # 'main_menu', 'pvp_setup_menu', 'pvai_setup_menu', 'load_game_menu', 'settings_menu'

        # Settings for Player vs AI menu
        self.selected_ai_mode = "stockfish"
        self.ai_modes = ["easy", "medium", "stockfish"] # Does not include "local_player" here

        # Settings for Player vs Player menu (and possibly AI if it's time-based)
        self.selected_time_control = "classic"
        self.time_controls = ["classic", "rapid", "blitz", "bullet"]

        # Variables for the game loading screen
        self.saved_games = {} # Will be populated when entering the load screen
        self.scroll_offset = 0 # For scrolling the list of saves
        self.item_height = 60 # Height of each item in the save list

        # List to store deletion button rectangles and their save names
        self.delete_buttons_rects = []
        self.delete_font = pygame.font.SysFont(None, 24, bold=True) # Font for the 'X'

        self.run() # Starts the main menu loop

    def run(self):
        running = True
        while running:
            self.screen_width, self.screen_height = self.screen.get_size() # Updates screen dimensions
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
                if event.button == 1: # Left mouse button
                    self._handle_click(event.pos)
                elif event.button == 4: # Mouse wheel up
                    if self.current_state == 'load_game_menu':
                        self.scroll_offset = max(0, self.scroll_offset - self.item_height)
                elif event.button == 5: # Mouse wheel down
                    if self.current_state == 'load_game_menu':
                        total_height = len(self.saved_games) * self.item_height
                        display_area_height = self.screen_height - 180 # Adjustment for the "Back" button
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
                self.saved_games = self.save_manager.load_all_saves() # Loads saves when entering the menu
                self.scroll_offset = 0 # Resets scrolling
            elif self.settings_button_rect.collidepoint(pos):
                self._run_settings() # Placeholder for future settings
            elif self.exit_button_rect.collidepoint(pos):
                pygame.quit()
                sys.exit()
        elif self.current_state == 'pvp_setup_menu':
            # Logic for time control selection buttons (PvP)
            for i, control in enumerate(self.time_controls):
                rect = self._get_time_control_button_rect(i)
                if rect.collidepoint(pos):
                    self.selected_time_control = control

            if self.start_game_button_rect.collidepoint(pos):
                self._start_pvp_game()
            elif self.back_button_rect.collidepoint(pos):
                self.current_state = 'main_menu'
        elif self.current_state == 'pvai_setup_menu':
            # Logic for AI selection buttons (PvAI)
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
        # Back Button
        if self.back_button_rect_load.collidepoint(pos):
            self.current_state = 'main_menu'
            return

        # Converts the click position to the internal coordinates of the temp_surface
        display_area_start_y = 100
        click_x_temp = pos[0]
        click_y_temp = pos[1] - (display_area_start_y - self.scroll_offset)
        click_pos_temp = (click_x_temp, click_y_temp)

        # Checks for clicks on delete buttons FIRST
        for delete_rect_temp, save_name_to_delete in self.delete_buttons_rects:
            # Calculates the actual Y position of the delete button on the screen to check visibility
            actual_delete_button_screen_y = display_area_start_y - self.scroll_offset + delete_rect_temp.y
            
            if (delete_rect_temp.collidepoint(click_pos_temp) and
                actual_delete_button_screen_y >= display_area_start_y and
                actual_delete_button_screen_y + delete_rect_temp.height <= (self.screen_height - 80)): # -80 for the "Back" button margin
                
                self.save_manager.delete_save(save_name_to_delete)
                self.saved_games = self.save_manager.load_all_saves() # Reloads saves
                self.scroll_offset = 0 # Resets scrolling
                return # Exits after handling deletion

        # Original logic for loading the game (if a save item itself is clicked)
        # This part will only be reached if no delete button was clicked
        y_offset = 100 - self.scroll_offset # Initial list position adjusted by scrolling
        for name, data in self.saved_games.items():
            button_rect = pygame.Rect(
                (self.screen_width - 400) // 2, y_offset, 400, self.item_height - 10
            )
            # Checks if the button is visible on the screen before checking the click
            if button_rect.collidepoint(pos) and y_offset >= 100 and y_offset < self.screen_height - 80:
                self._load_saved_game(name, data)
                return # Exits after loading the game
            y_offset += self.item_height # Increments for the next item

    def _draw_screen(self):
        self.screen.fill((30, 30, 30)) # Dark background for all screens

        if self.current_state == 'main_menu':
            self._draw_main_menu()
        elif self.current_state == 'pvp_setup_menu':
            self._draw_pvp_setup_menu()
        elif self.current_state == 'pvai_setup_menu':
            self._draw_pvai_setup_menu()
        elif self.current_state == 'load_game_menu':
            self._draw_load_game_menu()
        # elif self.current_state == 'settings_menu':
        #     self._draw_settings_menu() # For future implementations

    def _draw_main_menu(self):
        title_text = self.big_font.render("AI Chess Game", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        self.screen.blit(title_text, title_rect)

        button_width = 250
        button_height = 60
        spacing = 20
        start_y = self.screen_height // 2 - (button_height * 2.5 + spacing * 2) / 2 # Adjustment for 4 buttons

        # Player vs Player Button
        self.pvp_button_rect = pygame.Rect(
            (self.screen_width - button_width) // 2, start_y, button_width, button_height
        )
        self._draw_button(self.pvp_button_rect, "Player vs Player")

        # Player vs AI Button
        self.pvai_button_rect = pygame.Rect(
            (self.screen_width - button_width) // 2, self.pvp_button_rect.bottom + spacing, button_width, button_height
        )
        self._draw_button(self.pvai_button_rect, "Player vs AI")

        # Load Game Button
        self.load_game_button_rect = pygame.Rect(
            (self.screen_width - button_width) // 2, self.pvai_button_rect.bottom + spacing, button_width, button_height
        )
        self._draw_button(self.load_game_button_rect, "Load Game")

        # Settings Button
        self.settings_button_rect = pygame.Rect(
            (self.screen_width - button_width) // 2, self.load_game_button_rect.bottom + spacing, button_width, button_height
        )
        self._draw_button(self.settings_button_rect, "Settings")

        # Exit Button
        self.exit_button_rect = pygame.Rect(
            (self.screen_width - button_width) // 2, self.settings_button_rect.bottom + spacing, button_width, button_height
        )
        self._draw_button(self.exit_button_rect, "Exit")

    def _draw_pvp_setup_menu(self):
        title_text = self.big_font.render("Player vs Player", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(title_text, title_rect)

        # Time Control Selection
        time_label = self.font.render("Select Time Control:", True, self.WHITE)
        self.screen.blit(time_label, (self.screen_width // 2 - 200, 150))
        for i, control in enumerate(self.time_controls):
            rect = self._get_time_control_button_rect(i)
            self._draw_button(rect, control, self.selected_time_control == control)

        # Start Game Button
        self.start_game_button_rect = pygame.Rect(
            (self.screen_width - 200) // 2, self.screen_height - 150, 200, 60
        )
        self._draw_button(self.start_game_button_rect, "Start Game")

        # Back Button
        self.back_button_rect = pygame.Rect(
            (self.screen_width - 200) // 2, self.screen_height - 80, 200, 60
        )
        self._draw_button(self.back_button_rect, "Back")

    def _draw_pvai_setup_menu(self):
        title_text = self.big_font.render("Player vs AI", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(title_text, title_rect)

        # AI Mode Selection
        ai_label = self.font.render("Select AI Difficulty:", True, self.WHITE)
        self.screen.blit(ai_label, (self.screen_width // 2 - 200, 150))
        for i, mode in enumerate(self.ai_modes):
            rect = self._get_ai_mode_button_rect(i)
            self._draw_button(rect, mode, self.selected_ai_mode == mode)

        # Start Game Button
        self.start_game_button_rect = pygame.Rect(
            (self.screen_width - 200) // 2, self.screen_height - 150, 200, 60
        )
        self._draw_button(self.start_game_button_rect, "Start Game")

        # Back Button
        self.back_button_rect = pygame.Rect(
            (self.screen_width - 200) // 2, self.screen_height - 80, 200, 60
        )
        self._draw_button(self.back_button_rect, "Back")

    def _draw_load_game_menu(self):
        title_text = self.big_font.render("Load Game", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(title_text, title_rect)

        display_area_start_y = 100
        display_area_height = self.screen_height - 180
        
        temp_surface = pygame.Surface((self.screen_width, max(display_area_height, len(self.saved_games) * self.item_height)), pygame.SRCALPHA)
        temp_surface.fill((0,0,0,0))

        self.delete_buttons_rects = [] # Clears the list for this drawing cycle

        y_offset_in_temp = 0
        if not self.saved_games:
            no_saves_text = self.font.render("No games saved.", True, self.GRAY)
            no_saves_rect = no_saves_text.get_rect(center=(self.screen_width // 2, display_area_height // 2))
            temp_surface.blit(no_saves_text, no_saves_rect)
        else:
            for name, data in self.saved_games.items():
                item_rect_on_temp = pygame.Rect(
                    (self.screen_width - 400) // 2, y_offset_in_temp, 400, self.item_height - 10
                )
                self._draw_button_on_surface(temp_surface, item_rect_on_temp, name)

                # Draws the delete button on the temp_surface
                delete_button_size = 30
                delete_button_margin_x = 10
                delete_button_x_on_temp = item_rect_on_temp.right + delete_button_margin_x
                delete_button_y_on_temp = item_rect_on_temp.centery - (delete_button_size // 2)
                
                delete_button_rect_on_temp = pygame.Rect(delete_button_x_on_temp, delete_button_y_on_temp, delete_button_size, delete_button_size)

                pygame.draw.rect(temp_surface, self.RED, delete_button_rect_on_temp, border_radius=5)
                delete_text_surface = self.delete_font.render("X", True, self.WHITE)
                delete_text_rect = delete_text_surface.get_rect(center=delete_button_rect_on_temp.center)
                temp_surface.blit(delete_text_surface, delete_text_rect)

                # Stores the rectangle (relative to temp_surface) and the save name
                self.delete_buttons_rects.append((delete_button_rect_on_temp, name))

                y_offset_in_temp += self.item_height
            
        self.screen.blit(temp_surface, (0, display_area_start_y - self.scroll_offset))


        # Back Button
        self.back_button_rect_load = pygame.Rect(
            (self.screen_width - 200) // 2, self.screen_height - 80, 200, 60
        )
        self._draw_button(self.back_button_rect_load, "Back")


    def _draw_button(self, rect, text, selected=False):
        color = self.DARK_BLUE if selected else self.BLUE
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            color = self.BLUE if selected else self.DARK_BLUE # Inverts colors on hover
        
        pygame.draw.rect(self.screen, color, rect, border_radius=12)
        label = self.font.render(text, True, self.WHITE)
        label_rect = label.get_rect(center=rect.center)
        self.screen.blit(label, label_rect)

    def _draw_button_on_surface(self, surface, rect, text, selected=False):
        color = self.DARK_BLUE if selected else self.BLUE
        # Does not check mouse_pos here, as it's a temporary surface
        
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
        # Starts a Player vs Player game
        main(self.FEN, True, None, self.selected_time_control, None, None, loaded_save_name=None)
        self.current_state = 'main_menu' # Returns to the main menu after the game

    def _start_pvai_game(self):
        # Starts a Player vs AI game
        config = self.load_config_from_main()
        skill_level = config["skill_level"]
        thinking_time = config["thinking_time"]
        main(self.FEN, False, self.selected_ai_mode, None, None, None, loaded_save_name=None)
        self.current_state = 'main_menu' # Returns to the main menu after the game

    def _load_saved_game(self, save_name, save_data):
        FEN = save_data.get("FEN", self.FEN)
        local = save_data.get("local", False)
        ai_type = save_data.get("ai_type", None)
        skill_level = save_data.get("skill_level", None)
        thinking_time = save_data.get("thinking_time", None)
        time_control = save_data.get("time_control", None)
        white_time_left = save_data.get("white_time_left", None)
        black_time_left = save_data.get("black_time_left", None)

        main(FEN, local, ai_type, time_control, white_time_left, black_time_left, loaded_save_name=save_name)
        self.current_state = 'main_menu' # Returns to the main menu after the game

    def _run_settings(self):
        # self.current_state = 'settings_menu' # For future implementations
        pass

    def load_config_from_main(self):
        from src.main import load_config as main_load_config
        return main_load_config()
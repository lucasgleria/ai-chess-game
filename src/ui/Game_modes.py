import pygame
import sys
import chess
from src.main import main # Imports the main function from src/main.py
from src.data.Save_Manager import SaveManager # Imports the SaveManager
from src.utils import load_config

class GameModes:
    def __init__(self, screen, save_manager):
        self.screen = screen
        self.save_manager = save_manager

        self.screen_width, self.screen_height = self.screen.get_size()
        self.font = pygame.font.SysFont(None, 36)
        self.big_font = pygame.font.SysFont(None, 48)

        # Chess-themed colors with alternative themes
        self.WHITE = (255, 255, 255)
        self.CHESS_BROWN = (139, 69, 19)  # Dark brown for chess board
        self.CHESS_CREAM = (245, 245, 220)  # Light cream for chess board
        self.CHESS_GOLD = (255, 215, 0)  # Gold for highlights
        self.CHESS_SILVER = (192, 192, 192)  # Silver for secondary elements
        self.CHESS_DARK = (47, 79, 79)  # Dark slate gray
        self.CHESS_LIGHT = (240, 248, 255)  # Alice blue
        self.CHESS_BLACK = (25, 25, 25)  # Dark background
        self.CHESS_RED = (220, 20, 60)  # Crimson red for delete buttons
        self.CHESS_GREEN = (34, 139, 34)  # Forest green for success
        
        # Alternative color themes for future use
        self.ALT_GOLD = (218, 165, 32)  # Goldenrod
        self.ALT_SILVER = (169, 169, 169)  # Dark gray
        self.ALT_BLUE = (70, 130, 180)  # Steel blue
        self.ALT_PURPLE = (128, 0, 128)  # Purple

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
        display_area_start_y = 120  # Updated to match the new positioning
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
                
                # Confirm deletion with user
                if self._confirm_delete_save(save_name_to_delete):
                    self.save_manager.delete_save(save_name_to_delete)
                    self.saved_games = self.save_manager.load_all_saves() # Reloads saves
                    self.scroll_offset = 0 # Resets scrolling
                return # Exits after handling deletion

        # Original logic for loading the game (if a save item itself is clicked)
        # This part will only be reached if no delete button was clicked
        y_offset = 120 - self.scroll_offset # Initial list position adjusted by scrolling and new positioning
        for name, data in self.saved_games.items():
            button_rect = pygame.Rect(
                (self.screen_width - 450) // 2, y_offset, 450, self.item_height - 15
            )
            # Checks if the button is visible on the screen before checking the click
            if button_rect.collidepoint(pos) and y_offset >= 120 and y_offset < self.screen_height - 80:
                self._load_saved_game(name, data)
                return # Exits after loading the game
            y_offset += self.item_height + 5 # Increments for the next item with spacing

    def _draw_screen(self):
        # Draw chess-themed background
        self._draw_chess_background()
        
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

    def _draw_chess_background(self):
        """Draw a refined chess-themed background with subtle board pattern"""
        # Fill with dark background
        self.screen.fill(self.CHESS_BLACK)
        
        # Draw refined chess board pattern overlay with better transparency
        pattern_size = 80  # Increased pattern size for elegance
        for y in range(0, self.screen_height, pattern_size):
            for x in range(0, self.screen_width, pattern_size):
                # Use more subtle colors with better transparency
                color = self.CHESS_BROWN if (x + y) // pattern_size % 2 == 0 else self.CHESS_CREAM
                overlay = pygame.Surface((pattern_size, pattern_size), pygame.SRCALPHA)
                overlay.fill((*color, 20))  # Very subtle transparency
                self.screen.blit(overlay, (x, y))
        
        # Add subtle gradient overlay for depth
        gradient = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        for i in range(self.screen_height):
            alpha = int(5 * (i / self.screen_height))  # Very subtle gradient
            pygame.draw.line(gradient, (0, 0, 0, alpha), (0, i), (self.screen_width, i))
        self.screen.blit(gradient, (0, 0))

    def _draw_main_menu(self):
        # Draw decorative chess pieces at the top
        self._draw_chess_decorations()
        
        # Enhanced title with chess theme - Better positioning
        title_font = pygame.font.SysFont(None, 72, bold=True)
        title_text = title_font.render("AI Chess Game", True, self.CHESS_GOLD)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle - Better positioning
        subtitle_font = pygame.font.SysFont(None, 28)  # Slightly larger font
        subtitle_text = subtitle_font.render("Strategic Battle of Minds", True, self.CHESS_SILVER)
        subtitle_rect = subtitle_text.get_rect(center=(self.screen_width // 2, title_rect.bottom + 15))
        self.screen.blit(subtitle_text, subtitle_rect)

        # Improved button layout with better spacing
        button_width = 300  # Increased width for better proportions
        button_height = 75  # Increased height for better proportions
        spacing = 30        # Increased spacing between buttons
        start_y = self.screen_height // 2 - (button_height * 2.5 + spacing * 2) / 2

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
        self._draw_button(self.exit_button_rect, "Exit Game")

    def _draw_chess_decorations(self):
        """Draw enhanced decorative chess pieces with better positioning and effects"""
        piece_font = pygame.font.SysFont(None, 48)  # Adjusted font size for text
        pieces = ["KING", "QUEEN", "ROOK", "BISHOP", "KNIGHT", "PAWN"]
        colors = [self.CHESS_GOLD, self.CHESS_SILVER, self.CHESS_GOLD, self.CHESS_SILVER, self.CHESS_GOLD, self.CHESS_SILVER]
        
        # Draw pieces in a row at the top with improved spacing and positioning
        piece_spacing = 120  # Increased spacing for text elements
        start_x = (self.screen_width - (len(pieces) * piece_spacing)) // 2
        
        for i, (piece, color) in enumerate(zip(pieces, colors)):
            # Add subtle shadow effect for depth
            shadow_surface = piece_font.render(piece, True, (0, 0, 0, 100))
            shadow_rect = shadow_surface.get_rect(center=(start_x + i * piece_spacing + 2, 82))
            self.screen.blit(shadow_surface, shadow_rect)
            
            # Draw main piece text
            piece_surface = piece_font.render(piece, True, color)
            piece_rect = piece_surface.get_rect(center=(start_x + i * piece_spacing, 80))
            self.screen.blit(piece_surface, piece_rect)
            
            # Add subtle highlight effect
            highlight_surface = piece_font.render(piece, True, (255, 255, 255, 50))
            highlight_rect = highlight_surface.get_rect(center=(start_x + i * piece_spacing - 1, 78))
            self.screen.blit(highlight_surface, highlight_rect)

    def _draw_pvp_setup_menu(self):
        # Draw decorative elements
        self._draw_chess_decorations()
        
        title_text = self.big_font.render("Player vs Player", True, self.CHESS_GOLD)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(title_text, title_rect)

        # Time Control Selection - Improved spacing and positioning
        time_label = self.font.render("Select Time Control:", True, self.CHESS_SILVER)
        time_label_rect = time_label.get_rect(center=(self.screen_width // 2, 150))
        self.screen.blit(time_label, time_label_rect)
        
        # Improved button positioning with better spacing
        for i, control in enumerate(self.time_controls):
            rect = self._get_time_control_button_rect(i)
            self._draw_button(rect, f"{control.title()}", self.selected_time_control == control)

        # Start Game Button - Better positioned
        self.start_game_button_rect = pygame.Rect(
            (self.screen_width - 250) // 2, self.screen_height - 150, 250, 70
        )
        self._draw_button(self.start_game_button_rect, "Start Game")

        # Back Button - Better positioned
        self.back_button_rect = pygame.Rect(
            (self.screen_width - 200) // 2, self.screen_height - 80, 200, 60
        )
        self._draw_button(self.back_button_rect, "Back")

    def _draw_pvai_setup_menu(self):
        # Draw decorative elements
        self._draw_chess_decorations()
        
        title_text = self.big_font.render("Player vs AI", True, self.CHESS_GOLD)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(title_text, title_rect)

        # AI Mode Selection - Improved spacing and positioning
        ai_label = self.font.render("Select AI Difficulty:", True, self.CHESS_SILVER)
        ai_label_rect = ai_label.get_rect(center=(self.screen_width // 2, 150))
        self.screen.blit(ai_label, ai_label_rect)
        
        # Improved button positioning with better spacing
        for i, mode in enumerate(self.ai_modes):
            rect = self._get_ai_mode_button_rect(i)
            mode_display = {
                "easy": "Easy",
                "medium": "Medium", 
                "stockfish": "Stockfish"
            }
            self._draw_button(rect, mode_display.get(mode, mode), self.selected_ai_mode == mode)

        # Start Game Button - Better positioned
        self.start_game_button_rect = pygame.Rect(
            (self.screen_width - 250) // 2, self.screen_height - 150, 250, 70
        )
        self._draw_button(self.start_game_button_rect, "Start Game")

        # Back Button - Better positioned
        self.back_button_rect = pygame.Rect(
            (self.screen_width - 200) // 2, self.screen_height - 80, 200, 60
        )
        self._draw_button(self.back_button_rect, "Back")

    def _draw_load_game_menu(self):
        # Draw decorative elements
        self._draw_chess_decorations()
        
        title_text = self.big_font.render("Load Game", True, self.CHESS_GOLD)
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(title_text, title_rect)

        # Improved display area positioning
        display_area_start_y = 120  # Increased from 100 to avoid title overlap
        display_area_height = self.screen_height - 220  # Adjusted for better spacing
        
        temp_surface = pygame.Surface((self.screen_width, max(display_area_height, len(self.saved_games) * self.item_height)), pygame.SRCALPHA)
        temp_surface.fill((0,0,0,0))

        self.delete_buttons_rects = [] # Clears the list for this drawing cycle

        y_offset_in_temp = 0
        if not self.saved_games:
            no_saves_text = self.font.render("No games saved.", True, self.CHESS_SILVER)
            no_saves_rect = no_saves_text.get_rect(center=(self.screen_width // 2, display_area_height // 2))
            temp_surface.blit(no_saves_text, no_saves_rect)
        else:
            for name, data in self.saved_games.items():
                # Improved item positioning and spacing
                item_rect_on_temp = pygame.Rect(
                    (self.screen_width - 450) // 2, y_offset_in_temp + 5, 450, self.item_height - 15
                )
                self._draw_button_on_surface(temp_surface, item_rect_on_temp, f"{name}")

                # Improved delete button positioning
                delete_button_size = 35  # Slightly larger for better usability
                delete_button_margin_x = 15  # Increased margin
                delete_button_x_on_temp = item_rect_on_temp.right + delete_button_margin_x
                delete_button_y_on_temp = item_rect_on_temp.centery - (delete_button_size // 2)
                
                delete_button_rect_on_temp = pygame.Rect(delete_button_x_on_temp, delete_button_y_on_temp, delete_button_size, delete_button_size)

                pygame.draw.rect(temp_surface, self.CHESS_RED, delete_button_rect_on_temp, border_radius=8)
                delete_text_surface = self.delete_font.render("X", True, self.WHITE)
                delete_text_rect = delete_text_surface.get_rect(center=delete_button_rect_on_temp.center)
                temp_surface.blit(delete_text_surface, delete_text_rect)

                # Stores the rectangle (relative to temp_surface) and the save name
                self.delete_buttons_rects.append((delete_button_rect_on_temp, name))

                y_offset_in_temp += self.item_height + 5  # Added extra spacing between items
            
        self.screen.blit(temp_surface, (0, display_area_start_y - self.scroll_offset))

        # Back Button - Better positioned
        self.back_button_rect_load = pygame.Rect(
            (self.screen_width - 200) // 2, self.screen_height - 80, 200, 60
        )
        self._draw_button(self.back_button_rect_load, "Back")


    def _draw_button(self, rect, text, selected=False):
        # Uniform color system for consistent visual appearance
        base_color = self.CHESS_DARK
        hover_color = self.CHESS_SILVER
        border_color = self.CHESS_GOLD
        
        # Apply selection and hover effects
        if selected:
            color = hover_color
        else:
            color = base_color
            
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = rect.collidepoint(mouse_pos)
        
        if is_hovered:
            color = hover_color
            # Enhanced hover effect with glow
            glow_rect = pygame.Rect(rect.x - 2, rect.y - 2, rect.width + 4, rect.height + 4)
            pygame.draw.rect(self.screen, border_color, glow_rect, border_radius=17)
        
        # Draw button with improved chess theme and enhanced effects
        pygame.draw.rect(self.screen, color, rect, border_radius=15)
        
        # Enhanced border with better contrast
        border_width = 4 if is_hovered else 3
        pygame.draw.rect(self.screen, border_color, rect, border_width, border_radius=15)
        
        # Add subtle inner highlight for depth
        if is_hovered:
            highlight_rect = pygame.Rect(rect.x + 2, rect.y + 2, rect.width - 4, rect.height - 4)
            pygame.draw.rect(self.screen, (255, 255, 255, 30), highlight_rect, border_radius=13)
        
        # Improved text rendering with better contrast and positioning
        text_color = self.CHESS_LIGHT if not is_hovered else (255, 255, 255)
        label = self.font.render(text, True, text_color)
        label_rect = label.get_rect(center=rect.center)
        
        # Add subtle text shadow for better readability
        shadow_surface = self.font.render(text, True, (0, 0, 0, 100))
        shadow_rect = shadow_surface.get_rect(center=(label_rect.centerx + 1, label_rect.centery + 1))
        self.screen.blit(shadow_surface, shadow_rect)
        
        # Draw main text
        self.screen.blit(label, label_rect)

    def _draw_button_on_surface(self, surface, rect, text, selected=False):
        # Use improved chess theme colors for surface buttons
        base_color = self.CHESS_DARK
        hover_color = self.CHESS_SILVER
        border_color = self.CHESS_GOLD
        
        if selected:
            color = hover_color
        else:
            color = base_color
        
        # Draw button with improved chess theme and enhanced effects
        pygame.draw.rect(surface, color, rect, border_radius=15)
        
        # Enhanced border with better contrast
        border_width = 4 if selected else 3
        pygame.draw.rect(surface, border_color, rect, border_width, border_radius=15)
        
        # Add subtle inner highlight for depth when selected
        if selected:
            highlight_rect = pygame.Rect(rect.x + 2, rect.y + 2, rect.width - 4, rect.height - 4)
            pygame.draw.rect(surface, (255, 255, 255, 30), highlight_rect, border_radius=13)
        
        # Improved text rendering with better contrast and positioning
        text_color = self.CHESS_LIGHT if not selected else (255, 255, 255)
        label = self.font.render(text, True, text_color)
        label_rect = label.get_rect(center=rect.center)
        
        # Add subtle text shadow for better readability
        shadow_surface = self.font.render(text, True, (0, 0, 0, 100))
        shadow_rect = shadow_surface.get_rect(center=(label_rect.centerx + 1, label_rect.centery + 1))
        surface.blit(shadow_surface, shadow_rect)
        
        # Draw main text
        surface.blit(label, label_rect)


    def _get_ai_mode_button_rect(self, index):
        button_width = 180  # Increased width for better text display
        button_height = 60   # Increased height for better proportions
        spacing = 20         # Increased spacing between buttons
        x_start = self.screen_width // 2 - (len(self.ai_modes) * (button_width + spacing) - spacing) // 2
        return pygame.Rect(x_start + index * (button_width + spacing), 200, button_width, button_height)

    def _get_time_control_button_rect(self, index):
        button_width = 180  # Increased width for better text display
        button_height = 60   # Increased height for better proportions
        spacing = 20         # Increased spacing between buttons
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
        return load_config()

    def _confirm_delete_save(self, save_name):
        """Show a confirmation dialog for deleting a save game"""
        # Simple confirmation - in a real implementation, you might want a proper dialog
        # For now, we'll just return True to confirm deletion
        # You can enhance this later with a proper confirmation UI
        return True
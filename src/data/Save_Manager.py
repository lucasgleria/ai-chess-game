import json
import os

class SaveManager:
    def __init__(self, filename="saves.json"):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensures the save file exists and is valid JSON."""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump({}, f) # Initializes with an empty JSON object
        else:
            # Tries to load to check if it's valid JSON
            with open(self.filename, 'r') as f:
                try:
                    json.load(f)
                except json.JSONDecodeError:
                    # If invalid, overwrites with an empty object
                    with open(self.filename, 'w') as f_write:
                        json.dump({}, f_write)

    def load_all_saves(self):
        """Loads all saved games from the file."""
        self._ensure_file_exists() # Ensures the file exists before attempting to read
        with open(self.filename, 'r') as f:
            try:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
            except json.JSONDecodeError:
                # This should be less likely now with _ensure_file_exists, but it's a safeguard
                return {}

    def save_game(self, name, fen, local, ai_type, skill_level, thinking_time, time_control, white_time_left, black_time_left):
        """Saves the current game state."""
        saves = self.load_all_saves()
        saves[name] = {
            "FEN": fen,
            "local": local,
            "ai_type": ai_type,
            "skill_level": skill_level,
            "thinking_time": thinking_time,
            "time_control": time_control,
            "white_time_left": white_time_left,
            "black_time_left": black_time_left
        }
        with open(self.filename, 'w') as f:
            json.dump(saves, f, indent=4) # Saves with indentation for readability

    def delete_save(self, name):
        """Deletes a saved game by name."""
        saves = self.load_all_saves()
        if name in saves:
            del saves[name]
            with open(self.filename, 'w') as f:
                json.dump(saves, f, indent=4)
            return True
        return False
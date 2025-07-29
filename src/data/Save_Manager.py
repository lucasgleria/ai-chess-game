import json

class SaveManager:
    
    def __init__(self):
        
        self.data_fen = "data.json"
    
    def save_game(self, fen):

        with open(self.data_fen, "w") as f:
            json.dump({"FEN" : fen}, f)
    
    def load_game(self):

        with open(self.data_fen, "r") as f:
            return json.load(f)
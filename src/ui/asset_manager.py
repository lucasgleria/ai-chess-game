# src/ui/asset_manager.py

import pygame
import os

class AssetManager:
    def __init__(self, piece_path="assets/pieces/", square_size=100):
        self.piece_path = piece_path
        self.square_size = square_size
        self.pieces = {}

        # Set the names of the chess pieces
        self.piece_names = [
            "white_pawn", "white_rook", "white_knight", "white_bishop", "white_queen", "white_king",
            "black_pawn", "black_rook", "black_knight", "black_bishop", "black_queen", "black_king"
        ]

        self.load_pieces()

    def load_pieces(self):
        # Loads and resizes the piece images
        piece_scale = int(self.square_size * 0.9)  # 90% of the square size
        for name in self.piece_names:
            path = os.path.join(self.piece_path, f"{name}.png")
            if os.path.exists(path):
                image = pygame.image.load(path).convert_alpha()
                image = pygame.transform.smoothscale(image, (piece_scale, piece_scale))
                self.pieces[name] = image
            else:
                print(f"[!WARNING!] Missing piece: {path}")

    def get_piece(self, name):

        # Returns the sprite of a piece by name.
        return self.pieces.get(name)
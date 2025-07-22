# src/ui/audio_manager.py

import pygame
import os

class AudioManager:
    def __init__(self, audio_path="assets/audio/"):
        self.audio_path = audio_path
        self.sounds = {}
        self.load_sounds()

    def load_sounds(self):
       # Load necessary sound files
        sound_files = {
            "move": "move.wav",  # Sound for moving a piece
            "checkmate": "checkmate.wav",  # Sound for checkmate
            "capture": "capture.wav",  # Sound for capturing a piece
        }

        for key, filename in sound_files.items():
            path = os.path.join(self.audio_path, filename)
            if os.path.exists(path):
                self.sounds[key] = pygame.mixer.Sound(path)
            else:
                print(f"[AVISO] Som não encontrado: {path}")

    def play(self, name):
        # Plays the sound associated with the name (ex: 'move)
        if name in self.sounds:
            self.sounds[name].play()

import chess
import chess.engine
import os
import threading
from src.ia.ai_base import BaseChessAI

class StockfishAI(BaseChessAI):
    def __init__(self, engine_path="engines/stockfish-windows-x86-64-avx2.exe", skill_level=10, thinking_time=1.0):
        self.engine_path = engine_path
        self.skill_level = skill_level  # 0-20
        self.thinking_time = thinking_time  # in seconds
        self.lock = threading.Lock()

        if not os.path.exists(self.engine_path):
            raise FileNotFoundError(f"Stockfish binary not found at {self.engine_path}")

        self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)
        self.engine.configure({"Skill Level": self.skill_level})

    def set_skill_level(self, level):
        with self.lock:
            self.skill_level = max(0, min(20, level))
            self.engine.configure({"Skill Level": self.skill_level})

    def set_thinking_time(self, seconds):
        self.thinking_time = max(0.1, seconds)

    def get_best_move(self, board, callback=None):
        def run_engine():
            with self.lock:
                try:
                    result = self.engine.play(board, chess.engine.Limit(time=self.thinking_time))
                    if callback:
                        callback(result.move)
                except Exception as e:
                    print(f"[StockfishAI] Error during move generation: {e}")
                    if callback:
                        callback(None)

        thread = threading.Thread(target=run_engine)
        thread.start()

    def __del__(self):
        try:
            self.engine.quit()
        except Exception:
            pass
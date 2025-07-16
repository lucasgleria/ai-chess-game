import abc

class BaseChessAI(abc.ABC):
    @abc.abstractmethod
    def get_best_move(self, board):
        """
        Given a chess.Board object, returns the best move found by the AI.
        Must be implemented by subclasses.
        """
        pass 
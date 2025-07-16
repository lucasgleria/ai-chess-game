import chess
from ia.ai_base import BaseChessAI

class MediumAI(BaseChessAI):
    def __init__(self, depth=2):
        self.depth = depth

    def get_best_move(self, board):
        best_move = None
        best_value = float('-inf') if board.turn == chess.WHITE else float('inf')
        for move in board.legal_moves:
            board.push(move)
            value = self.alphabeta(board, self.depth - 1, float('-inf'), float('inf'), not board.turn)
            board.pop()
            if board.turn == chess.WHITE:
                if value > best_value:
                    best_value = value
                    best_move = move
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
        return best_move

    def alphabeta(self, board, depth, alpha, beta, is_white):
        if depth == 0 or board.is_game_over():
            return self.evaluate(board)
        if is_white:
            max_eval = float('-inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.alphabeta(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.legal_moves:
                board.push(move)
                eval = self.alphabeta(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def evaluate(self, board):
        # Evaluation: material + center control + basic king safety
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3.2,
            chess.BISHOP: 3.3,
            chess.ROOK: 5.1,
            chess.QUEEN: 9.5,
            chess.KING: 0
        }
        value = 0
        for piece_type in piece_values:
            value += len(board.pieces(piece_type, chess.WHITE)) * piece_values[piece_type]
            value -= len(board.pieces(piece_type, chess.BLACK)) * piece_values[piece_type]
        # Center: d4, d5, e4, e5
        center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
        value += 0.2 * sum(1 for sq in center_squares if board.piece_at(sq) and board.piece_at(sq).color == chess.WHITE)
        value -= 0.2 * sum(1 for sq in center_squares if board.piece_at(sq) and board.piece_at(sq).color == chess.BLACK)
        # King safety: penalizes exposed king (rank 1/8 without pawns)
        value += self.king_safety(board, chess.WHITE)
        value -= self.king_safety(board, chess.BLACK)
        return value

    def king_safety(self, board, color):
        king_square = board.king(color)
        if king_square is None:
            return -5  # King captured (should be game over)
        rank = chess.square_rank(king_square)
        if (color == chess.WHITE and rank != 0) or (color == chess.BLACK and rank != 7):
            return -1  # King out of first/last rank
        # Penalizes if there are no pawns nearby
        pawn_shield = 0
        for file in range(8):
            sq = chess.square(file, rank + (1 if color == chess.WHITE else -1))
            if board.piece_at(sq) and board.piece_at(sq).piece_type == chess.PAWN and board.piece_at(sq).color == color:
                pawn_shield += 0.5
        return pawn_shield 
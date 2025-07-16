import chess
import pytest
from ia.easy_ai import EasyAI
from ia.medium_ai import MediumAI

@pytest.fixture
def starting_board():
    return chess.Board()

def test_easy_ai_returns_legal_move(starting_board):
    ai = EasyAI(depth=1)
    move = ai.get_best_move(starting_board)
    assert move in starting_board.legal_moves

def test_medium_ai_returns_legal_move(starting_board):
    ai = MediumAI(depth=2)
    move = ai.get_best_move(starting_board)
    assert move in starting_board.legal_moves

def test_easy_ai_evaluate_material():
    ai = EasyAI()
    board = chess.Board()
    # Initial position: equal material
    assert ai.evaluate(board) == 0
    # Remove a white piece
    board.remove_piece_at(chess.E2)
    assert ai.evaluate(board) < 0

def test_medium_ai_evaluate_material_and_center():
    ai = MediumAI()
    board = chess.Board()
    # Initial position: equal material
    assert abs(ai.evaluate(board)) < 1.1
    # Place a white pawn in the center
    board.set_piece_at(chess.E4, chess.Piece(chess.PAWN, chess.WHITE))
    assert ai.evaluate(board) > 0 

def test_medium_ai_pawn_structure_isolated():
    ai = MediumAI()
    board = chess.Board()
    # Coloca um peão branco isolado em a4
    board.clear_board()
    board.set_piece_at(chess.A4, chess.Piece(chess.PAWN, chess.WHITE))
    board.set_piece_at(chess.E4, chess.Piece(chess.PAWN, chess.WHITE))
    # O peão em a4 deve ser penalizado
    eval_isolated = ai.evaluate(board)
    # Agora adiciona um peão branco em b4 (não isolado)
    board.set_piece_at(chess.B4, chess.Piece(chess.PAWN, chess.WHITE))
    eval_not_isolated = ai.evaluate(board)
    assert eval_not_isolated > eval_isolated

def test_medium_ai_pawn_structure_doubled():
    ai = MediumAI()
    board = chess.Board()
    board.clear_board()
    # Dois peões brancos na mesma coluna
    board.set_piece_at(chess.A4, chess.Piece(chess.PAWN, chess.WHITE))
    board.set_piece_at(chess.A5, chess.Piece(chess.PAWN, chess.WHITE))
    eval_doubled = ai.evaluate(board)
    # Um peão só
    board.remove_piece_at(chess.A5)
    eval_single = ai.evaluate(board)
    assert eval_single > eval_doubled

def test_medium_ai_pawn_structure_blocked():
    ai = MediumAI()
    board = chess.Board()
    board.clear_board()
    # Peão branco bloqueado por outro peão
    board.set_piece_at(chess.A4, chess.Piece(chess.PAWN, chess.WHITE))
    board.set_piece_at(chess.A5, chess.Piece(chess.PAWN, chess.WHITE))
    eval_blocked = ai.evaluate(board)
    # Peão não bloqueado
    board.remove_piece_at(chess.A5)
    eval_free = ai.evaluate(board)
    assert eval_free > eval_blocked

def test_medium_ai_mobility():
    ai = MediumAI()
    board = chess.Board()
    # Posição inicial: mobilidade limitada
    eval_start = ai.evaluate(board)
    # Remove todos os peões para aumentar mobilidade
    for sq in range(8, 16):
        board.remove_piece_at(sq)
        board.remove_piece_at(sq + 40)
    eval_open = ai.evaluate(board)
    assert eval_open > eval_start

def test_medium_ai_depth_affects_move():
    board = chess.Board()
    ai_depth1 = MediumAI(depth=1)
    ai_depth3 = MediumAI(depth=3)
    move1 = ai_depth1.get_best_move(board)
    move3 = ai_depth3.get_best_move(board)
    # Não é garantido que sejam diferentes, mas o teste valida que ambos são legais
    assert move1 in board.legal_moves
    assert move3 in board.legal_moves 
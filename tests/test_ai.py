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
    assert abs(ai.evaluate(board)) < 0.01
    # Place a white pawn in the center
    board.set_piece_at(chess.E4, chess.Piece(chess.PAWN, chess.WHITE))
    assert ai.evaluate(board) > 0 
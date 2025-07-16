import pytest
from core.chess_game import ChessGame

@pytest.fixture
def game():
    return ChessGame()

def test_new_game(game):
    game.make_move('e2e4')
    game.new_game()
    assert game.board.fullmove_number == 1
    assert game.board.is_game_over() is False

def test_make_and_undo_move(game):
    assert game.make_move('e2e4')
    assert game.board.piece_at(28) is not None  # e4
    assert game.undo_move()
    assert game.board.piece_at(28) is None  # e4

def test_is_legal_move(game):
    assert game.is_legal_move('e2e4')
    assert not game.is_legal_move('e2e5')

def test_get_legal_moves(game):
    moves = game.get_legal_moves()
    assert 'e2e4' in moves
    assert 'e7e5' not in moves  # not black's turn

def test_checkmate_and_stalemate():
    game = ChessGame()
    # Fool's mate
    game.make_move('f2f3')
    game.make_move('e7e5')
    game.make_move('g2g4')
    game.make_move('d8h4')
    assert game.is_checkmate()
    assert game.is_game_over()
    outcome = game.outcome()
    assert outcome is not None and outcome.winner is False  # Black wins

    # Stalemate position
    game = ChessGame()
    # Set up a known stalemate position
    game.board.set_fen('7k/5Q2/6K1/8/8/8/8/8 b - - 0 1')
    assert game.is_stalemate()
    assert game.is_game_over()
    outcome = game.outcome()
    assert outcome is not None and outcome.winner is None

def test_move_conversion(game):
    move_obj = game.uci_to_move('e2e4')
    assert move_obj is not None
    assert game.move_to_uci(move_obj) == 'e2e4' 
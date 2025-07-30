import pygame
import chess
import re # Importar re para a função load_pieces
from src.core.move_validator import MoveValidator # Importar MoveValidator

class BoardRenderer():
    def __init__(self, screen, square_size, chess_game_instance, local, asset_manager=None, audio_manager=None):
        self.screen = screen
        self.square_size = square_size
        self.asset_manager = asset_manager
        self.audio_manager = audio_manager
        self.local = local # Indica se é um jogo local (Player vs Player)

        # AGORA, self.chess_game RECEBE A INSTÂNCIA JÁ CRIADA DO main.py
        self.chess_game = chess_game_instance
        # Instância de MoveValidator usando a mesma instância de ChessGame
        self.move_val = MoveValidator(self.chess_game)

        # Fonte para mensagens de status
        self.status_font = pygame.font.SysFont("Arial", 28, bold=True)

        # Chessboard colors
        self.light_color = (240, 217, 181)  # light color
        self.dark_color = (181, 136, 99)    # dark color

        self.selected_square = None # (row, col) da peça selecionada
        self.dragging_piece = None  # Símbolo da peça que está sendo arrastada
        self.dragging_piece_original_pos = None # (row, col) original da peça arrastada
        self.drag_offset_x = 0      # Deslocamento X do mouse em relação ao canto superior esquerdo da peça
        self.drag_offset_y = 0      # Deslocamento Y do mouse em relação ao canto superior esquerdo da peça
        self.mouse_pos = (0, 0)     # Posição atual do mouse na tela

        self.last_move = None # Para destacar o último movimento

        # Mapeamento de símbolos FEN para nomes de assets
        self.piece_map = {
            'r': "black_rook", 'n': "black_knight", 'b': "black_bishop",
            'q': "black_queen", 'k': "black_king", 'p': "black_pawn",
            'R': "white_rook", 'N': "white_knight", 'B': "white_bishop",
            'Q': "white_queen", 'K': "white_king", 'P': "white_pawn"
        }

        # Carrega as peças com base no FEN atual do chess_game
        self.load_pieces()

    def load_pieces(self):
        # Cria uma representação 2D do tabuleiro para renderização no Pygame.
        # Isso é diferente do chess.Board, é apenas para o estado visual.
        self.test_board = [[None for _ in range(8)] for _ in range(8)]
        # Obtém o FEN do tabuleiro real do chess_game
        current_fen = self.chess_game.board.fen()
        # Divide o FEN para obter a parte das peças
        fen_parts = current_fen.split(' ')[0]
        
        row_idx = 0
        col_idx = 0
        for char in fen_parts:
            if char == '/':
                row_idx += 1
                col_idx = 0
            elif char.isdigit():
                col_idx += int(char)
            else:
                # Usa self.piece_map para obter o nome do asset
                self.test_board[row_idx][col_idx] = self.piece_map.get(char)
                col_idx += 1

    # Desenha uma mensagem centralizada no topo do tabuleiro
    def draw_status_message(self, message, color=(255, 255, 255)):
        text_surface = self.status_font.render(message, True, color)
        screen_width = self.screen.get_width()
        text_rect = text_surface.get_rect(center=(screen_width // 2, 30))
        self.screen.blit(text_surface, text_rect)

    def draw_board(self):
        # Desenha o tabuleiro (8x8) alternando as cores dos quadrados
        for r in range(8):
            for c in range(8):
                color = self.light_color if (r + c) % 2 == 0 else self.dark_color
                rect = pygame.Rect(c * self.square_size, r * self.square_size, self.square_size, self.square_size)
                pygame.draw.rect(self.screen, color, rect)

                # Destacar o último movimento
                if self.last_move:
                    from_square_uci = self.last_move[:2]
                    to_square_uci = self.last_move[2:4]
                    
                    # Converte UCI para coordenadas de linha/coluna do Pygame
                    from_col_last = chess.parse_square(from_square_uci) % 8
                    from_row_last = 7 - (chess.parse_square(from_square_uci) // 8)
                    to_col_last = chess.parse_square(to_square_uci) % 8
                    to_row_last = 7 - (chess.parse_square(to_square_uci) // 8)

                    highlight_color = (200, 200, 0, 100) # Amarelo semi-transparente
                    s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
                    s.fill(highlight_color)

                    if r == from_row_last and c == from_col_last:
                        self.screen.blit(s, (c * self.square_size, r * self.square_size))
                    if r == to_row_last and c == to_col_last:
                        self.screen.blit(s, (c * self.square_size, r * self.square_size))

                # Destacar quadrado selecionado
                if self.selected_square and self.selected_square == (r, c):
                    pygame.draw.rect(self.screen, (255, 255, 0), rect, 3) # Amarelo, borda de 3px

                # Desenhar peças
                piece_symbol = self.test_board[r][c]
                # Não desenha a peça que está sendo arrastada na posição original
                if piece_symbol and (r, c) != self.dragging_piece_original_pos:
                    piece_image = self.asset_manager.get_piece(piece_symbol)
                    if piece_image:
                        self.screen.blit(piece_image, (c * self.square_size, r * self.square_size))

        # Desenhar a peça arrastada por último, por cima de tudo
        if self.dragging_piece:
            x, y = pygame.mouse.get_pos()
            # Ajusta a posição da peça arrastada para a superfície do tabuleiro
            # Considera o deslocamento do tabuleiro na tela principal
            board_offset_x = (self.screen.get_width() - 8 * self.square_size) // 2
            board_offset_y = (self.screen.get_height() - 8 * self.square_size) // 2 # Pode ser diferente se o menu estiver no topo

            piece_image = self.asset_manager.get_piece(self.dragging_piece)
            if piece_image:
                # A posição da peça arrastada é a posição do mouse menos o offset do arrasto,
                # menos o offset do tabuleiro na tela para que fique dentro da área do tabuleiro.
                self.screen.blit(piece_image, (x - self.drag_offset_x - board_offset_x, y - self.drag_offset_y - board_offset_y))

        # Higlight valid moves for the selected piece
        if self.selected_square:
            for move_row, move_col in self.chess_game.get_legal_moves_from(self.to_chess_square(self.selected_square[0], self.selected_square[1])):
                center = (
                    move_col * self.square_size + self.square_size // 2,
                    move_row * self.square_size + self.square_size // 2,
                )
                radius = self.square_size // 6
                pygame.draw.circle(self.screen, (0, 255, 0, 100), center, radius) # Verde semi-transparente

        # Mostra mensagens de status na parte superior
        if self.chess_game.board.is_checkmate():
            message = "Checkmate!"
        elif self.chess_game.board.is_stalemate() or self.chess_game.board.is_insufficient_material():
            message = "Empate!"
        elif self.chess_game.board.is_check():
            message = "Cheque!"
        else:
            message = "Turno das Pretas" if self.chess_game.board.turn == chess.BLACK else "Turno das Brancas"

        self.draw_status_message(message)

    def handle_click(self, pos):
        col = pos[0] // self.square_size
        row = pos[1] // self.square_size
        
        # Converte para a notação do python-chess
        chess_square = chess.square(col, 7 - row)
        
        # Verifica se o quadrado clicado tem uma peça do turno atual
        piece = self.chess_game.board.piece_at(chess_square)
        if piece and piece.color == self.chess_game.board.turn:
            self.selected_square = (row, col)
            self.dragging_piece = self.test_board[row][col]
            self.dragging_piece_original_pos = (row, col) # Guarda a posição original da peça arrastada
            
            # Ajusta o offset para a posição do mouse em relação à peça
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Precisamos considerar o offset do tabuleiro na tela principal para o cálculo correto
            board_offset_x = (self.screen.get_width() - 8 * self.square_size) // 2
            board_offset_y = (self.screen.get_height() - 8 * self.square_size) // 2

            self.drag_offset_x = (mouse_x - board_offset_x) - (col * self.square_size)
            self.drag_offset_y = (mouse_y - board_offset_y) - (row * self.square_size)
        else:
            self.selected_square = None
            self.dragging_piece = None
            self.dragging_piece_original_pos = None


    def start_drag(self, pos):
        # A lógica de início de arrasto já está em handle_click
        pass

    def end_drag(self, pos):
        if self.selected_square:
            target_col = pos[0] // self.square_size
            target_row = pos[1] // self.square_size

            from_row, from_col = self.selected_square
            from_uci = chess.square_name(chess.square(from_col, 7 - from_row))
            to_uci = chess.square_name(chess.square(target_col, 7 - target_row))

            move_uci = from_uci + to_uci

            # Lógica para promoção (exemplo simples: sempre rainha)
            # Verifica se a peça é um peão e está na última fila
            piece = self.chess_game.board.piece_at(chess.parse_square(from_uci))
            if piece and piece.piece_type == chess.PAWN:
                if (piece.color == chess.WHITE and target_row == 0) or \
                   (piece.color == chess.BLACK and target_row == 7):
                    move_uci += 'q' # Promove para rainha por padrão

            if self.chess_game.is_legal_move(move_uci):
                # Verifica se houve captura antes de fazer o movimento
                captured_piece_before_move = self.chess_game.board.piece_at(chess.parse_square(to_uci))

                self.chess_game.make_move(move_uci) # Aplica o movimento ao tabuleiro principal
                self.last_move = move_uci # Armazena o último movimento para destaque
                self.load_pieces() # Recarrega as peças para refletir o novo estado

                # Toca som de movimento ou captura
                if self.audio_manager:
                    if captured_piece_before_move:
                        self.audio_manager.play("capture")
                    else:
                        self.audio_manager.play("move")
                
                # Chama o MoveValidator para verificar o estado do jogo
                self.move_val.validate_move() # ESTA É A LINHA CRÍTICA!
            else:
                # Movimento ilegal, a peça será redesenhada na posição original
                pass

        # Limpa o estado de arrasto e seleção
        self.selected_square = None
        self.dragging_piece = None
        self.dragging_piece_original_pos = None
        # self.valid_moves = [] # Não precisa limpar aqui, é limpo em handle_click se a seleção mudar

    def update_mouse_pos(self, pos):
        self.mouse_pos = pos
        
    def to_chess_square(self, row, col):
        # Esta função foi movida para dentro da classe BoardRenderer
        # para resolver o AttributeError
        files = 'abcdefgh'  # columns
        ranks = '87654321'  # rows (0 is rank 8)
        return files[col] + ranks[row]
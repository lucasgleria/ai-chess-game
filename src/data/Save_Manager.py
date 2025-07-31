# import json

# class SaveManager:
    
#     def __init__(self):
        
#         self.data_fen = "data.json"
    
#     def save_game(self, fen):

#         with open(self.data_fen, "w") as f:
#             json.dump({"FEN" : fen}, f)
    
#     def load_game(self):

#         with open(self.data_fen, "r") as f:
#             return json.load(f)

import json
import os

class SaveManager:
    def __init__(self, save_file='saves.json'):
        self.save_file = save_file
        # Garante que o arquivo de saves exista e seja um JSON válido
        if not os.path.exists(self.save_file):
            with open(self.save_file, 'w') as f:
                json.dump({}, f) # Inicializa com um dicionário vazio
        elif os.path.getsize(self.save_file) == 0:
            # Se o arquivo existir mas estiver vazio, inicializa-o
            with open(self.save_file, 'w') as f:
                json.dump({}, f)

    def _load_saves(self):
        """Carrega todos os saves do arquivo JSON."""
        try:
            with open(self.save_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            # Lida com arquivos JSON corrompidos ou vazios
            print(f"Aviso: Arquivo de saves '{self.save_file}' corrompido ou vazio. Recriando.")
            return {}
        except FileNotFoundError:
            # Isso não deve acontecer se o __init__ for bem-sucedido, mas é uma segurança
            return {}

    def _save_saves(self, saves_data):
        """Salva todos os saves no arquivo JSON."""
        with open(self.save_file, 'w') as f:
            json.dump(saves_data, f, indent=4) # Usa indent para facilitar a leitura

    def save_game(self, save_name, FEN, local, ai_type, skill_level, thinking_time, time_control, white_time_left, black_time_left):
        """
        Salva o estado atual do jogo com um nome fornecido pelo usuário.
        
        Args:
            save_name (str): Nome único para o save.
            FEN (str): Notação FEN do tabuleiro.
            local (bool): True para Player vs Player, False para Player vs AI.
            ai_type (str | None): Tipo da IA ('easy', 'medium', 'stockfish') ou None.
            skill_level (int | None): Nível de habilidade da Stockfish ou None.
            thinking_time (float | None): Tempo de pensamento da Stockfish ou None.
            time_control (str | None): Tipo de controle de tempo ('classic', 'rapid', etc.) ou None.
            white_time_left (float | None): Tempo restante das brancas em segundos ou None.
            black_time_left (float | None): Tempo restante das pretas em segundos ou None.
        """
        saves = self._load_saves()
        saves[save_name] = {
            "FEN": FEN,
            "local": local,
            "ai_type": ai_type,
            "skill_level": skill_level,
            "thinking_time": thinking_time,
            "time_control": time_control,
            "white_time_left": white_time_left,
            "black_time_left": black_time_left
        }
        self._save_saves(saves)
        print(f"Jogo '{save_name}' salvo com sucesso!")

    def load_all_saves(self):
        """
        Carrega e retorna um dicionário com todos os jogos salvos.
        Retorna um dicionário vazio se não houver saves.
        """
        return self._load_saves()

    def delete_save(self, save_name):
        """
        Deleta um save específico do arquivo.
        
        Args:
            save_name (str): Nome do save a ser deletado.
        """
        saves = self._load_saves()
        if save_name in saves:
            del saves[save_name]
            self._save_saves(saves)
            print(f"Save '{save_name}' deletado com sucesso.")
            return True
        print(f"Save '{save_name}' não encontrado.")
        return False

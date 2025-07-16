# 📋 Developer A Checklist

**Main Focus:** Core Game Logic, Main Flow, and Match Management.

---

## Phase 0: Setup and Initial Planning (All Together)

- [x] **0.1 "Hello Pygame" Prototype:** Edit the main.py file to run your first hello world in pygame.
- [x] **0.2 Internal API Design (Overview):** Participate in the discussion and definition of the main classes and interactions.

---

## Phase 1: Independent Foundation

- [x] **1.A.1 Set up python-chess:**
  - Create a `ChessGame` class (or similar) that encapsulates a `chess.Board()` object.
  - Implement methods to start a new game (`new_game()`).
  - Add methods to apply a move (`make_move(move_str)` or `make_move(from_sq, to_sq)`).
  - Add a method to undo a move (`undo_move()`).

- [x] **1.A.2 Validation and Game State:**
  - Implement methods to check if a move is legal (`is_legal_move(move)`).
  - Implement methods to check the game state (`is_checkmate()`, `is_stalemate()`, `is_game_over()`, `outcome()`).

- [x] **1.A.3 Move Representation:**
  - Ensure the class can generate all legal moves for the current position (`get_legal_moves()`).
  - Convert moves between formats (e.g., `e2e4` to `chess.Move` object).

- [x] **1.A.4 Unit Tests:** Write tests for all game logic functions (validate moves, check checkmate, etc.) to ensure robustness.

---

## Phase 2: Integration and Essential Features

- [ ] **2.A.1 Logic-UI Integration:**
  - Connect click/drag events from the interface (from Developer B) to the move logic (`ChessGame.make_move()`).
  - Receive feedback from the logic (`is_legal_move`, `is_checkmate`) and inform the UI.

- [ ] **2.A.2 AI Integration:**
  - In the main game loop, alternate turns.
  - When it's the AI's turn (from Developer C), call `current_ai.get_best_move(board)`.
  - Apply the move returned by the AI to `ChessGame`.
  - Manage the game state (whose turn, if it's over).

- [ ] **2.A.3 Undo Implementation:** Connect the logic's `undo_move()` method to a UI event (future button).

- [ ] **2.A.4 Match Management:** Implement transitions between game states (menu, playing, end of game).

---

## Phase 3: Advanced Features and Polish

- [ ] **3.A.1 Main Menu:** Implement the Pygame main menu with buttons "New Game", "Load Game", "Game Modes", "Local Multiplayer", "Exit".

- [ ] **3.A.2 Save/Load Game:**
  - Implement functionality to save the game state (FEN) to a file.
  - Implement functionality to load a game from a FEN file.

- [ ] **3.A.3 Local Multiplayer (PvP):**
  - Set up logic to alternate turns between two human players.
  - Ensure the AI is not activated in this mode.

---

## Phase 4: Final Polish and Distribution (All Together)

- [ ] **4.1 Integration Tests:** Participate in testing all features together.
- [ ] **4.2 Usability Tests:** Participate in gathering feedback from external users.
- [ ] **4.3 Error Handling and Robustness:** Contribute to exception handling.
- [ ] **4.4 Documentation:** Contribute to project documentation.
- [ ] **4.5 Packaging for Distribution:** Assist in creating executables with PyInstaller.
- [ ] **4.6 Release and Launch:** Participate in the game launch.
# 📋 Developer C Checklist

**Main Focus:** AI Structure, AI Implementation (Easy, Medium, Hard), and Optimization.

---

## Phase 0: Setup and Initial Planning (All Together)

- [x] **0.1 "Hello Pygame" Prototype:** Edit the main.py file to run your first hello world in pygame.
- [x] **0.2 Internal API Design (Overview):** Participate in the discussion and definition of the main classes and interactions.

---

## Phase 1: Independent Foundation

- [x] **1.C.1 AI Interface Definition:**  
  Create an abstract base class `BaseChessAI` with a `get_best_move(board)` method. All AIs (Easy, Medium, Hard) will inherit from this base.

- [x] **1.C.2 "Easy" AI Implementation (Simple Minimax):**  
  Create the `EasyAI` class that inherits from `BaseChessAI`.  
  Implement a very basic evaluation function (e.g., only material counting).  
  Implement the Minimax algorithm with a very low search depth (1 or 2 ply).  
  Use `board.legal_moves` to generate the search tree children.

- [x] **1.C.3 "Medium" AI Implementation (Minimax with Alpha-Beta):**  
  Create the `MediumAI` class that inherits from `BaseChessAI`.  
  Implement a slightly more sophisticated evaluation function (add center control, basic king safety).  
  Implement the Minimax algorithm with Alpha-Beta Pruning with a slightly higher search depth (2 or 3 ply).

- [x] **1.C.4 AI Testing:**  
  Create tests to ensure that the AIs return moves and that the evaluation functions work as expected.

---

## Phase 2: Integration and Essential Features

- [x] **2.C.1 Improve Evaluation Functions:**  
  Collaborate with Developer A to refine the "Medium" AI evaluation function based on testing and gameplay.  
  Add more factors such as pawn structure, piece activity, etc.

- [x] **2.C.2 AI Optimizations:**  
  Ensure that Alpha-Beta Pruning is working efficiently.  
  Consider additional optimizations (e.g., transposition table - if time permits and more performance is needed).

- [x] **2.C.3 Dynamic Difficulty Creation:**  
  Allow the "Easy" and "Medium" AIs to have difficulty parameters (e.g., search depth) that can be adjusted.

- [x] **2.C.4 Game Testing:**  
  Play extensively against the "Easy" and "Medium" AIs to identify bugs and balance the difficulty.

---

## Phase 3: Advanced Features and Polish

- [ ] **3.C.1 Stockfish Integration:**  
  Implement the `StockfishAI` class that interacts with the Stockfish executable (download it and include it in the `engines/` folder).  
  Use `python-chess.engine` or the `stockfish` library for this communication.

- [ ] **3.C.2 Stockfish Difficulty Configuration:**  
  Allow adjusting the thinking time or "skill level" of Stockfish through the UI (e.g., slider or buttons in the difficulty menu).

- [ ] **3.C.3 AI Performance Optimization and Testing:**  
  Ensure that the AI (especially Stockfish) doesn't freeze the interface (may need to use threading for longer calculations).  
  Test AI performance on different machines.

---

## Phase 4: Final Polish and Distribution (All Together)

- [ ] **4.1 Integration Tests:** Participate in testing all features together.
- [ ] **4.2 Usability Tests:** Participate in gathering feedback from external users.
- [ ] **4.3 Error Handling and Robustness:** Contribute to exception handling.
- [ ] **4.4 Documentation:** Contribute to project documentation.
- [ ] **4.5 Packaging for Distribution:** Assist in creating executables with PyInstaller.
- [ ] **4.6 Release and Launch:** Participate in the game launch.
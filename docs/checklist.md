# 📋 General Chess Project Checklist

This is the master checklist that covers all project tasks from start to finish.  
Tasks marked as **"All Together"** are the responsibility of the entire team.

---

## Phase 0: Setup and Initial Planning (**All Together**)

- [x] **0.1 "Hello Pygame" Prototype:** Each developer creates a basic script to test the Pygame environment.
- [x] **0.2 Internal API Design (Overview):** Discussion and definition of main classes and interactions between modules.

---

## Phase 1: Independent Foundation (Parallel)

### Developer A: Core Game Logic & Board Representation

- [x] **1.A.1 Set up python-chess:** Encapsulate `chess.Board()` and basic game methods.
- [x] **1.A.2 Validation and Game State:** Implement methods to check move legality and final game state.
- [x] **1.A.3 Move Representation:** Generate legal moves and convert formats.
- [x] **1.A.4 Unit Tests:** Write tests for game logic.

### Developer B: Visuals, User Interaction & Audio

- [x] **1.B.1 Basic Pygame Setup:** Set up window, main loop, and sizes.
- [x] **1.B.2 Asset Loading and Drawing:** Load piece PNGs and draw board/pieces.
- [x] **1.B.3 Mouse Event System:** Detect clicks and drag/drop, and visual selection feedback.
- [x] **1.B.4 Basic Audio Logic:** Set up mixer and load/test a simple sound.

### Developer C: AI Framework & AI Core Logic

- [x] **1.C.1 AI Interface Definition:** Create base class `BaseChessAI`.
- [x] **1.C.2 "Easy" AI Implementation (Simple Minimax):** Create `EasyAI` with basic evaluation and low-depth Minimax.
- [x] **1.C.3 "Medium" AI Implementation (Minimax with Alpha-Beta):** Create `MediumAI` with more sophisticated evaluation and Alpha-Beta Pruning.
- [x] **1.C.4 AI Testing:** Write tests for AI functions.

---

## Phase 2: Integration and Essential Features (Collaborative with Focus)

### Developer A (Main Focus: Game Flow and AI)

- [ ] **2.A.1 Logic-UI Integration:** Connect UI events to move logic.
- [ ] **2.A.2 AI Integration:** Call AI on its turn and apply the move.
- [ ] **2.A.3 Undo Implementation:** Connect undo function to a UI event.
- [ ] **2.A.4 Match Management:** Implement transitions between game states.

### Developer B (Main Focus: Interface Polish and UX)

- [ ] **2.B.1 Drawing Refinements:** Improve piece drawing, highlight valid moves and last move.
- [ ] **2.B.2 Status Messages:** Display turn, check, checkmate messages, etc.
- [ ] **2.B.3 Piece Animation:** Implement smooth sliding animation.
- [ ] **2.B.4 Game Sounds:** Integrate sounds for moves, captures, and check.

### Developer C (Main Focus: AI Refinement and Testing)

- [ ] **2.C.1 Improve Evaluation Functions:** Refine the "Medium" AI evaluation function.
- [ ] **2.C.2 AI Optimizations:** Optimize Alpha-Beta Pruning.
- [ ] **2.C.3 Dynamic Difficulty Creation:** Allow adjustment of difficulty parameters for "Easy" and "Medium" AIs.
- [ ] **2.C.4 Game Testing:** Extensively test "Easy" and "Medium" AIs.

---

## Phase 3: Advanced Features and Polish (Collaborative)

### Developer A (Main Focus: Menu, Save/Load, Local Multiplayer)

- [ ] **3.A.1 Main Menu:** Implement the main menu with all options.
- [ ] **3.A.2 Save/Load Game:** Implement save/load functionality via FEN.
- [ ] **3.A.3 Local Multiplayer (PvP):** Set up logic to alternate turns in PvP mode.

### Developer B (Main Focus: Final UX and Aesthetics)

- [ ] **3.B.1 Pawn Promotion:** Implement UI for piece choice in promotion.
- [ ] **3.B.2 End Game Screens:** Create dedicated screens for match results.
- [ ] **3.B.3 General Visual Refinement:** Adjust colors, fonts, layouts, and visual themes.
- [ ] **3.B.4 Enhanced Audio Feedback:** Add background music and other sounds.

### Developer C (Main Focus: "Hard" AI and Difficulty Settings)

- [ ] **3.C.1 Stockfish Integration:** Implement `StockfishAI` class and communication with executable.
- [ ] **3.C.2 Stockfish Difficulty Configuration:** Allow adjustment of thinking time/skill level.
- [ ] **3.C.3 AI Performance Optimization and Testing:** Ensure AI doesn't freeze the interface.

---

## Phase 4: Final Polish and Distribution (**All Together**)

- [ ] **4.1 Integration Tests:** Test all features together.
- [ ] **4.2 Usability Tests:** Collect feedback from external users.
- [ ] **4.3 Error Handling and Robustness:** Implement exception handling.
- [ ] **4.4 Documentation:** Create a clear and complete `README.md`.
- [ ] **4.5 Packaging for Distribution:** Use PyInstaller to create executables.
- [ ] **4.6 Release and Launch:** Share the game.

---
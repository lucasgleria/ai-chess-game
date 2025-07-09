# 📋 Developer B Checklist

**Main Focus:** Graphical Interface (UI), User Experience (UX), and Audio.

---

## Phase 0: Setup and Initial Planning (All Together)

- [ ] **0.1 "Hello Pygame" Prototype:** Edit the main.py file to run your first hello world in pygame.
- [ ] **0.2 Internal API Design (Overview):** Participate in the discussion and definition of the main classes and interactions.

---

## Phase 1: Independent Foundation

- [ ] **1.B.1 Basic Pygame Setup:**
  - Set up the Pygame window, title, and main loop.
  - Define screen and board square sizes.
- [ ] **1.B.2 Asset Loading and Drawing:**
  - Implement an `AssetManager` function/class to load all piece PNG sprites (12 images) and any custom board image.
  - Create a `BoardRenderer` class (or similar) responsible for drawing the base board (light/dark squares) and the pieces in their positions.
- [ ] **1.B.3 Mouse Event System:**
  - Implement mouse click detection logic:
    - Identify which board square was clicked.
    - Detect "drag and drop" (click, drag, release).
  - **Selection Visual Feedback:** When a piece is clicked, draw a visual highlight on the selected square.
- [ ] **1.B.4 Basic Audio Logic:**
  - Set up the Pygame mixer.
  - Load and test a simple sound (e.g., for a click).

---

## Phase 2: Integration and Essential Features

- [ ] **2.B.1 Drawing Refinements:**
  - Improve piece drawing (centering, size adjustment).
  - Implement highlight of valid moves when a piece is selected (receiving legal moves from Developer A).
  - Implement highlight of the last move.
- [ ] **2.B.2 Status Messages:**
  - Display on-screen text messages: "White's Turn", "Black's Turn", "Check!", "Checkmate!", "Draw!".
- [ ] **2.B.3 Piece Animation:**
  - Implement smooth sliding animation for pieces (not "teleport").
- [ ] **2.B.4 Game Sounds:**
  - Integrate sounds for piece moves, captures, and check.

---

## Phase 3: Advanced Features and Polish

- [ ] **3.B.1 Pawn Promotion:**
  - Implement the UI for choosing the piece on pawn promotion (small pop-up window).
- [ ] **3.B.2 End Game Screens:**
  - Create dedicated screens for "Checkmate", "Draw", "Stalemate" with options for "New Game" or "Exit".
- [ ] **3.B.3 General Visual Refinement:**
  - Adjust colors, fonts, and layouts.
  - Consider additional visual themes (if time permits).
- [ ] **3.B.4 Enhanced Audio Feedback:**
  - Add background music (with option to turn on/off/volume).
  - Sounds for check, checkmate, etc.

---

## Phase 4: Final Polish and Distribution (All Together)

- [ ] **4.1 Integration Tests:** Participate in testing all features together.
- [ ] **4.2 Usability Tests:** Participate in gathering feedback from external users.
- [ ] **4.3 Error Handling and Robustness:** Contribute to exception handling.
- [ ] **4.4 Documentation:** Contribute to project documentation.
- [ ] **4.5 Packaging for Distribution:** Assist in creating executables with PyInstaller.
- [ ] **4.6 Release and Launch:** Participate in the game launch.
Battleship Game in Python

---Overview---
This is a terminal-based Battleship game implemented in Python.  
The player competes against an intelligent bot. Game state is tracked in CSV files, and the game displays boards after each move.

------

1. Input Format

---Player Ship Placement---
- Ships are placed on a 10×10 grid (rows and columns numbered 0–9).
- Coordinates are entered as comma-separated pairs for each ship:
- Multiple coordinates are separated by spaces.
- Ship sizes: 4, 3, 3, 2, 2, 2, 1, 1, 1, 1

---Player Moves---
- During gameplay, the player enters a move as a single coordinate:


2. Ship Placement Validation
When the player enters ship coordinates:
1. Correct size - number of coordinates matches the ship size.
2. Inside board - all coordinates are within 0–9 for rows and columns.
3. No touching - ships cannot touch each other, even diagonally.
4. Format check - input must follow "row,col" with integers.

Invalid inputs are rejected with an error message, and the player is prompted again.


3. Game State Update & Display
- All moves are tracked in "data/game_state.csv":
- Turn number
- Player move (coordinate + hit/miss)
- Bot move (coordinate + hit/miss)
- Current board state
- Boards are printed after each move:
- "." – unknown cell
- "X" – hit
- "O" – miss
- When a ship is destroyed:
- All surrounding cells are automatically marked as miss
- This ensures no adjacent ship placement conflicts


4. Bot Logic
- Random Mode: Initially selects untested cells randomly.
- Smart Follow-up: After first hit on a ship > size 1, bot selects adjacent cells.
- Axis Locking: After second consecutive hit on the same ship (> size 2), bot continues along the same axis until the ship is destroyed.
- When a ship is destroyed, bot returns to random mode.


5. Design Decisions & Trade-offs
- CSV tracking: Chosen for simplicity and visibility; may not scale for huge games but ideal for terminal-based 10×10 grid.
- Terminal display: Easier to debug and play quickly; no GUI implemented.
- Bot AI: Simple but effective; keeps the project beginner-friendly while still adding challenge.
- Modular structure: "ship_input.py", "bot_generation.py", "gameplay.py", and "utils.py" separated for clarity and maintainability.


Battleship Game in Python
Overview

This is a terminal based Battleship game implemented in Python.
The player competes against an intelligent bot.
The game state is tracked in CSV files, and the boards are displayed after each move.

1. Input Format

Player Ship Placement

Ships are placed on a 10×10 grid with rows and columns numbered from 0 to 9.

The player enters ship coordinates as comma separated pairs.
Multiple coordinates for one ship are separated by spaces.

Example
2,3 2,4 2,5

Ship sizes used in the game
4, 3, 3, 2, 2, 2, 1, 1, 1, 1

Player Moves

During gameplay, the player enters a single coordinate in the format
row,col

Example
3,4

2. Ship Placement Validation

When the player enters ship coordinates, the following checks are applied

Correct size
The number of coordinates must match the required ship size.

Inside board
All coordinates must be within the range 0 to 9 for both rows and columns.

No touching
Ships are not allowed to touch each other, including diagonally.

Format check
Each coordinate must follow the format row,col with integer values.

Invalid inputs are rejected with an error message, and the player is prompted to re enter the ship coordinates.


3. Game State Update and Display

All moves are recorded in the file data/game_state.csv.
Each record contains

• Turn number
• Player move with result hit or miss
• Bot move with result hit or miss
• Current flattened board state

Boards are printed after each move.

Board symbols used in the game

"." unknown cell
"X" hit
"O" miss

When a ship is completely destroyed, all surrounding cells are automatically marked as miss.
This prevents illegal adjacent ship placement.


Boards are printed after each move.

Board symbols used in the game

"." unknown cell
"X" hit
"O" miss

When a ship is completely destroyed, all surrounding cells are automatically marked as miss.
This prevents illegal adjacent ship placement.

4. Bot Logic

The bot uses three targeting modes.

Random Mode
The bot selects a random untested cell.

Smart Mode
After the first hit on a ship, the bot targets adjacent cells.

Axis Mode
After a second hit on the same ship, the bot determines the ship orientation and continues firing along the same axis until the ship is destroyed.

Once a ship is destroyed, the bot returns to random mode.

5. Design Decisions and Trade offs

CSV based tracking
Chosen for simplicity and transparency. It does not scale well for large games but is suitable for a 10×10 terminal game.

Terminal interface
Allows fast development and easy debugging without a graphical interface.

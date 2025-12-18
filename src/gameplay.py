import pandas as pd
import os
import random

BOARD_SIZE = 10


# Creates an empty game board filled with spaces.
def init_board():
    return [["." for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]



# Prints a board to the terminal with row and column numbers.
def print_board(board, title):
    print(f"\n{title}")
    print("  " + " ".join(str(i) for i in range(10)))
    for i, row in enumerate(board):
        print(f"{i} " + " ".join(row))


# Returns all neighboring cells around a coordinate.
def get_neighbors(r, c):
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < 10 and 0 <= nc < 10:
                neighbors.append((nr, nc))
    return neighbors


# Checks whether all cells of a ship have been hit.
def is_ship_destroyed(ship_cells, hits):
    return all(cell in hits for cell in ship_cells)


# Marks all surrounding cells of a destroyed ship as misses.
def mark_surroundings(board, ship_cells):
    for r, c in ship_cells:
        for nr, nc in get_neighbors(r, c):
            if board[nr][nc] == ".":
                board[nr][nc] = "O"


# Loads ships from CSV and groups them by ship_id.
def load_ships_grouped(csv_file):
    df = pd.read_csv(csv_file)
    ships = {}
    for ship_id, group in df.groupby("ship_id"):
        ships[ship_id] = set(zip(group.row, group.col))
    return ships


# Applies a move with ship grouping and tracks hits.
def apply_move(board, move, ships, hits):
    r, c = move

    for ship_id, cells in ships.items():
        if (r, c) in cells:
            board[r][c] = "X"
            hits.add((r, c))

            if is_ship_destroyed(cells, hits):
                mark_surroundings(board, cells)

            return "hit"

    if board[r][c] == ".":
        board[r][c] = "O"
    return "miss"


# Converts the board into a single string.
def flatten_board(board):
    return "".join(cell for row in board for cell in row)


# Saves the current game turn to the game_state CSV file.
def save_game_state(turn, player_move, bot_move, board):
    os.makedirs("data", exist_ok=True)
    row = {
        "turn": turn,
        "player_move": player_move,
        "bot_move": bot_move,
        "board": flatten_board(board)
    }

    path = "data/game_state.csv"
    if not os.path.exists(path):
        pd.DataFrame([row]).to_csv(path, index=False)
    else:
        df = pd.read_csv(path)
        pd.concat([df, pd.DataFrame([row])]).to_csv(path, index=False)


# Runs the full gameplay loop until one side wins.
def run_game():
    player_board = init_board()
    bot_board = init_board()

    player_ships = load_ships_grouped("data/player_ships.csv")
    bot_ships = load_ships_grouped("data/bot_ships.csv")

    player_hits = set()
    bot_hits = set()

    last_hits = []
    axis = None
    mode = "random"

    turn = 1
    print("\n GAME STARTED\n")

    while True:
        print_board(player_board, "Your View of Bot Board")
        print_board(bot_board, "Bot View of Your Board")

        move = input("Enter your move (row,col): ")
        try:
            r, c = map(int, move.strip().split(","))
        except:
            print("Invalid input format")
            continue

        result_player = apply_move(player_board, (r, c), bot_ships, player_hits)
        print(f"You: {result_player}")

        all_bot_cells = set().union(*bot_ships.values())
        if all_bot_cells.issubset(player_hits):
            print("YOU WIN")
            break

        br, bc = bot_choose_move(bot_board, last_hits, axis, mode)
        result_bot = apply_move(bot_board, (br, bc), player_ships, bot_hits)
        print(f"Bot shoots at {br},{bc}: {result_bot}")

        if result_bot == "hit":
            last_hits.append((br, bc))
            if len(last_hits) == 2:
                axis = determine_axis(last_hits[0], last_hits[1])
                mode = "axis"
            elif len(last_hits) == 1:
                mode = "smart"

        all_player_cells = set().union(*player_ships.values())
        if all_player_cells.issubset(bot_hits):
            print("BOT WINS")
            break

        for ship_id, cells in player_ships.items():
            if is_ship_destroyed(cells, bot_hits) and any(hit in last_hits for hit in cells):
                last_hits.clear()
                axis = None
                mode = "random"

        save_game_state(turn, f"{r},{c}:{result_player}", f"{br},{bc}:{result_bot}", player_board)
        turn += 1


# Returns valid adjacent cells around a hit cell.
def get_adjacent_cells(r, c, board):
    adj = []
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 10 and 0 <= nc < 10 and board[nr][nc] == ".":
            adj.append((nr, nc))
    return adj


# Determines the orientation of a ship based on two hits.
def determine_axis(hit1, hit2):
    r1, c1 = hit1
    r2, c2 = hit2
    return "horizontal" if r1 == r2 else "vertical"


# Returns the next possible cells along a known ship axis.
def get_next_on_axis(hit_coords, axis, board):
    candidates = []
    hit_coords = sorted(hit_coords)
    if axis == "horizontal":
        row = hit_coords[0][0]
        min_col = hit_coords[0][1]
        max_col = hit_coords[-1][1]
        if min_col-1 >= 0 and board[row][min_col-1] == ".":
            candidates.append((row, min_col-1))
        if max_col+1 < 10 and board[row][max_col+1] == ".":
            candidates.append((row, max_col+1))
    else:
        col = hit_coords[0][1]
        min_row = hit_coords[0][0]
        max_row = hit_coords[-1][0]
        if min_row-1 >= 0 and board[min_row-1][col] == ".":
            candidates.append((min_row-1, col))
        if max_row+1 < 10 and board[max_row+1][col] == ".":
            candidates.append((max_row+1, col))
    return candidates


# Chooses the bot move based on its current targeting mode.
def bot_choose_move(bot_board, last_hits, axis, mode):
    if mode == "random":
        empty = [(r,c) for r in range(10) for c in range(10) if bot_board[r][c] == "."]
        return random.choice(empty)
    elif mode == "smart":
        candidates = get_adjacent_cells(*last_hits[0], bot_board)
        return random.choice(candidates) if candidates else random.choice(
            [(r,c) for r in range(10) for c in range(10) if bot_board[r][c] == "."]
        )
    elif mode == "axis":
        candidates = get_next_on_axis(last_hits, axis, bot_board)
        return random.choice(candidates) if candidates else random.choice(
            [(r,c) for r in range(10) for c in range(10) if bot_board[r][c] == "."]
        )

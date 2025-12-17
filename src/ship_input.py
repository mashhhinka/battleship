import os
import pandas as pd

BOARD_SIZE = 10
SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]


# Converts user input text into a list of coordinate tuples.
# Example input format is "0,0 0,1 0,2".
# Parse a string like '0,0 0,1 0,2' into a list of tuples"""

def parse_coordinates(input_str):
    coords = []
    for part in input_str.strip().split():
        r, c = map(int, part.split(","))
        coords.append((r, c))
    return coords


# Checks that all coordinates are inside the game board boundaries.
def is_inside_board(coords):
    return all(0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE for r, c in coords)


# Checks that all ship cells are aligned in a single row or a single column.
def is_straight_line(coords):
    rows = {r for r, _ in coords}
    cols = {c for _, c in coords}
    return len(rows) == 1 or len(cols) == 1


# Checks that ship cells are placed consecutively without gaps.
def is_consecutive(coords):
    coords = sorted(coords)
    if len({r for r, _ in coords}) == 1:
        cols = [c for _, c in coords]
        return cols == list(range(min(cols), max(cols) + 1))
    else:
        rows = [r for r, _ in coords]
        return rows == list(range(min(rows), max(rows) + 1))


# Checks whether a ship touches any previously placed ship.
# Touching includes diagonal, vertical, and horizontal adjacency.
def touches_existing(coords, occupied):
    for r, c in coords:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if (r + dr, c + dc) in occupied:
                    return True
    return False


# Saves all player ships into a CSV file in the data folder.
def save_to_csv(ships):
    os.makedirs("data", exist_ok=True)

    data = []
    for ship_id, ship in enumerate(ships):
        for r, c in ship:
            data.append({"ship_id": ship_id, "row": r, "col": c})

    df = pd.DataFrame(data)
    df.to_csv("data/player_ships.csv", index=False)
    print(" Ships saved to data/player_ships.csv")


# Collects ship positions from the player.
# Validates input and ensures all placement rules are respected.
def collect_player_ships():
    print("Place your ships on a 10x10 board (rows & cols: 0–9)\n")

    all_ships = []
    occupied = set()

    for size in SHIP_SIZES:
        while True:
            try:
                user_input = input(f"Enter ship of size {size}: ")
                coords = parse_coordinates(user_input)

                if len(coords) != size:
                    print(" Wrong number of coordinates")
                    continue

                if not is_inside_board(coords):
                    print(" Ship is outside the board")
                    continue

                if not is_straight_line(coords) or not is_consecutive(coords):
                    print(" Ship must be straight and consecutive")
                    continue

                if touches_existing(coords, occupied):
                    print(" Ship touches another ship")
                    continue

                all_ships.append(coords)
                occupied.update(coords)
                break

            except Exception:
                print(" Invalid input format")

    save_to_csv(all_ships)

import os
import random
import pandas as pd

BOARD_SIZE = 10
SHIP_SIZES = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]


# Checks whether a ship touches any already placed ships.
# Touching includes diagonal, horizontal, and vertical adjacency.
# Check if a ship touches existing ships (including diagonals)

def touches_existing(coords, occupied):
    for r, c in coords:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if (r + dr, c + dc) in occupied:
                    return True
    return False


# Generates a single valid ship of a given size.
# The ship is placed randomly and must not touch other ships.
def generate_ship(size, occupied):
    """Generate a single valid ship of given size"""
    while True:
        orientation = random.choice(["horizontal", "vertical"])
        if orientation == "horizontal":
            r = random.randint(0, BOARD_SIZE - 1)
            c = random.randint(0, BOARD_SIZE - size)
            coords = [(r, c + i) for i in range(size)]
        else:  # vertical
            r = random.randint(0, BOARD_SIZE - size)
            c = random.randint(0, BOARD_SIZE - 1)
            coords = [(r + i, c) for i in range(size)]

        if not touches_existing(coords, occupied):
            return coords


# Generates all bot ships following the standard Battleship rules.
def generate_bot_ships():
    """Generate all bot ships following the rules"""
    all_ships = []
    occupied = set()

    for size in SHIP_SIZES:
        ship_coords = generate_ship(size, occupied)
        all_ships.append(ship_coords)
        occupied.update(ship_coords)

    return all_ships


# Saves bot ship coordinates into a CSV file.
def save_to_csv(ships, filename="data/bot_ships.csv"):
    os.makedirs("data", exist_ok=True)
    data = []
    for ship_id, ship in enumerate(ships):
        for r, c in ship:
            data.append({"ship_id": ship_id, "row": r, "col": c})
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f" Bot ships saved to {filename}")


# Generates bot ships and immediately saves them to a CSV file.
def generate_and_save_bot_ships():
    ships = generate_bot_ships()
    save_to_csv(ships)

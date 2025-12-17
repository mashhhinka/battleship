from src.ship_input import collect_player_ships
from src.bot_generation import generate_and_save_bot_ships
from src.gameplay import run_game


# This function is the main entry point of the program.
# It starts the game by collecting player ships and generating bot ships.
def main():
    print("================================")
    print("       BATTLESHIP GAME       ")
    print("================================\n")

    # Collects ship positions from the player and saves them to a CSV file.
    collect_player_ships()
    print("\n Player ships saved successfully!")

    # Generates random ship positions for the bot and saves them to a CSV file.
    generate_and_save_bot_ships()
    print("\n Bot ships generated successfully!")


from src.gameplay import (
    init_board,
    print_board,
    load_ships_grouped,
    apply_move
)

# This section is a temporary test loop for gameplay mechanics.
# It allows testing shooting logic before the final game loop is completed.
player_board = init_board()
bot_board = init_board()

bot_ships = load_ships_grouped("data/bot_ships.csv")

hits = set()

print("\n GAME STARTED\n")

while True:
    # Displays the current visible state of the bot board.
    print_board(player_board, "Your View of Bot Board")

    move = input("Enter your move (row,col): ")

    try:
        r, c = map(int, move.split(","))
    except:
        print("Invalid format")
        continue

    # Applies the player's move and updates the board and hit tracking.
    result = apply_move(player_board, (r, c), bot_ships, hits)
    print(f"Result: {result}")


# Starts the main gameplay loop defined in gameplay.py.
run_game()

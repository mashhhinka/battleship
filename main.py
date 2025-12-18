from src.ship_input import collect_player_ships
from src.bot_generation import generate_and_save_bot_ships
from src.gameplay import run_game


def main():
    print("================================")
    print("       BATTLESHIP GAME       ")
    print("================================\n")

    collect_player_ships()
    print("\nPlayer ships saved successfully!")

    generate_and_save_bot_ships()
    print("\nBot ships generated successfully!")

    run_game()


if __name__ == "__main__":
    main()

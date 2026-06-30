#!/bin/python3
# MasterMind
# by ICTROCN

import random

print("MasterMind")

# Lijst met kleuren per moeilijkheidsgraad
DIFFICULTY_LEVELS = {
    "1": {
        "naam":     "Makkelijk",
        "lengte":   3,
        "pogingen": 12,
        "kleuren":  ["Red", "Blue", "Yellow", "Purple", "Green"],
    },
    "2": {
        "naam":     "Normaal",
        "lengte":   4,
        "pogingen": 10,
        "kleuren":  ["Red", "Blue", "Yellow", "Purple", "Green"],
    },
    "3": {
        "naam":     "Moeilijk",
        "lengte":   5,
        "pogingen": 8,
        "kleuren":  ["Red", "Blue", "Yellow", "Purple", "Green", "Orange"],
    },
    "4": {
        "naam":     "Expert",
        "lengte":   6,
        "pogingen": 6,
        "kleuren":  ["Red", "Blue", "Yellow", "Purple", "Green", "Orange", "White", "Pink"],
    },
}


# Laad het admin wachtwoord uit een tekstbestand
def load_Password(filename="password.txt"):
    with open(filename) as f:
        return f.read().strip()


# Laad het admin wachtwoord bij het starten van het programma
ADMIN_PASSWORD = load_Password()


def choose_Difficulty():
    print("\n=== Kies een moeilijkheidsgraad ===")
    for key, level in DIFFICULTY_LEVELS.items():
        kleuren = ", ".join(level["kleuren"])
        print(
            f"  [{key}] {level['naam']}"
            f" — codelengte: {level['lengte']}"
            f", pogingen: {level['pogingen']}"
            f", kleuren: {kleuren}"
        )

    choice = ""
    while choice not in DIFFICULTY_LEVELS:
        choice = input(f"Jouw keuze (1-{len(DIFFICULTY_LEVELS)}): ").strip()
        if choice not in DIFFICULTY_LEVELS:
            print(f"Ongeldige keuze. Voer 1 t/m {len(DIFFICULTY_LEVELS)} in.")

    selected = DIFFICULTY_LEVELS[choice]
    print(
        f"\nGekozen: {selected['naam']} "
        f"(lengte: {selected['lengte']}, pogingen: {selected['pogingen']})\n"
    )
    return selected


def generate_Code(length, colors):
    return [random.choice(colors) for _ in range(length)]


def get_Feedback(secret, guess):
    black_Pegs = sum(s == g for s, g in zip(secret, guess))

    secret_Counts = {}
    guess_Counts = {}

    for s, g in zip(secret, guess):
        if s != g:
            secret_Counts[s] = secret_Counts.get(s, 0) + 1
            guess_Counts[g] = guess_Counts.get(g, 0) + 1

    white_Pegs = sum(
        min(secret_Counts.get(d, 0), guess_Counts.get(d, 0))
        for d in guess_Counts
    )

    return black_Pegs, white_Pegs


# Controleer of de speler admin is
def admin_Check():
    password = input("Enter admin password: ").strip()
    if password == ADMIN_PASSWORD:
        print("Access granted.")
        return True
    else:
        print("Wrong password. Access denied.")
        return False


# Toont de geheime code alleen als de speler admin is
def show_Secret(mystery, is_Admin):
    if is_Admin:
        print(f"Secret code: {mystery}")
    else:
        print("Access denied. Admin only.")


def play_Mastermind(is_Admin):
    # Moeilijkheidsgraad kiezen vóór het spel start
    settings = choose_Difficulty()

    code_Length = settings["lengte"]
    max_Pogingen = settings["pogingen"]
    colors = settings["kleuren"]

    print("Welcome to Mastermind!")
    print(f"Guess the {code_Length} colors. Choose from: {', '.join(colors)}")
    print(f"You have {max_Pogingen} attempts.")

    secret_Code = generate_Code(code_Length, colors)

    for attempt in range(1, max_Pogingen + 1):
        guess = []
        valid_Guess = False
        while not valid_Guess:
            raw_input = input(
                f"Attempt {attempt}/{max_Pogingen} ({', '.join(colors)}): "
            ).strip()

            if raw_input.lower() == "cheat":
                show_Secret(secret_Code, is_Admin)
                continue

            guess = [color.capitalize() for color in raw_input.split()]

            valid_Guess = len(guess) == code_Length and all(c in colors for c in guess)
            if not valid_Guess:
                print(
                    f"Invalid input. Enter exactly {code_Length} colors from: "
                    f"{', '.join(colors)}"
                )

        black, white = get_Feedback(secret_Code, guess)
        print(
            f"Black pegs (correct position): {black}, "
            f"White pegs (wrong position): {white}"
        )

        if black == code_Length:
            print(
                f"Congratulations! You guessed the code: "
                f"{' '.join(secret_Code)}"
            )
            return

    print(
        f"Sorry, you've used all attempts. "
        f"The correct code was: {' '.join(secret_Code)}"
    )


if __name__ == "__main__":
    print("=== Admin check ===")
    is_Admin = admin_Check()

    again = 'Y'
    while again == 'Y':
        play_Mastermind(is_Admin)
        again = input("Play again (Y/N) ?").upper()
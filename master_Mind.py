#!/bin/python3
# MasterMind
# by ICTROCN

import random

print("MasterMind")

COLORS = ["Red", "Blue", "Yellow", "Purple", "Green"]
CODE_LENGTH = 4
MAX_ATTEMPTS = 10
MAX_HINTS = 2


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


def show_Hints(secret_Code, revealed_Positions):
    hint = []

    for position in range(len(secret_Code)):
        if position in revealed_Positions:
            hint.append(secret_Code[position])
        else:
            hint.append("_")

    print("Hint:", " ".join(hint))


def give_Hint(secret_Code, revealed_Positions, hints_Used):
    if hints_Used >= MAX_HINTS:
        print("Je hebt alle hints al gebruikt.")
        return hints_Used

    hidden_Positions = []

    for position in range(len(secret_Code)):
        if position not in revealed_Positions:
            hidden_Positions.append(position)

    position = random.choice(hidden_Positions)
    revealed_Positions[position] = secret_Code[position]
    hints_Used += 1

    print(f"Hint {hints_Used}/{MAX_HINTS}: positie {position + 1} is bekend.")
    show_Hints(secret_Code, revealed_Positions)

    return hints_Used


def play_Mastermind():
    print("Welcome to Mastermind!")
    print(f"Guess the {CODE_LENGTH} colors. Choose from: {', '.join(COLORS)}")
    print(f"You have {MAX_ATTEMPTS} attempts.")
    print(f"Typ 'hint' voor een hint. Je hebt maximaal {MAX_HINTS} hints.")

    secret_Code = generate_Code(CODE_LENGTH, COLORS)
    revealed_Positions = {}
    hints_Used = 0

    for attempt in range(1, MAX_ATTEMPTS + 1):
        guess = []
        valid_Guess = False

        while not valid_Guess:
            raw_input = input(
                f"Attempt {attempt}/{MAX_ATTEMPTS} ({', '.join(COLORS)}): "
            ).strip()

            if raw_input.lower() == "hint":
                hints_Used = give_Hint(
                    secret_Code,
                    revealed_Positions,
                    hints_Used
                )
                continue

            guess = [color.capitalize() for color in raw_input.split()]

            valid_Guess = (
                len(guess) == CODE_LENGTH
                and all(c in COLORS for c in guess)
            )

            if not valid_Guess:
                print(
                    f"Invalid input. Enter exactly {CODE_LENGTH} colors from: "
                    f"{', '.join(COLORS)}"
                )

        black, white = get_Feedback(secret_Code, guess)
        print(
            f"Black pegs (correct position): {black}, "
            f"White pegs (wrong position): {white}"
        )

        if black == CODE_LENGTH:
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
    again = "Y"
    while again == "Y":
        play_Mastermind()
        again = input("Play again (Y/N) ?").upper()
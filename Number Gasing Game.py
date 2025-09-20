import random
import mysql.connector
from datetime import datetime

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",          
        password="943pradip@A",
        database="game_db"
    )
    return conn   

def save_score(player_name, difficulty, score):
    conn = get_connection()   
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO leaderboard (player_name, difficulty, score, date_played) VALUES (%s, %s, %s, %s)",
        (player_name, difficulty, score, datetime.now())
    )
    conn.commit()
    conn.close()

def show_leaderboard(difficulty_filter=None):
    conn = get_connection()
    cursor = conn.cursor()

    if difficulty_filter:
        cursor.execute(
            "SELECT player_name, difficulty, score, date_played FROM leaderboard WHERE difficulty=%s ORDER BY score DESC LIMIT 5",
            (difficulty_filter,)
        )
        print(f"\n Leaderboard (Top 5 {difficulty_filter} Scores) ")
    else:
        cursor.execute(
            "SELECT player_name, difficulty, score, date_played FROM leaderboard ORDER BY score DESC LIMIT 5"
        )
        print("\n Leaderboard (Top 5 Overall Scores) ")

    rows = cursor.fetchall()
    conn.close()

    print("-" * 70)
    print(f"{'Player':<15} {'Difficulty':<12} {'Score':<8} {'Date'}")
    print("-" * 70)

    for row in rows:
        print(f"{row[0]:<15} {row[1]:<12} {row[2]:<8} {row[3]}")
    print("-" * 70)


class NumberGuessingGame:
    def __init__(self, player_name):
        self.player_name = player_name
        self.difficulty = None
        self.lower = 1
        self.upper = 100
        self.attempts = 5
        self.number_to_guess = None
        self.score = 0

    def set_difficulty(self):
        print("\nChoose Difficulty Level:")
        print("1. Easy (1-50, 10 attempts)")
        print("2. Medium (1-100, 7 attempts)")
        print("3. Hard (1-200, 5 attempts)")

        choice = input("Enter choice (1/2/3): ")

        if choice == "1":
            self.difficulty = "Easy"
            self.upper = 50
            self.attempts = 10
            self.max_score = 100
        elif choice == "2":
            self.difficulty = "Medium"
            self.upper = 100
            self.attempts = 7
            self.max_score = 150
        else:
            self.difficulty = "Hard"
            self.upper = 200
            self.attempts = 5
            self.max_score = 200

        self.number_to_guess = random.randint(self.lower, self.upper)

    def play_round(self):
        print(f"\n Hello {self.player_name}! Difficulty: {self.difficulty}")
        print(f"Guess the number between {self.lower} and {self.upper}.")
        print(f"You have {self.attempts} attempts.\n")

        for attempt in range(1, self.attempts + 1):
            try:
                guess = int(input(f"Attempt {attempt}: Enter your guess → "))
            except ValueError:
                print(" Invalid input! Please enter a number.")
                continue

            if guess == self.number_to_guess:
                self.score = self.max_score - (attempt - 1) * 10
                print(f" Correct! You guessed it in {attempt} attempts. Score: {self.score}")
                break
            elif guess < self.number_to_guess:
                print(" Too low!")
            else:
                print(" Too high!")
        else:
            print(f" Game Over! The number was {self.number_to_guess}.")
            self.score = 0

        save_score(self.player_name, self.difficulty, self.score)
        show_leaderboard(self.difficulty)

if __name__ == "__main__":
    print(" Welcome to the Number Guessing Game with Leaderboard!\n")
    name = input("Enter your name: ")

    while True:
        game = NumberGuessingGame(name)
        game.set_difficulty()
        game.play_round()

        again = input("\nDo you want to play again? (y/n): ").lower()
        if again != "y":
            print("\nThank you for playing! Final Leaderboard:")
            show_leaderboard()
            break
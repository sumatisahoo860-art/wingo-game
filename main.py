import random
import time

class ColorPredictionGame:
    def __init__(self, initial_balance=1000):
        self.balance = initial_balance
        self.game_history = []
        self.colors = ["Green", "Red", "Violet"]

    def display_status(self):
        print("\n" + "="*40)
        print(f"💰 Current Balance: ₹{self.balance}")
        print("="*40)

    def get_system_outcome(self):
        """
        Simulates realistic 51 Game probabilities:
        Green: ~45% | Red: ~45% | Violet: ~10%
        """
        rand_val = random.random()
        if rand_val < 0.45:
            return "Green"
        elif rand_val < 0.90:
            return "Red"
        else:
            return "Violet"

    def play_round(self):
        self.display_status()
        
        # Step 1: Input Bet Amount
        try:
            bet_amount = int(input("Enter Bet Amount (Min ₹10): "))
            if bet_amount < 10:
                print("❌ Minimum bet amount is ₹10!")
                return
            if bet_amount > self.balance:
                print("❌ Insufficient balance for this bet!")
                return
        except ValueError:
            print("❌ Invalid input! Please enter a valid number.")
            return

        # Step 2: Input Color Choice
        print("\nChoose your Color:")
        print("1. Green (2x Return)")
        print("2. Red (2x Return)")
        print("3. Violet (4.5x Return)")
        choice = input("Enter choice (1/2/3 or Name): ").strip().title()

        # Map number choices to colors
        choice_map = {"1": "Green", "2": "Red", "3": "Violet"}
        player_choice = choice_map.get(choice, choice)

        if player_choice not in self.colors:
            print("❌ Invalid color selection!")
            return

        # Deduct bet money
        self.balance -= bet_amount
        print(f"\n🎰 Placing ₹{bet_amount} on {player_choice}...")
        print("Waiting for game timer countdown...")
        time.sleep(1.5)  # Simulates game processing delay

        # Step 3: Draw Result
        winning_color = self.get_system_outcome()
        print(f"🎲 Result Color is: {winning_color}")

        # Step 4: Calculate Payouts
        if player_choice == winning_color:
            if winning_color == "Violet":
                winnings = int(bet_amount * 4.5)
            else:
                winnings = bet_amount * 2
            
            self.balance += winnings
            print(f"🎉 Congratulations! You WON ₹{winnings}!")
        else:
            print("😞 You LOST this round! Better luck next time.")

        # Save to Game History
        self.game_history.append({"bet": bet_amount, "chosen": player_choice, "result": winning_color})

    def show_history(self):
        if not self.game_history:
            print("\n📜 No history available yet.")
            return
        print("\n📜 --- GAME HISTORY ---")
        for idx, record in enumerate(self.game_history[-5:], 1):  # Shows last 5 games
            print(f"Game {idx}: Bet ₹{record['bet']} on {record['chosen']} -> Result: {record['result']}")

# --- Main Game Loop ---
if __name__ == "__main__":
    print("Welcome to 51 Game (Color Prediction Server Simulator)")
    game = ColorPredictionGame(initial_balance=1000)

    while True:
        print("\n[1] Play Game  |  [2] View History  |  [3] Exit")
        main_choice = input("Select an option: ").strip()

        if main_choice == "1":
            game.play_round()
            if game.balance < 10:
                print("\n💥 Game Over! You don't have enough money to place a minimum bet.")
                break
        elif main_choice == "2":
            game.show_history()
        elif main_choice == "3":
            print("\nThank you for playing! Exiting...")
            break
        else:
            print("❌ Invalid option. Choose 1, 2, or 3.")
            

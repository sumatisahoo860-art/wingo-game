import random
import time

class ColourTradingGame:
    def __init__(self):
        # शुरुआत में यूज़र का बैलेंस ₹1000 सेट किया गया है
        self.wallet_balance = 1000.0
        self.available_colours = ["Green", "Red", "Violet"]
        self.round_number = 1

    def display_status(self):
        print("\n" + "="*40)
        print(f"🎮 ROUND NUMBER: {self.round_number}")
        print(f"💰 WALLET BALANCE: ₹{self.wallet_balance:.2f}")
        print("="*40)

    def get_user_bet(self):
        # 1. कलर का चुनाव
        print("\nAvailable Colours: [1] Green  [2] Red  [3] Violet")
        while True:
            try:
                choice = int(input("Select colour number (1-3): "))
                if choice in:
                    selected_colour = self.available_colours[choice - 1]
                    break
                print("❌ Invalid choice! Please select 1, 2, or 3.")
            except ValueError:
                print("❌ Please enter a valid number.")

        # 2. बेट की रकम का चुनाव
        while True:
            try:
                amount = float(input(f"Enter bet amount (Min ₹10, Max ₹{self.wallet_balance}): ₹"))
                if amount < 10:
                    print("❌ Minimum bet amount is ₹10.")
                elif amount > self.wallet_balance:
                    print("❌ Insufficient balance in your wallet!")
                else:
                    break
            except ValueError:
                print("❌ Please enter a valid amount.")

        return selected_colour, amount

    def run_timer(self, seconds=5):
        # लाइव ऐप की तरह काउंटडाउन एनीमेशन
        print("\n⏳ Locking bets... Counting down to result:")
        for i in range(seconds, 0, -1):
            print(f"⏰ Result in: {i}s...", end="\r")
            time.sleep(1)
        print("⏰ Result in: 0s... Processing!       \n")

    def calculate_result(self, user_colour, bet_amount):
        # RNG (Random Number Generation) के आधार पर जीतने वाला कलर चुनना
        # रैंडम एल्गोरिदम में वॉयलेट आने की संभावना कम रखी जाती है (जैसे असली ऐप्स में होता है)
        winning_colour = random.choices(self.available_colours, weights=[45, 45, 10], k=1)[0]
        
        print(f"🎯 Winning Colour Is: {winning_colour.upper()}")

        if user_colour == winning_colour:
            # वॉयलेट (Violet) पर अक्सर ज़्यादा रिटर्न (जैसे 4.5x) मिलता है
            if winning_colour == "Violet":
                winnings = bet_amount * 4.5
            else:
                winnings = bet_amount * 2.0 # ग्रीन/रेड पर 2x रिटर्न
            
            self.wallet_balance += (winnings - bet_amount) # नेट प्रॉफिट जोड़ना
            print(f"🎉 CONGRATULATIONS! You guessed right.")
            print(f"➕ ₹{winnings:.2f} credited to your wallet.")
        else:
            self.wallet_balance -= bet_amount
            print(f"💔 YOU LOST! Better luck next time.")
            print(f"➖ ₹{bet_amount:.2f} deducted from your wallet.")

        self.round_number += 1

    def start_game_loop(self):
        print("📢 Welcome to Python Colour Trading Simulator!")
        
        while self.wallet_balance >= 10:
            self.display_status()
            
            # यूज़र से बेट लेना
            chosen_colour, bet_amt = self.get_user_bet()
            print(f"🔒 Bet Locked: ₹{bet_amt} on {chosen_colour}")
            
            # टाइमर चलाना
            self.run_timer(5)
            
            # रिज़ल्ट प्रोसेस करना
            self.calculate_result(chosen_colour, bet_amt)
            
            # दोबारा खेलने की चॉइस
            play_again = input("\nDo you want to play next round? (yes/no): ").strip().lower()
            if play_again not in ['y', 'yes']:
                print("\n👋 Thank you for playing!")
                break
        else:
            print("\n🚨 GAME OVER! Your balance is less than the minimum bet amount (₹10).")
            print("Please top up your wallet.")

# गेम शुरू करने के लिए ऑब्जेक्ट बनाकर रन करना
if __name__ == "__main__":
    game = ColourTradingGame()
    game.start_game_loop()
    

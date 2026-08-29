import random
import time

def start_wingo_game():
    print("--- 91 Club स्टाइल Wingo गेम सिम्युलेटर में आपका स्वागत है ---")
    balance = 1000  # शुरुआती वर्चुअल बैलेंस
    
    colors = {
        'Red': [2, 4, 6, 8],
        'Green': [1, 3, 7, 9],
        'Violet': [0, 5]
    }
    
    while balance > 0:
        print(f"\nआपका वर्तमान बैलेंस: ₹{balance}")
        print("चुनें: [1] Green  [2] Red  [3] Violet")
        
        choice = input("अपना विकल्प चुनें (1/2/3) या बाहर निकलने के लिए 'q' दबाएं: ")
        if choice.lower() == 'q':
            print("खेलने के लिए धन्यवाद!")
            break
            
        if choice not in ['1', '2', '3']:
            print("अवैध विकल्प! कृपया सही नंबर चुनें।")
            continue
            
        try:
            bet_amount = int(input("अपनी बेट राशि दर्ज करें (₹): "))
            if bet_amount > balance or bet_amount <= 0:
                print("अमान्य राशि या अपर्याप्त बैलेंस!")
                continue
        except ValueError:
            print("कृपया केवल नंबर दर्ज करें।")
            continue
            
        # प्रेडिक्शन का मिलान सेट करना
        predicted_color = 'Green' if choice == '1' else 'Red' if choice == '2' else 'Violet'
        
        print("\nलॉटरी परिणाम आ रहा है... (3 सेकंड रुकें)")
        time.sleep(3)
        
        # 0 से 9 के बीच रैंडम नंबर जनरेट करना
        winning_number = random.randint(0, 9)
        winning_color = ""
        
        for color, numbers in colors.items():
            if winning_number in numbers:
                winning_color = color
                
        print(f"➜ परिणाम संख्या: {winning_number} ({winning_color})")
        
        # जीत या हार का फैसला
        if predicted_color == winning_color:
            if winning_color == 'Violet':
                win_multiplier = 4.5  # वायलेट के लिए ज्यादा रिवॉर्ड
            else:
                win_multiplier = 2.0
                
            winnings = int(bet_amount * win_multiplier)
            balance += (winnings - bet_amount)
            print(f"🎉 बधाई हो! आप जीत गए। आपको मिले: ₹{winnings}")
        else:
            balance -= bet_amount
            print("❌ ओहो! आपका अनुमान गलत था। आप यह बेट हार गए।")
            
    if balance <= 0:
        print("\nआपका बैलेंस खत्म हो गया है! गेम समाप्त।")

# गेम शुरू करने के लिए रन करें
if __name__ == "__main__":
    start_wingo_game()
    

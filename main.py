import os
import threading
import time
from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# रेंडर सर्वर को चालू रखने के लिए Flask वेब ऐप
app = Flask(__name__)


@app.route("/")
def home():
    return "Bot is running perfectly in the background!"


def run_full_automation():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    print("🚀 बैकग्राउंड में ब्राउज़र शुरू हो रहा है...")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)

    try:
        # --- चरण 1: लॉगिन प्रक्रिया ---
        print("🔗 लॉगिन पेज पर जा रहे हैं...")
        driver.get("https://51gameq.com")
        time.sleep(5)

        phone_input = wait.until(
            EC.presence_of_element_located((By.NAME, "phone"))
        )
        password_input = driver.find_element(By.NAME, "password")

        # ⚠️ अपना सही विवरण डालें
        phone_input.send_keys("YOUR_PHONE_NUMBER")
        password_input.send_keys("YOUR_PASSWORD")

        login_button = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Login')]"
        )
        login_button.click()
        print("✅ लॉगिन प्रक्रिया पूरी हुई।")
        time.sleep(6)

        # --- चरण 2: गेम पेज पर जाना ---
        print("🎮 WinGo गेम पेज पर जा रहे हैं...")
        driver.get("https://51gameq.com...")  # ⚠️ सही गेम URL डालें
        time.sleep(5)

        # --- चरण 3: डेटा निकालने का लगातार लूप ---
        print("📊 लगातार डेटा मॉनिटरिंग एक्टिव है...")
        while True:
            try:
                try:
                    timer_element = driver.find_element(
                        By.XPATH, "//div[contains(@class, 'Time remaining')]"
                    )
                    print(f"⏱️ टाइमर स्थिति: {timer_element.text}")
                except Exception:
                    pass

                rows = driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class, 'Game history')]//table//tr",
                )
                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) >= 4:
                        print(
                            f"🔹 Period: {cols[0].text} | Number: {cols[1].text} | Size: {cols[2].text}"
                        )

                time.sleep(10)  # हर 10 सेकंड में डेटा चेक करें
            except Exception as loop_error:
                print(f"लूप एरर: {loop_error}")
                time.sleep(5)

    except Exception as e:
        print(f"❌ मुख्य एरर: {e}")
    finally:
        driver.quit()


# बॉट स्क्रिप्ट को अलग थ्रेड (Thread) में चलाना ताकि वेब सर्वर डिस्टर्ब न हो
def start_bot_thread():
    bot_thread = threading.Thread(target=run_full_automation)
    bot_thread.daemon = True
    bot_thread.start()


if __name__ == "__main__":
    start_bot_thread()
    # रेंडर के पोर्ट पर वेब सर्वर चालू करना
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    

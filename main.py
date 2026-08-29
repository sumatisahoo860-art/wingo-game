import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def run_full_automation():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    print("🚀 ब्राउज़र शुरू हो रहा है...")
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

        # ⚠️ अपनी डिटेल्स यहाँ डालें
        phone_input.send_keys("YOUR_PHONE_NUMBER")
        password_input.send_keys("YOUR_PASSWORD")

        login_button = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Login')]"
        )
        login_button.click()
        print("✅ लॉगिन सफल रहा!")
        time.sleep(6)

        # --- चरण 2: गेम पेज पर जाना ---
        print("🎮 WinGo गेम पेज पर जा रहे हैं...")
        driver.get("https://51gameq.com...")  # ⚠️ अपनी सही गेम URL डालें
        time.sleep(5)

        # --- चरण 3: लगातार डेटा निकालने के लिए लूप (Loop) ---
        print("📊 लगातार डेटा मॉनिटरिंग शुरू की जा रही है...")
        while True:
            try:
                # टाइमर की स्थिति पढ़ें
                try:
                    timer_element = driver.find_element(
                        By.XPATH, "//div[contains(@class, 'Time remaining')]"
                    )
                    print(f"⏱️ टाइमर: {timer_element.text}")
                except Exception:
                    pass

                # गेम इतिहास का डेटा निकालें
                rows = driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class, 'Game history')]//table//tr",
                )
                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) >= 4:
                        print(
                            f"🔹 Period: {cols.text} | Number: {cols.text} | Size: {cols.text}"
                        )

                # सर्वर को एक्टिव रखने और अगले अपडेट के लिए 10 सेकंड रुकें
                time.sleep(10)

            except Exception as loop_error:
                print(f"लूप के अंदर एरर आया: {loop_error}")
                time.sleep(5)

    except Exception as e:
        print(f"❌ मुख्य ऑटोमेशन में एरर आया: {e}")
    finally:
        print("🛑 ब्राउज़र बंद हो रहा है...")
        driver.quit()


if __name__ == "__main__":
    run_full_automation()
    

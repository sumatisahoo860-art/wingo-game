import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def run_full_automation():
    # Render.com क्लाउड सर्वर के लिए क्रोम सेटिंग्स
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # बिना स्क्रीन के बैकग्राउंड में चलाने के लिए
    chrome_options.add_argument("--no-sandbox")  # सर्वर पर परमिशन एरर से बचने के लिए
    chrome_options.add_argument("--disable-dev-shm-usage")  # कम मेमोरी/क्रैश से बचने के लिए
    chrome_options.add_argument("--window-size=1920,1080")  # वर्चुअल स्क्रीन साइज सेट करना

    print("ब्राउज़र शुरू किया जा रहा है...")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)

    try:
        # ========================================================
        # चरण 1: लॉगिन प्रक्रिया
        # ========================================================
        print("लॉगिन पेज पर जा रहे हैं...")
        driver.get("https://51gameq.com")
        time.sleep(5)

        # मोबाइल इनपुट बॉक्स के लोड होने का इंतज़ार करें
        print("लॉगिन एलिमेंट्स ढूंढ रहे हैं...")
        phone_input = wait.until(
            EC.presence_of_element_located((By.NAME, "phone"))
        )
        password_input = driver.find_element(By.NAME, "password")

        # अपनी सही क्रेडेंशियल यहाँ डालें
        phone_input.send_keys("YOUR_PHONE_NUMBER")
        password_input.send_keys("YOUR_PASSWORD")

        # लॉगिन बटन ढूंढकर क्लिक करें
        login_button = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Login')]"
        )
        login_button.click()
        print("लॉगिन बटन पर क्लिक कर दिया गया है।")

        # लॉगिन प्रोसेस पूरा होने के लिए रुकें
        time.sleep(5)

        # ========================================================
        # चरण 2: गेम पेज (WinGo) पर जाना
        # ========================================================
        print("गेम पेज पर नेविगेट कर रहे हैं...")
        driver.get("https://51gameq.com...")  # यहाँ अपनी सही गेम URL डालें
        time.sleep(5)

        # ========================================================
        # चरण 3: टाइमर की जांच
        # ========================================================
        try:
            timer_element = driver.find_element(
                By.XPATH, "//div[contains(@class, 'Time remaining')]"
            )
            print(f"वर्तमान टाइमर स्थिति: {timer_element.text}")
        except Exception:
            print("चेतावनी: टाइमर एलिमेंट पेज पर नहीं मिला।")

        # ========================================================
        # चरण 4: गेम इतिहास (Game History) का डेटा निकालना
        # ========================================================
        print("\n--- गेम इतिहास डेटा निकाला जा रहा है ---")

        # टेबल कतारों (Rows) को ढूंढें
        rows = driver.find_elements(
            By.XPATH, "//div[contains(@class, 'Game history')]//table//tr"
        )

        game_records = []

        for row in rows:
            try:
                cols = row.find_elements(By.TAG_NAME, "td")

                if len(cols) >= 4:
                    period = cols[0].text
                    number = cols[1].text
                    big_small = cols[2].text
                    color = cols[3].text

                    record = {
                        "Period": period,
                        "Number": number,
                        "Big_Small": big_small,
                        "Color": color,
                    }
                    game_records.append(record)

                    print(
                        f"Period: {period} | Number: {number} | Result: {big_small} | Color: {color}"
                    )
            except Exception:
                continue

        print(
            f"\nसफलतापूर्वक {len(game_records)} रिकॉर्ड्स इतिहास से निकाले गए।"
        )

    except Exception as global_error:
        print(f"ऑटोमेशन के दौरान त्रुटि आई: {global_error}")

    finally:
        print("ब्राउज़र बंद किया जा रहा है...")
        driver.quit()


if __name__ == "__main__":
    run_full_automation()
                    

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def run_full_automation():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # बिना स्क्रीन के बैकग्राउंड में चलाने के लिए
    chrome_options.add_argument("--no-sandbox")  # सर्वर पर परमिशन एरर से बचने के लिए
    chrome_options.add_argument("--disable-dev-shm-usage")  # कम मेमोरी क्रैश से बचने के लिए
    chrome_options.add_argument("--window-size=1920,1080")

    # रेंडर क्लाउड सर्वर पर क्रोम और ड्राइवर का पाथ (रास्ता)
    chrome_options.binary_location = (
        "/opt/render/project/.render/chrome/chrome"
    )
    chrome_service = Service(
        executable_path="/opt/render/project/.render/chromedriver/chromedriver"
    )

    print("🚀 रेंडर क्लाउड पर क्रोम शुरू हो रहा है...")
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
    wait = WebDriverWait(driver, 15)

    try:
        # ========================================================
        # चरण 1: लॉगिन प्रक्रिया (जो स्क्रीनशॉट 1 में था)
        # ========================================================
        print("🔗 लॉगिन पेज पर जा रहे हैं...")
        driver.get("https://51gameq.com")
        time.sleep(5)

        print("📝 मोबाइल और पासवर्ड इनपुट बॉक्स ढूंढ रहे हैं...")
        phone_input = wait.until(
            EC.presence_of_element_located((By.NAME, "phone"))
        )
        password_input = driver.find_element(By.NAME, "password")

        # ⚠️ यहाँ अपना असली नंबर और पासवर्ड बदलें
        phone_input.send_keys("YOUR_PHONE_NUMBER")
        password_input.send_keys("YOUR_PASSWORD")

        # लॉगिन बटन पर क्लिक करें
        login_button = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Login')]"
        )
        login_button.click()
        print("✅ लॉगिन बटन पर क्लिक किया गया।")
        time.sleep(6)

        # ========================================================
        # चरण 2: मुख्य होम पेज पर जाना
        # ========================================================
        print("🏠 मुख्य होम पेज लोड हो रहा है...")
        driver.get("https://51gameq.com")
        time.sleep(5)

        # ========================================================
        # चरण 3: WinGo गेम पेज (जो स्क्रीनशॉट 2 में था)
        # ========================================================
        print("🎮 WinGo गेम पेज पर जा रहे हैं...")
        driver.get("https://51gameq.comsaasl...")  # ⚠️ यहाँ अपनी सही गेम URL डालें
        time.sleep(5)

        # टाइमर बॉक्स का टेक्स्ट पढ़ें (Time remaining)
        try:
            timer_element = driver.find_element(
                By.XPATH, "//div[contains(@class, 'Time remaining')]"
            )
            print(f"⏱️ वर्तमान टाइमर स्थिति: {timer_element.text}")
        except Exception:
            print("⚠️ टाइमर एलिमेंट पेज पर नहीं मिला।")

        # ========================================================
        # चरण 4: गेम इतिहास (Game History) का डेटा निकालना (जो स्क्रीनशॉट 3 में था)
        # ========================================================
        print("\n📊 गेम इतिहास डेटा निकाला जा रहा है...")

        # टेबल की सभी कतारों (Rows) को ढूंढें
        rows = driver.find_elements(
            By.XPATH, "//div[contains(@class, 'Game history')]//table//tr"
        )

        for row in rows:
            try:
                # रो के अंदर मौजूद सभी कॉलम्स (td) को ढूंढें
                cols = row.find_elements(By.TAG_NAME, "td")

                if len(cols) >= 4:
                    period = cols[0].text  # पीरियड नंबर (जैसे: 20260829100052662)
                    number = cols[1].text  # नंबर (जैसे: 8)
                    big_small = cols[2].text  # बिग या स्मॉल (जैसे: Big)
                    color = cols[3].text  # कलर का नाम

                    print(
                        f"🔹 Period: {period} | Number: {number} | Result: {big_small} | Color: {color}"
                    )
            except Exception:
                continue

    except Exception as e:
        print(f"❌ ऑटोमेशन के दौरान त्रुटि आई: {e}")

    finally:
        # काम पूरा होने के बाद ब्राउज़र बंद करें
        print("🛑 काम पूरा हुआ, ब्राउज़र बंद किया जा रहा है...")
        driver.quit()


if __name__ == "__main__":
    run_full_automation()
                    

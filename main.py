import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def run_full_automation():
    # 1. ब्राउज़र शुरू करें
    driver = webdriver.Chrome()
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    try:
        # ========================================================
        # चरण 1: लॉगिन प्रक्रिया
        # ========================================================
        print("लॉगिन पेज पर जा रहे हैं...")
        driver.get("https://51gameq.com")  # अपनी सही लॉगिन URL डालें
        time.sleep(3)

        # मोबाइल और पासवर्ड इनपुट बॉक्स ढूंढें (Xpath को अपनी आवश्यकतानुसार बदलें)
        phone_input = wait.until(
            EC.presence_of_element_input((By.NAME, "phone"))
        )
        password_input = driver.find_element(By.NAME, "password")

        # अपनी क्रेडेंशियल डालें
        phone_input.send_keys("YOUR_PHONE_NUMBER")
        password_input.send_keys("YOUR_PASSWORD")

        # लॉगिन बटन पर क्लिक करें
        login_button = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Login')]"
        )
        login_button.click()
        print("लॉगिन बटन पर क्लिक किया गया।")

        # लॉगिन पूरा होने और होम पेज लोड होने के लिए रुकें
        time.sleep(5)

        # ========================================================
        # चरण 2: गेम पेज (WinGo) पर नेविगेट करना
        # ========================================================
        print("गेम पेज पर रीडायरेक्ट हो रहे हैं...")
        # आप सीधे गेम का URL डाल सकते हैं या होम पेज से WinGo बटन पर क्लिक करा सकते हैं
        driver.get("https://51gameq.com...")  # अपनी सही गेम URL डालें
        time.sleep(5)

        # ========================================================
        # चरण 3: टाइमर और मुख्य एलिमेंट्स की जांच
        # ========================================================
        try:
            # टाइमर बॉक्स का टेक्स्ट पढ़ें (Time remaining)
            timer_element = driver.find_element(
                By.XPATH, "//div[contains(@class, 'Time remaining')]"
            )
            print(f"वर्तमान टाइमर स्थिति: {timer_element.text}")
        except Exception:
            print("टाइमर एलिमेंट नहीं मिला।")

        # ========================================================
        # चरण 4: गेम इतिहास (Game History) टेबल का डेटा निकालना
        # ========================================================
        print("\n--- गेम इतिहास डेटा निकाला जा रहा है ---")

        # टेबल की सभी कतारों (Rows) को ढूंढें
        # नोट: वेबसाइट के वास्तविक HTML स्ट्रक्चर के अनुसार यह Xpath बदलना पड़ सकता है
        rows = driver.find_elements(
            By.XPATH, "//div[contains(@class, 'Game history')]//table//tr"
        )

        game_records = []

        for row in rows:
            try:
                # प्रत्येक रो के अंदर मौजूद सभी कॉलम्स (td) को ढूंढें
                cols = row.find_elements(By.TAG_NAME, "td")

                # सुनिश्चित करें कि रो में डेटा मौजूद है (हेडर छोड़कर)
                if len(cols) >= 4:
                    period = cols[0].text  # पीरियड नंबर (जैसे: 20260829100052662)
                    number = cols[1].text  # नंबर (जैसे: 8)
                    big_small = cols[2].text  # बिग या स्मॉल (जैसे: Big)
                    color = cols[3].text  # कलर का नाम

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
                # यदि किसी रो को पार्स करने में समस्या हो तो उसे स्किप करें
                continue

        print(
            f"\nसफलतापूर्वक {len(game_records)} रिकॉर्ड्स इतिहास से निकाले गए।"
        )

    except Exception as global_error:
        print(f"ऑटोमेशन के दौरान त्रुटि आई: {global_error}")

    finally:
        # 5. काम पूरा होने के बाद ब्राउज़र बंद करें
        print("ब्राउज़र बंद किया जा रहा है...")
        driver.quit()


if __name__ == "__main__":
    run_full_automation()
    

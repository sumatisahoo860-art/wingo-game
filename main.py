import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def run_on_mobile_chrome():
    # मोबाइल के अंदर क्रोम ब्राउज़र चलाने की ज़रूरी सेटिंग्स
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # बैकग्राउंड में क्रोम चलाने के लिए
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    print("🚀 मोबाइल क्रोम ब्राउज़र शुरू हो रहा है...")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)

    try:
        # --- चरण 1: लॉगिन प्रक्रिया ---
        print("🔗 क्रोम में लॉगिन पेज खोला जा रहा है...")
        driver.get("https://51gameq.com")
        time.sleep(5)

        phone_input = wait.until(
            EC.presence_of_element_located((By.NAME, "phone"))
        )
        password_input = driver.find_element(By.NAME, "password")

        # ⚠️ यहाँ अपना असली नंबर और पासवर्ड डालें
        phone_input.send_keys("YOUR_PHONE_NUMBER")
        password_input.send_keys("YOUR_PASSWORD")

        login_button = driver.find_element(
            By.XPATH, "//button[contains(text(), 'Login')]"
        )
        login_button.click()
        print("✅ लॉगिन बटन पर क्लिक किया गया।")
        time.sleep(6)

        # --- चरण 2: गेम पेज पर जाना ---
        print("🎮 WinGo गेम पेज पर जा रहे हैं...")
        driver.get("https://51gameq.com...")  # ⚠️ यहाँ गेम का सही लिंक डालें
        time.sleep(5)

        # --- चरण 3: लगातार पीरियड नंबर और हिस्ट्री देखना ---
        print("📊 गेम हिस्ट्री और पीरियड नंबर मॉनिटरिंग शुरू...")
        while True:
            try:
                # स्क्रीन से गेम इतिहास की टेबल ढूंढें
                rows = driver.find_elements(
                    By.XPATH,
                    "//div[contains(@class, 'Game history')]//table//tr",
                )

                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) >= 4:
                        period = cols[0].text  # पीरियड नंबर
                        number = cols[1].text  # नंबर
                        size = cols[2].text  # बिग/स्मॉल

                        print(
                            f"🔹 Period: {period} | Number: {number} | Size: {size}"
                        )

                print("--- 10 सेकंड में नया डेटा आएगा ---")
                time.sleep(10)  # हर 10 सेकंड में नया पीरियड नंबर चेक करेगा

            except Exception as loop_err:
                time.sleep(2)

    except Exception as global_error:
        print(f"❌ एरर आया: {global_error}")
    finally:
        print("🛑 ब्राउज़र बंद हो रहा है...")
        driver.quit()


if __name__ == "__main__":
    run_on_mobile_chrome()
    

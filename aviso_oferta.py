import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

print('Starting...')
# CONFIG
URL = "{URL}"  # URL del producto a monitorear
PRICE_THRESHOLD_ARS = 81000
TELEGRAM_BOT_TOKEN = "{TU_TOKEN}"
TELEGRAM_CHAT_ID = "{TU_CHAT_ID}"
CHECK_INTERVAL = 900  # Chequear cada 900 segundos (15 minutos)

# Configurar el navegador en modo headless
options = Options()
options.headless = True
service = Service()
driver = webdriver.Chrome(service=service, options=options)

def parse_price(text):
    clean = text.replace("$", "").replace(" ", "").strip()
    clean = clean.replace(".", "").replace(",", ".")
    try:
        return float(clean)
    except ValueError:
        return None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Error sending message: {e}")

def check_products():
    driver.get(URL)
    time.sleep(5)  # esperar a que cargue JS
    soup = BeautifulSoup(driver.page_source, "html.parser")

    products = soup.find_all("div", class_="js-product-item-private product-item js-product-container js-item-product mb-3")
    
    for product in products:
        title_tag = product.find("div", class_="js-item-name")
        price_tag = product.find("span", class_="js-price-display")

        if title_tag and price_tag:
            title = title_tag.get_text(strip=True)
            price = parse_price(price_tag.get_text())

            if price and price < PRICE_THRESHOLD_ARS:
                message = f"🟢 {title} está por debajo del umbral: ${price:,}"
                print(message)
                send_telegram_message(message)

if __name__ == '__main__':
    print("Starting price checker...")
    try:
        while True:
            check_products()
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("Finalizando...")
    finally:
        driver.quit()
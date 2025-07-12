import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ----- SETUP -----
options = Options()
options.add_argument("--headless=new")  # Headless = silent mode
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

# ----- CONFIG -----
base_url = "https://sourcing.alibaba.com/rfq/rfq_search_list.htm?spm=a2700.8073608.1998677541.1.82be65aaoUUItC&country=AE&recently=Y&page={}"

all_data = []
max_pages = 2  # ⬅️ You can increase this

# ----- SCRAPER LOOP -----
for page in range(1, max_pages + 1):
    print(f"\n📄 Scraping Page {page}...")
    url = base_url.format(page)
    driver.get(url)
    time.sleep(4)

    try:
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.brh-rfq-item__subject-link")))
        cards = driver.find_elements(By.CSS_SELECTOR, "div.brh-rfq-item")
        print(f"📦 Found {len(cards)} RFQ cards")

        for card in cards:
            def safe(selector, attr='text', default=''):
                try:
                    el = card.find_element(By.CSS_SELECTOR, selector)
                    if attr == 'text':
                        return el.text.strip()
                    elif attr == 'src':
                        return "https:" + el.get_attribute("src")
                    elif attr == 'href':
                        return "https:" + el.get_attribute("href")
                    else:
                        return el.get_attribute(attr)
                except:
                    return default

            title = safe("a.brh-rfq-item__subject-link")
            rfq_link = safe("a.brh-rfq-item__subject-link", attr="href")
            quantity_num = safe(".brh-rfq-item__quantity-num")
            quantity_unit = safe(".brh-rfq-item__quantity > span:nth-child(3)")
            quantity = f"{quantity_num} {quantity_unit}".strip()
            country = safe(".brh-rfq-item__country")
            posted_on = safe(".brh-rfq-item__publishtime").replace("Date Posted:", "").strip()
            quotes_left = safe(".brh-rfq-item__quote-left span")
            buyer_name = safe(".brh-rfq-item__other-info .text")
            buyer_image = safe(".img-con img", attr="src", default="N/A")

            try:
                tag_div = card.find_element(By.CSS_SELECTOR, ".brh-rfq-item__buyer-tag")
                tags = [tag.text.strip() for tag in tag_div.find_elements(By.CSS_SELECTOR, ".next-tag-body")]
            except:
                tags = []

            email_confirmed = "Yes" if "Email Confirmed" in tags else "No"
            experienced_buyer = "Yes" if "Experienced buyer" in tags else "No"
            complete_order = "Yes" if "Complete order via RFQ" in tags else "No"
            typical_replies = "Yes" if "Typically replies" in tags else "No"
            interactive_user = "Yes" if "Interactive user" in tags else "No"
            scraping_date = datetime.today().strftime("%Y-%m-%d")

            all_data.append({
                "Buyer Name": buyer_name,
                "Buyer Image": buyer_image,
                "Inquiry Title": title,
                "Inquiry URL": rfq_link,
                "Inquiry Time": posted_on,
                "Quotes Left": quotes_left,
                "Country": country,
                "Quantity Required": quantity,
                "Email Confirmed": email_confirmed,
                "Experienced Buyer": experienced_buyer,
                "Complete Order via RFQ": complete_order,
                "Typical Replies": typical_replies,
                "Interactive User": interactive_user,
                "Inquiry Date": posted_on,
                "Scraping Date": scraping_date
            })

    except Exception as e:
        print(f"❌ Error on page {page}: {e}")
        continue

driver.quit()

# ----- SAVE OUTPUT -----
if all_data:
    df = pd.DataFrame(all_data)
    df.to_csv("alibaba_rfq_output.csv", index=False, encoding="utf-8-sig")
    print("\n✅ Done! Data saved to alibaba_rfq_output.csv")
else:
    print("⚠️ No data found.")

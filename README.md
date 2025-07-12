# 📦 Alibaba RFQ Web Scraper

This project is a **Python-based web scraper** that extracts buyer inquiry data from the Alibaba RFQ (Request for Quotation) listings. It uses **Selenium** to navigate pages and collect detailed information from each RFQ post, and saves the results in a clean **CSV file**.

---

## 🚀 Features

- Scrapes **multiple pages** of RFQs
- Runs in **headless mode** (silent background scraping)
- Extracts the following fields:

| Field | Description |
|-------|-------------|
| Buyer Name | Name of the buyer |
| Buyer Image | URL of buyer profile picture |
| Inquiry Title | Title of the buyer's inquiry |
| Inquiry URL | Direct link to the RFQ post |
| Inquiry Time | How recently it was posted |
| Quotes Left | Remaining quote slots |
| Country | Buyer's country |
| Quantity Required | Quantity and unit |
| Email Confirmed | Whether buyer has verified email |
| Experienced Buyer | Label if buyer is experienced |
| Complete Order via RFQ | Whether buyer has completed orders through RFQs |
| Typical Replies | Indicates if buyer usually replies |
| Interactive User | Indicates active buyer |
| Inquiry Date | Date/time shown on site |
| Scraping Date | Current scraping timestamp |

---

## 🛠️ Requirements

- Python 3.8+
- Google Chrome
- ChromeDriver (matching your browser version)

### Install dependencies:

bash
pip install selenium pandas
🧠 How It Works
Constructs the URL with &page=1, &page=2, etc.

Loads each RFQ listing page.

Extracts key information from each inquiry card.

Repeats for all pages (you can configure how many).

Saves data to alibaba_rfq_output.csv.

▶️ How to Run
bash
Copy
Edit
python alibaba_rfq_scraper.py
Output CSV will be saved in the same directory.

Headless Chrome runs in the background.

📂 Example Output
Buyer Name	Inquiry Title	Quotes Left	Email Confirmed
Infinity Trading	display racks	8	Yes
Vimal ATE	LED Lighting and Electrical Items	10	Yes

🔄 Customization
To increase pages scraped:
Change max_pages = 20 to any number in the script.

To run with GUI:
Comment out:

python
Copy
Edit
options.add_argument("--headless=new")
📌 Notes
Designed specifically for this RFQ listing:

arduino
Copy
Edit
https://sourcing.alibaba.com/rfq/rfq_search_list.htm?country=AE&recently=Y
Only public data is scraped for personal/research/educational purposes.

Respect Alibaba’s terms of service when using this script.

📅 Future Enhancements
Auto-upload CSV to Google Drive

Daily scheduler with email reports

Scraping additional filters (industry, keywords, etc.)

👤 Author
Swagatam
📧 swagatam2222@gmail.com
💼 GitHub: Swagatam-lab

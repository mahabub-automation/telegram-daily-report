# 📊 Telegram Daily Sales Report Bot

Automated daily sales summary delivered to Telegram — reads sales data from Google Sheets, builds a formatted report, and sends it every night. Runs **serverless on GitHub Actions**: no server, no PC left on, zero hosting cost.

Built for small businesses (restaurants, shops, online sellers) whose owners want to see the day's numbers on their phone without opening a spreadsheet.

---

## ✨ What the report includes

- Total orders, total sales and average order value
- Number of unique customers
- Comparison with yesterday (percentage up / down)
- Top-selling products of the day
- A clear message when no sales were recorded

## 📱 Sample output

```
Rahim Restaurant
Daily Sales Report
20 September 2026, 10:00 PM

-------------------------------
Total Orders   : 4
Total Sales    : 1,650 BDT
Average Order  : 412 BDT
Customers      : 3
-------------------------------

Compared to yesterday
Yesterday : 1,250 BDT
Change    : UP 32.0%

Top 3 Products
1. Pizza - 800 BDT
2. Burger - 700 BDT
3. Coffee - 150 BDT
```

---

## 🏗️ How it works

```
Google Sheet  →  data_reader.py  →  report_builder.py  →  notifier.py  →  Telegram
                                                                           ↑
                          GitHub Actions cron (daily, 22:00 Asia/Dhaka) ───┘
```

| File | Responsibility |
|---|---|
| `config.py` | All client-specific settings — business name, column mapping, report options |
| `data_reader.py` | Loads data from a shared Google Sheet (CSV export) or a local Excel file |
| `report_builder.py` | Filters today/yesterday with timezone handling, computes metrics, formats HTML message |
| `notifier.py` | Reusable Telegram client — messages, documents, connection test |
| `main.py` | Orchestrates the steps; sends a failure alert to Telegram if any step breaks |
| `.github/workflows/daily-report.yml` | Scheduled run + manual trigger |

## 🔁 Reusable template

Onboarding a new business only needs **one config file and three secrets** — no code changes:

```python
BUSINESS_NAME = "Rahim Restaurant"
COLUMN_DATE = "Date"
COLUMN_AMOUNT = "Amount"
COLUMN_PRODUCT = "Product"
SHOW_COMPARISON = True
```

---

## 🚀 Setup

### 1. Prepare the sheet
Create a Google Sheet with these headers and share it as *Anyone with the link → Viewer*:

| Date | Product | Customer | Amount | Status |
|---|---|---|---|---|
| 2026-09-20 | Burger | Rahim | 350 | Delivered |

### 2. Create a Telegram bot
Talk to [@BotFather](https://t.me/BotFather) → `/newbot` → copy the token. Send the bot a message, then read your chat ID from `https://api.telegram.org/bot<TOKEN>/getUpdates`.

### 3. Run locally
```bash
pip install -r requirements.txt
```
Create a `.env` file:
```
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
GOOGLE_SHEET_URL=your_sheet_link
```
```bash
python main.py
```

### 4. Deploy on GitHub Actions
Add the same three values under **Settings → Secrets and variables → Actions**, then trigger **Actions → Daily Sales Report → Run workflow** to test. After that it runs every day on its own.

---

## 🛠️ Tech stack

Python · pandas · Google Sheets (CSV export) · Telegram Bot API · GitHub Actions · python-dotenv

## 🔒 Security

Credentials are never committed — they live in a local `.env` file (git-ignored) and in GitHub Actions encrypted secrets.

---

## 👤 Author

**Md. Mahabubul Hasan** — [@mahabub-automation](https://github.com/mahabub-automation) · [LinkedIn](https://linkedin.com/in/mahabubulhasan)

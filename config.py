"""
Configuration file.
The client only needs to edit values in this file.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ===================================================
# TELEGRAM SETTINGS
# ===================================================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# ===================================================
# DATA SOURCE
# Choose one: "google_sheet" or "excel"
# ===================================================
DATA_SOURCE = "google_sheet"

GOOGLE_SHEET_URL = os.getenv("GOOGLE_SHEET_URL", "")

EXCEL_FILE_PATH = "data/sales.xlsx"
EXCEL_SHEET_NAME = "Sheet1"

# ===================================================
# COLUMN MAPPING
# Change these to match the client's sheet headers
# ===================================================
COLUMN_DATE = "Date"
COLUMN_AMOUNT = "Amount"
COLUMN_PRODUCT = "Product"
COLUMN_CUSTOMER = "Customer"
COLUMN_STATUS = "Status"

# ===================================================
# BUSINESS SETTINGS
# ===================================================
BUSINESS_NAME = "My Restaurant"
CURRENCY = "BDT"
TIMEZONE_OFFSET = 6
TOP_PRODUCTS_COUNT = 5

# ===================================================
# REPORT OPTIONS
# ===================================================
SHOW_TOP_PRODUCTS = True
SHOW_COMPARISON = True
SHOW_CUSTOMER_COUNT = True
"""
Data reading module.
Supports Google Sheets and local Excel files.
Reusable across all automation tools.
"""

import pandas as pd
import logging
import re

logger = logging.getLogger(__name__)


def convert_sheet_url_to_csv(sheet_url):
    """Convert a normal Google Sheets URL into a CSV export URL."""
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", sheet_url)
    if not match:
        raise ValueError("Invalid Google Sheets URL.")
    sheet_id = match.group(1)

    gid_match = re.search(r"[#&]gid=(\d+)", sheet_url)
    gid = gid_match.group(1) if gid_match else "0"

    return (
        f"https://docs.google.com/spreadsheets/d/{sheet_id}"
        f"/export?format=csv&gid={gid}"
    )


def read_google_sheet(sheet_url):
    """Read data from a publicly shared Google Sheet."""
    csv_url = convert_sheet_url_to_csv(sheet_url)
    logger.info("Reading data from Google Sheets...")
    dataframe = pd.read_csv(csv_url)
    logger.info(f"Loaded {len(dataframe)} rows.")
    return dataframe


def read_excel_file(file_path, sheet_name="Sheet1"):
    """Read data from a local Excel file."""
    logger.info(f"Reading Excel file: {file_path}")
    dataframe = pd.read_excel(file_path, sheet_name=sheet_name)
    logger.info(f"Loaded {len(dataframe)} rows.")
    return dataframe


def load_data(source_type, google_sheet_url=None,
              excel_path=None, excel_sheet="Sheet1"):
    """Load data based on the configured source type."""
    if source_type == "google_sheet":
        return read_google_sheet(google_sheet_url)
    elif source_type == "excel":
        return read_excel_file(excel_path, excel_sheet)
    else:
        raise ValueError(f"Unknown data source: {source_type}")
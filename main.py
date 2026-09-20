"""
Telegram Daily Report Bot
Entry point.
"""

import sys
import logging

import config
from notifier import TelegramNotifier
from data_reader import load_data
from report_builder import build_report

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    logger.info("=" * 50)
    logger.info("Starting Daily Report Bot")
    logger.info("=" * 50)

    # Step 1: Connect to Telegram
    try:
        notifier = TelegramNotifier(
            config.TELEGRAM_TOKEN,
            config.TELEGRAM_CHAT_ID
        )
    except ValueError as error:
        logger.error(f"Configuration error: {error}")
        return 1

    if not notifier.test_connection():
        logger.error("Could not connect to Telegram. Check your token.")
        return 1

    # Step 2: Load the data
    try:
        dataframe = load_data(
            source_type=config.DATA_SOURCE,
            google_sheet_url=config.GOOGLE_SHEET_URL,
            excel_path=config.EXCEL_FILE_PATH,
            excel_sheet=config.EXCEL_SHEET_NAME,
        )
    except Exception as error:
        logger.error(f"Failed to load data: {error}")
        notifier.send_message(
            f"Report failed.\nCould not read the data source.\n\nError: {error}"
        )
        return 1

    # Step 3: Build the report
    try:
        report_text = build_report(dataframe)
        logger.info("Report built successfully.")
    except Exception as error:
        logger.error(f"Failed to build report: {error}")
        notifier.send_message(
            f"Report failed while processing data.\n\nError: {error}"
        )
        return 1

    # Step 4: Send the report
    if notifier.send_message(report_text):
        logger.info("Daily report delivered.")
        return 0

    logger.error("Failed to deliver the report.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
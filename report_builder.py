"""
Builds the daily sales report message.
"""

import pandas as pd
from datetime import datetime, timedelta, timezone
import logging

import config

logger = logging.getLogger(__name__)


def get_local_now():
    """Return the current time in the configured timezone."""
    return datetime.now(timezone.utc) + timedelta(hours=config.TIMEZONE_OFFSET)


def format_money(amount):
    """Format a number as currency."""
    return f"{amount:,.0f} {config.CURRENCY}"


def filter_by_date(dataframe, target_date):
    """Return only the rows matching a specific date."""
    dataframe[config.COLUMN_DATE] = pd.to_datetime(
        dataframe[config.COLUMN_DATE], errors="coerce"
    )
    mask = dataframe[config.COLUMN_DATE].dt.date == target_date
    return dataframe[mask]


def build_report(dataframe):
    """Create the full report message."""
    now = get_local_now()
    today = now.date()
    yesterday = today - timedelta(days=1)

    today_data = filter_by_date(dataframe.copy(), today)
    yesterday_data = filter_by_date(dataframe.copy(), yesterday)

    total_sales = today_data[config.COLUMN_AMOUNT].sum()
    total_orders = len(today_data)
    average_order = total_sales / total_orders if total_orders else 0

    lines = []
    lines.append(f"<b>{config.BUSINESS_NAME}</b>")
    lines.append("<b>Daily Sales Report</b>")
    lines.append(now.strftime("%d %B %Y, %I:%M %p"))
    lines.append("")
    lines.append("-------------------------------")
    lines.append(f"Total Orders   : <b>{total_orders}</b>")
    lines.append(f"Total Sales    : <b>{format_money(total_sales)}</b>")
    lines.append(f"Average Order  : {format_money(average_order)}")

    if config.SHOW_CUSTOMER_COUNT and config.COLUMN_CUSTOMER in today_data.columns:
        unique_customers = today_data[config.COLUMN_CUSTOMER].nunique()
        lines.append(f"Customers      : {unique_customers}")

    lines.append("-------------------------------")

    if config.SHOW_COMPARISON and len(yesterday_data) > 0 and total_orders > 0:
        yesterday_sales = yesterday_data[config.COLUMN_AMOUNT].sum()
        difference = total_sales - yesterday_sales
        percent = (difference / yesterday_sales * 100) if yesterday_sales else 0
        direction = "UP" if difference >= 0 else "DOWN"

        lines.append("")
        lines.append("<b>Compared to yesterday</b>")
        lines.append(f"Yesterday : {format_money(yesterday_sales)}")
        lines.append(f"Change    : {direction} {abs(percent):.1f}%")

    if config.SHOW_TOP_PRODUCTS and config.COLUMN_PRODUCT in today_data.columns:
        if total_orders > 0:
            top_products = (
                today_data.groupby(config.COLUMN_PRODUCT)[config.COLUMN_AMOUNT]
                .sum()
                .sort_values(ascending=False)
                .head(config.TOP_PRODUCTS_COUNT)
            )
            lines.append("")
            lines.append(f"<b>Top {len(top_products)} Products</b>")
            for rank, (product, amount) in enumerate(top_products.items(), start=1):
                lines.append(f"{rank}. {product} - {format_money(amount)}")

    if total_orders == 0:
        lines.append("")
        lines.append("<i>No sales recorded for today.</i>")

    lines.append("")
    lines.append("-------------------------------")
    lines.append("<i>Automated report</i>")

    return "\n".join(lines)

import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
LOCATION = os.getenv("LOCATION")
BQ_LOCATION = os.getenv("BQ_LOCATION", "US")

# Define your datasets
DATASETS = {
    "sticker_sales": {
        "dataset_id": "sticker",
        "table_id": "sales",
        "description": "Contains sticker sales data with columns like num_sold, country, date, etc."
    },
    "sticker_inventory": {
        "dataset_id": "sticker",
        "table_id": "inventory",
        "description": "Sticker inventory levels. key column: 'product' (joins with sales table)."
    }
}
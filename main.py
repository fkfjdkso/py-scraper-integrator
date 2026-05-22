import os
import asyncio
from dotenv import load_dotenv
from scraper import Scraper
from sheets import GoogleSheetIntegrator

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
ENDPOINT = os.getenv("ENDPOINT")


async def main():
    json_key = os.getenv("CREDENTIALS_FILE")
    sheet_name = os.getenv("SHEET_NAME")
    if not json_key or not sheet_name:
        return

    base_url = BASE_URL
    scraper = Scraper(base_url)
    endpoint = ENDPOINT
    df = await scraper.run(endpoint, batch_size=5, max_pages=200)
    integrator = GoogleSheetIntegrator(json_key, sheet_name)
    integrator.send_data(df)


if __name__ == "__main__":
    asyncio.run(main())

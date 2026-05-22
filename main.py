import os
import asyncio
from dotenv import load_dotenv
from scraper import Scraper
from sheets import GoogleSheetIntegrator

load_dotenv()


async def main():
    json_key = os.getenv("CREDENTIALS_FILE")
    sheet_name = os.getenv("SHEET_NAME")
    if not json_key or not sheet_name:
        return

    base_url = "https://www.chitai-gorod.ru"
    scraper = Scraper(base_url)
    endpoint = "/catalog/books/rossijskaya-literatura-110050"
    df = await scraper.run(endpoint, batch_size=5, max_pages=200)
    integrator = GoogleSheetIntegrator(json_key, sheet_name)
    integrator.send_data(df)


if __name__ == "__main__":
    asyncio.run(main())

import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup


class Scraper:

    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        }

    async def fetch_page(self, session, endpoint):
        url = f"{self.base_url}{endpoint}"
        async with session.get(url, headers=self.headers) as response:
            return await response.text()

    def parse(self, html):
        soup = BeautifulSoup(html, "html.parser")
        products = soup.select("article[data-testid-product-item]")
        items = []

        for product in products:
            title_el = product.select_one(".product-card__title")
            title = title_el.text.strip() if title_el else "Без названия"

            author_el = product.select_one(".product-card__subtitle")
            author = author_el.text.strip() if author_el else "Без автора"

            price = product.select_one(".product-mini-card-price__price")
            price_value = 0
            if price:
                raw_price = price.text.strip()
                clean_price = "".join(c for c in raw_price if c.isdigit())
                price_value = int(clean_price) if clean_price else 0

            items.append({"title": title, "author": author, "price": price_value})
        return items

    # async def run(self, endpoint, total_pages=1):
    #     all_data = []
    #     async with aiohttp.ClientSession() as session:
    #         for page in range(1, total_pages + 1):
    #             page_url = f"{endpoint}?page={page}"
    #             print(f"page: {page}/{total_pages}")
    #             try:
    #                 html = await self.fetch_page(session, page_url)
    #                 page_data = self.parse(html)
    #                 all_data.extend(page_data)
    #             except Exception as e:
    #                 print(f"error on page {page}: {e}")
    #             if page < total_pages:
    #                 await asyncio.sleep(1)
    #     return all_data

    async def run(self, endpoint, batch_size=5, max_pages=None):
        conn = aiohttp.TCPConnector(limit=batch_size)
        async with aiohttp.ClientSession(
            connector=conn, headers=self.headers
        ) as session:

            all_data = []
            start_page = 1
            while True:
                curr_batch = batch_size
                if max_pages is not None:
                    if start_page > max_pages:
                        break
                    if start_page + batch_size - 1 > max_pages:
                        curr_batch = max_pages - start_page + 1

                end_page = start_page + curr_batch
                tasks = [
                    self.fetch_page(session, f"{endpoint}?page={p}")
                    for p in range(start_page, end_page)
                ]

                pages_html = await asyncio.gather(*tasks, return_exceptions=True)

                batch_has_data = False
                for html in pages_html:
                    if html and isinstance(html, str):
                        parsed_items = self.parse(html)
                        if parsed_items:
                            all_data.extend(parsed_items)
                            batch_has_data = True

                if not batch_has_data:
                    break

                if max_pages is not None and (end_page - 1) >= max_pages:
                    break

                await asyncio.sleep(2)
                start_page += curr_batch

            if not all_data:
                return pd.DataFrame(columns=["title", "author", "price"])
            df = pd.DataFrame(all_data)
            if "title" in df.columns:
                df = df.drop_duplicates(subset=["title"])

            return df

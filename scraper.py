# scraper_project/scraper.py
from loguru import logger
from scraping_tasks.scraping_tasks import scrape_table_data, scrape_quotes

# Configure Loguru
logger.add(
    "scraper.log", rotation="500 MB", retention="7 days", enqueue=True, level="INFO"
)

if __name__ == "__main__":
    # URLs to scrape
    chemicalbook_url = (
        "https://www.chemicalbook.com/ChemicalProductProperty_DE_CB4116411.htm"
    )
    quotes_url = "http://quotes.toscrape.com/"

    # Call both scraping functions with URLs as parameters
    scrape_table_data(chemicalbook_url)
    scrape_quotes(quotes_url)

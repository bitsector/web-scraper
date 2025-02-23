# scraper_project/scraping_tasks/scraping_tasks.py
import requests
from bs4 import BeautifulSoup
from loguru import logger
from utils.util import get_header

def scrape_table_data(url):
    """Scrape chemical product data from ChemicalBook"""
    headers = get_header()
    
    logger.info(f"Starting scrape for ChemicalBook at URL: {url} with headers: {headers['User-Agent']}")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        if (th_element := soup.find("th", string="Firmenname")):
            logger.success("Found 'Firmenname' header element")
            
            if (table := th_element.find_parent("table")):
                logger.info("Extracting table rows")
                rows = table.find_all("tr")
                
                for row in rows:
                    cells = [cell.get_text(strip=True) for cell in row.find_all(["td", "th"])]
                    logger.debug(f"Row data: {cells}")
                
                logger.info(f"Extracted {len(rows)} rows")
            else:
                logger.warning("No parent table found")
        else:
            logger.error("Target element not found")
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")

def scrape_quotes(url):
    """Scrape quotes and authors from Quotes to Scrape"""
    logger.info(f"Starting scrape for Quotes to Scrape at URL: {url} without headers")
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        quotes = soup.find_all("div", class_="quote")

        if quotes:
            logger.success(f"Found {len(quotes)} quotes on the page")
            
            for quote in quotes:
                text = quote.find("span", class_="text").get_text(strip=True)
                author = quote.find("small", class_="author").get_text(strip=True)
                logger.info(f"Quote: {text} - Author: {author}")
        else:
            logger.warning("No quotes found on the page")
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")

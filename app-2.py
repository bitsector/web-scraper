# scraper_project/app-2.py
import requests
from bs4 import BeautifulSoup
from loguru import logger
from utils.util import get_header

# Configure Loguru
logger.add("scraper.log", 
          rotation="500 MB",
          retention="7 days",
          enqueue=True,
          level="INFO")

def scrape_table_data():
    '''Scrape chemical product data from ChemicalBook'''
    url = "https://www.chemicalbook.com/ChemicalProductProperty_DE_CB4116411.htm"
    headers = get_header()
    
    logger.info(f"Starting scrape with headers: {headers['User-Agent']}")
    
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

if __name__ == "__main__":
    scrape_table_data()

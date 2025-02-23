import requests
from bs4 import BeautifulSoup
import random
from loguru import logger

# Configure Loguru (rotating logs with retention)
logger.add("scraper.log", 
          rotation="500 MB",  # Rotate when log reaches 500MB
          retention="7 days",  # Keep logs for 1 week
          enqueue=True,  # Thread-safe logging
          level="INFO")

def get_header(index=None):
    """Return browser headers with optional specific User-Agent"""
    user_agents = [
        # Windows (0-1)
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36 Edg/117.0",
        # macOS (2-3)
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Safari/537.36",
        # Linux (4-5)
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:117.0) Gecko/20100101 Firefox/117.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Safari/537.36",
        # Android (6-7)
        "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/20 Mobile Safari/537.36",
        # iOS (8-9)
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16 Mobile Safari/605.1",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) CriOS/117 Mobile Safari/537.36",
        # Other browsers (10-11)
        "Mozilla/5.0 (Windows NT 10; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117 OPR/102 Safari/537",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3_1) AppleWebKit/537 (KHTML, like Gecko) Chrome Brave Safari"
    ]

    base_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/",
    }

    # Select User-Agent
    user_agent = user_agents[index] if isinstance(index, int) else random.choice(user_agents)
    logger.debug(f"Generated headers with User-Agent: {user_agent}")
    
    return {**base_headers, "User-Agent": user_agent}

def scrape_table_data():
    """Scrape chemical product data from ChemicalBook"""
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

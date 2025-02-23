import requests
from bs4 import BeautifulSoup

import random

def get_header(index=None):
    """
    Returns browser headers with either:
    - A specific User-Agent (if index is provided)
    - Random User-Agent (if index is None)
    
    Parameters:
    index (int, optional): Index from 0-11 to select specific header. Defaults to random.
    """
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
    if isinstance(index, int):
        user_agent = user_agents[index]
    else:
        user_agent = random.choice(user_agents)

    return {
        **base_headers,
        "User-Agent": user_agent
    }

def scrape_table_data():
    # ChemicalBook URL
    url = "https://www.chemicalbook.com/ChemicalProductProperty_DE_CB4116411.htm"

    # Provide a common User-Agent header to simulate a real browser
    headers = get_header()

    print(f"using header: {headers}")

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Locate the <th> element containing the text "Firmenname"
        th_element = soup.find("th", string="Firmenname")
        if th_element:
            print(f"Found the element with text 'Firmenname': {th_element}")

            # Find the parent table of the <th> element
            table = th_element.find_parent("table")
            if table:
                print("\nTable found. Extracting rows...")

                # Extract all rows (<tr>) from the table
                rows = table.find_all("tr")
                for row in rows:
                    # Extract all cells (<td> or <th>) in each row
                    cells = row.find_all(["td", "th"])
                    cell_texts = [cell.get_text(strip=True) for cell in cells]
                    print(cell_texts)
            else:
                print("No parent table found for the 'Firmenname' header.")
        else:
            print("Could not find the element with text 'Firmenname'.")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

if __name__ == "__main__":
    scrape_table_data()

import requests
from bs4 import BeautifulSoup

def scrape_table_data():
    # ChemicalBook URL
    url = "https://www.chemicalbook.com/ChemicalProductProperty_DE_CB4116411.htm"

    # Provide a common User-Agent header to simulate a real browser
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        )
    }

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

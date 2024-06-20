import requests
from bs4 import BeautifulSoup
import csv
import re  # Import regex module
from datetime import datetime  # Import datetime module to handle dates

def scrape_and_export_to_csv(url, output_filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    data_to_export = []  # List to hold dictionaries of scraped data

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div', class_='slidelink')  # Adjust class as needed

        for card in cards:
            name_tag = card.find('h3', class_='line-top')
            if name_tag:
                # Using regex to separate name and content in parentheses
                match = re.match(r"^(.*?)\s*\((.*?)\)$", name_tag.text.strip())
                if match:
                    name = match.group(1).strip()
                    ticker = match.group(2).strip()
                else:
                    name = name_tag.text.strip()
                    ticker = 'N/A'  # Default value if no parentheses content
            else:
                name, ticker = 'N/A', 'N/A'

            min_investment_header = card.find('h4', string="Min Investment")
            min_investment = min_investment_header.find_next('span').text.strip() if min_investment_header else 'N/A'

            price_per_token_header = card.find('h4', string="Price Per Token")
            price_per_token = price_per_token_header.find_next('span').text.strip() if price_per_token_header else 'N/A'

            description = card.find('p')
            description_text = description.text.strip() if description else 'N/A'

            # Extracting tags
            tags = card.find_all('a', class_='transparent-tag mt-2')
            stages = [tag.text.strip() for tag in tags if 'stage=' in tag['href']]
            token_types = [tag.text.strip() for tag in tags if 'token_type=' in tag['href']]
            investor_types = [tag.text.strip() for tag in tags if 'investor_type=' in tag['href']]

            # Add the scraped data to the list as a dictionary
            data_to_export.append({
                "Name": name,
                "Ticker": ticker,
                "Min Investment": min_investment,
                "Price Per Token": price_per_token,
                "Stage": ', '.join(stages),
                "Token Type": ', '.join(token_types),
                "Investor Type": ', '.join(investor_types),
                "Description": description_text
            })

        # Export to CSV
        with open(output_filename, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ["Name", "Ticker", "Min Investment", "Price Per Token", "Stage", "Token Type", "Investor Type", "Description"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data_to_export)
        print(f"Data has been written to {output_filename}")
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)

# Current date in YYYYMMDD format
current_date = datetime.now().strftime('%Y%m%d')

# Current time in HHMMSS format
current_time = datetime.now().strftime('%H%M%S')

# URL of the website to scrape and dynamic output filename
url = "https://stomarket.com/explore"
output_filename = f"sto_{current_date}.csv"
scrape_and_export_to_csv(url, output_filename)
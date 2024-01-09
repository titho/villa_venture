import csv
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

def fetch_villa_links(base_url, min_places, max_places):
    links = []
    page = 1
    while True:
        url = f"{base_url}{page}/"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch {url}")
            page += 1
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        if 'Няма намерени обяви' in soup.text:
            break
        
        offers = soup.find_all('div', class_='offersListingInfoBox')
        for offer in offers:
            places_info = offer.find(string=lambda text: 'места' in text)
            if places_info:
                places = int(places_info.split()[2])
                if min_places <= places <= max_places:
                    link = offer.find('a', href=True)['href']
                    full_link = urljoin(response.url, link)
                    links.append(full_link)
        page += 1
    return links

def extract_info(url, date):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        title_tag = soup.find("meta", property="og:title")
        title = title_tag["content"] if title_tag else ''

        capacity_tag = soup.find('h5', string=lambda text: text and 'наематели' in text)
        capacity = capacity_tag.next_sibling.strip() if capacity_tag else ''

        description_tag = soup.find('div', style=lambda value: value and "padding: 0 0 1px 0" in value)
        description = description_tag.get_text(strip=True).replace('Описание на', '').strip() if description_tag else ''

        accommodation_types = soup.select('#pricesAccommodationTypes > div')
        prices_rows = soup.select('#pricesCalendarSlider > div[id="pricesRow"]')
        price_details = []

        for acc_type, price_row in zip(accommodation_types, prices_rows):
            acc_name = acc_type.get('title', '').strip()
            date_price_tag = price_row.find('div', class_='day', title=date)
            if date_price_tag:
                price = date_price_tag.get_text(strip=True)
                if price.isdigit():
                    price_details.append(f"{acc_name}: {price} лв.")

        price = ' | '.join(price_details) if price_details else 'Not Found'

        address_tag = soup.find('li', class_='caption', string='Адрес:')
        location = address_tag.find_next_sibling('li', class_='element').get_text(strip=True) if address_tag else ''

    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")
        return '', '', '', '', '', url

    return title, capacity, description, price, location, url

def create_csv(links, date, csv_filename):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Title', 'Capacity', 'Description', 'Price', 'Location', 'URL'])

        for url in links:
            info = extract_info(url, date)
            csv_writer.writerow(info)

def scrape_villas(min_capacity, max_capacity, date):
    base_url = "https://www.bgvakancia.com/bulgaria/holidays/all-destinations/villas/"
    links = fetch_villa_links(base_url, min_capacity, max_capacity)
    datetime_str = datetime.now().strftime("%d-%m_%H-%M")  # Current date and time
    csv_filename = f"villas_info_{datetime_str}.csv"
    create_csv(links, date, csv_filename)

# Example usage
scrape_villas(min_capacity=20, max_capacity=40, date="09.02.2024")

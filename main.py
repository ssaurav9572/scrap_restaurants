import requests
from bs4 import BeautifulSoup
import json
import gzip

url = "https://food.grab.com/sg/en/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    restaurants = []

    for restaurant in soup.find_all('div', class_='ant-col-24 colInfo___3iLqj ant-col-md-24 ant-col-lg-24'):
        try:
            name = restaurant.find('p', class_='name___2epcT').text
        except AttributeError:
            name = None

        try:
            cuisine = restaurant.find('div', class_='basicInfoRow___UZM8d cuisine___T2tCh').text
        except AttributeError:
            cuisine = None

        try:
            rating = restaurant.find('div', class_='numbersChild___2qKMV').find('div', class_='ratingStar infoItemIcon___23Zvv').next_sibling.strip()
        except AttributeError:
            rating = None

        try:
            delivery_info = restaurant.find('div', class_='numbersChild___2qKMV').find_all('div', class_='deliveryClock infoItemIcon___23Zvv')[0].next_sibling.strip().split('•')
            delivery_time = delivery_info[0].strip()
            distance = delivery_info[1].strip()
        except (AttributeError, IndexError):
            delivery_time = None
            distance = None

        try:
            promo_offer = restaurant.find('span', class_='discountText___GQCkj').text
        except AttributeError:
            promo_offer = None

        try:
            promo_available = bool(restaurant.find('div', class_='discount___3h-0m'))
        except AttributeError:
            promo_available = False

        # Restaurant ID, latitude, and longitude would require further analysis or access to another part of the site's data.
        # They are not visible in the provided HTML structure.

        restaurants.append({
            'name': name,
            'cuisine': cuisine,
            'rating': rating,
            'delivery_time': delivery_time,
            'distance': distance,
            'promo_offer': promo_offer,
            'promo_available': promo_available
        })

    # Create NDJSON data
    ndjson_data = '\n'.join(json.dumps(restaurant) for restaurant in restaurants)

    # Compress NDJSON data to gzip
    with gzip.open('restaurants.ndjson.gz', 'wt', encoding='utf-8') as gz_file:
        gz_file.write(ndjson_data)

    print("Data successfully written to restaurants.ndjson.gz")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

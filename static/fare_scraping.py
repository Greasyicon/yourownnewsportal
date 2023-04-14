import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd

def get_destination_prices(destinations, start_date, end_date):
    base_url = 'https://www.southwest.com'
    search_url = f'{base_url}/air/booking/select.html'
    flight_data = []

    for destination in destinations:
        for date in date_range(start_date, end_date):
            params = {
                'originationAirportCode': 'XXX',  # Replace with the departure airport code
                'destinationAirportCode': destination,
                'returnAirportCode': 'XXX',  # Replace with the departure airport code
                'departureDate': date.strftime('%Y-%m-%d'),
                'returnDate': '',  # Set a return date if necessary
                'adultPassengersCount': '1',
                'seniorPassengersCount': '0',
                'fareType': 'DOLLARS',
                'searchType': 'OW'
            }

            response = requests.get(search_url, params=params)
            soup = BeautifulSoup(response.text, 'html.parser')

            flights = soup.find_all('div', {'class': 'air-booking-select-detail'})
            for flight in flights:
                price_div = flight.find('div', {'class': 'fare-button--value'})
                if price_div:
                    price = float(price_div.get_text().replace('$', ''))
                    flight_data.append({
                        'date': date,
                        'destination': destination,
                        'price': price
                    })

    return flight_data

def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def get_all_destinations(departure_airport_code):
    url = f'https://www.southwest.com/flight/routemap_dyn.html?clk=GFOOTER-FLY-ROUTEMAP'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    origin_airport_tag = soup.find('option', {'value': departure_airport_code})
    if origin_airport_tag is None:
        raise ValueError(f'No airport found for code: {departure_airport_code}')

    destinations = []
    for tag in origin_airport_tag.find_next_siblings():
        dest_code = tag.get('value')
        if dest_code == "ZZZ":
            break
        destinations.append(dest_code)

    return destinations

if __name__ == '__main__':
    start_date = datetime.strptime('2023-05-01', '%Y-%m-%d')
    end_date = datetime.strptime('2023-12-31', '%Y-%m-%d')
    destinations = get_all_destinations('ORD')
    flight_data = get_destination_prices(destinations, start_date, end_date)

    # Save the data to a pandas DataFrame and sort by price
    df = pd.DataFrame(flight_data)
    df_sorted = df.sort_values(by='price', ascending=True)

    # Save the sorted data to a CSV file
    df_sorted.to_csv('cheapest_flights.csv', index=False)

    print(df_sorted.head())  # Print the top 5 cheapest flights

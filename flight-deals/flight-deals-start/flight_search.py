import requests
import os
from dotenv import load_dotenv

load_dotenv()

FLIGHT_SEARCH_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"



class FlightSearch:
    def __init__(self):
        self.api_key = os.environ["FLIGHT_API_KEY"]
        self.api_secret = os.environ["FLIGHT_API_SECRET"]
        self.token = self._get_token()

    def get_destination_code(self, city_name):
        params = {
            "keyword": city_name,
            "max": 2,
            "include": "AIRPORTS"
        }
        header = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url=FLIGHT_SEARCH_ENDPOINT, headers=header, params=params)
        data = response.json()
        try:
            destination_code = data["data"][0]["iataCode"]
        except KeyError:
            print(f"No flight path to {city_name}")
        else:
            return destination_code

    def _get_token(self):
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key ,
            "client_secret": self.api_secret
        }
        response = requests.post(url=IATA_ENDPOINT, headers=header, data=params)
        data = response.json()
        return data["access_token"]

    def get_flight_details(self,origin, destination, out_date, return_date, is_direct = "true"):
        header = {
            "Authorization": f"Bearer {self.token}"
        }
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": out_date,
            "returnDate": return_date,
            "adults": 1,
            "nonStop": is_direct,
            "currencyCode": "GBP",
            "max": 10,
        }
        response = requests.get(url=FLIGHT_ENDPOINT, params=params, headers=header)
        if response.status_code != 200:
            return None
        return response.json()
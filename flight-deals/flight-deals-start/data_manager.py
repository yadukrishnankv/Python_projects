import requests
import os
from dotenv import load_dotenv

load_dotenv()


class DataManager:
    def __init__(self):
        self.flight_endpoint = os.environ["SHEETY_FLIGHT_ENDPOINT"]
        self.user_endpoint = os.environ["SHEETY_USER_ENDPOINT"]
        self.token = os.environ["SHEETY_TOKEN"]
        self.sheet_data = {}
        self.customer_data = {}

    def get_sheet_data(self):
        header = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url=self.flight_endpoint, headers=header)
        data = response.json()
        self.sheet_data = data["prices"]
        return self.sheet_data

    def update_sheet_data(self):
        header = {
            "Authorization": f"Bearer {self.token}"
        }
        for city in self.sheet_data:
            params = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(url=f"{self.flight_endpoint}/{city["id"]}", headers=header, json=params)

    def get_user_email(self):
        header = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url=self.user_endpoint, headers=header)
        data = response.json()
        self.customer_data = data["users"]
        return self.customer_data
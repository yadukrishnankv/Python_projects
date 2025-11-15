from datetime import datetime, timedelta

from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import cheap_flight_search
from notification_manager import NotificationManager

#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

sheet_data = data_manager.get_sheet_data()

ORIGIN_IATA_CODE = "LON"

# for data in sheet_data:
#     if data["iataCode"] == "":
#         data["iataCode"] = flight_search.get_destination_code(data["city"])
#
# data_manager.update_sheet_data()
# sheet_data = data_manager.get_sheet_data()
user_data = data_manager.get_user_email()
user_list = [row["whatIsYourEmail?"] for row in user_data]

tomorrow = datetime.now() + timedelta(days=1)
six_months = datetime.now() + timedelta(days=6 * 30)

for city in sheet_data:
    print(f"Getting flights for {city["city"]}")
    flight = flight_search.get_flight_details(ORIGIN_IATA_CODE, city["iataCode"], tomorrow.strftime("%Y-%m-%d"), six_months.strftime("%Y-%m-%d"))
    cheapest_flight = cheap_flight_search(flight)
    if cheapest_flight.price == "N/A":
        print(f"There is no direct flight to {city["city"]}")
        step_overflight = flight_search.get_flight_details(ORIGIN_IATA_CODE, city["iataCode"], tomorrow.strftime("%Y-%m-%d"), six_months.strftime("%Y-%m-%d"), "false")
        cheapest_flight = cheap_flight_search(step_overflight)
    if cheapest_flight.price != "N/A" and float(cheapest_flight.price) < float(city["lowestPrice"]):
        notification_manager.send_whatsapp(
            message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
                         f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                         f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        )
        for user in user_list:
            notification_manager.send_email(
                message_body=f"Low price alert! Only GBP {cheapest_flight.price} to fly "
                             f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                             f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}.",
                to_addr=user
            )
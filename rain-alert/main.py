import requests
from twilio.rest import Client

account_sid = 'ADD YOUR ACCOUNT SID'
auth_token = 'ADD YOUR TOKEN'
api_key =  "ADD YOUR API KEY"

parameters = {
    "lat": 10.762600,
    "lon": 76.269402,
    "appid": api_key,
    "cnt": 4,
}


response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()
weather_data = response.json()["list"]
will_rain = False
for data in weather_data:
    weather_id = data["weather"][0]["id"]
    if int(weather_id) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        messaging_service_sid='MG119abae4a1880a2a0362d1bce38926fe',
        body='It might rain today, Bring an Umbrella.',
        to='ADD YOUR NUMBER'
    )

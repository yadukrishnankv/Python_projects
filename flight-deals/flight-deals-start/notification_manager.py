import os
from twilio.rest import Client
from dotenv import load_dotenv
import smtplib

load_dotenv()

class NotificationManager:
    def __init__(self):
        self.email_id = os.environ["EMAIL_ID"]
        self.email_pass = os.environ["EMAIL_PASSWORD"]
        self.account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        self.auth_token = os.environ["TWILIO_AUTH_TOKEN"]

    def send_whatsapp(self, message_body):
        client = Client(self.account_sid, self.auth_token)
        message = client.messages.create(
            from_="whatsapp:+14155238886",
            body=message_body,
            to="whatsapp:+918075797927"
        )
        print(message.sid)

    def send_email(self, message_body, to_addr):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self.email_id, password=self.email_pass)
            connection.sendmail(
                from_addr=self.email_id,
                to_addrs=to_addr,
                msg=message_body
            )
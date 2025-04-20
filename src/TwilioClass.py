import os

from twilio.rest import Client
from dotenv import load_dotenv
from rich import print

from rich.traceback import install

install(show_locals=True)


class TwilioClass:
    def __init__(self):
        self.load_dotenv()
        self.client = self.get_twilio_client()
        self.TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

    def load_dotenv(self):
        load_dotenv()

    def get_twilio_client(self):
        self.TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
        self.TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
        self.client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)
        return self.client

    def send_message(self, body, to):
        self.body = body
        self.to = to
        self.message = self.client.messages.create(
            body=self.body, from_=f"{self.TWILIO_PHONE_NUMBER}", to=f"{self.to}"
        )
        print(self.message)


# if __name__ == "__main__":
#     twilio_client = TwilioClient()
#     twilio_client.send_message("NEVER", "+")

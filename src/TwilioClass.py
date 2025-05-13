import os

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv
from rich import print

from rich.traceback import install
from config import load_twilio_config

install(show_locals=True)
twilio_config = load_twilio_config()


class TwilioClient:
    def __init__(self):
        self.load_dotenv()
        self.client = self.get_twilio_client()
        self.twilio_phone_number = twilio_config.twilio_phone_number
        # self.TWILIO_PHONE_NUMBER = os.environ["TWILIO_PHONE_NUMBER"]

    def load_dotenv(self):
        load_dotenv()

    def get_twilio_client(self):
        self.twilio_account_sid = twilio_config.twilio_account_sid
        self.twilio_auth_token = twilio_config.twilio_auth_token
        # self.TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
        # self.TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
        self.client = Client(self.twilio_account_sid, self.twilio_auth_token)
        return self.client

    #  TODO: add check for if the phone number is blocked on twilio side, typically because their opt-out message was missed by this app. Remove that user from my nocodb list
    def send_message(self, body, to):
        self.body = str(body)
        self.to = f"+{to}"
        self.message = self.client.messages.create(
            body=self.body, from_=f"{self.TWILIO_PHONE_NUMBER}", to=f"{self.to}"
        )
        print(self.message)


# if __name__ == "__main__":
#     twilio_client = TwilioClient()
#     twilio_client.send_message("NEVER", "+18649580133")

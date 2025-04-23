import os

import dotenv
from flask import Flask, request, redirect
from rich import print
from rich.traceback import install
from twilio.twiml.messaging_response import MessagingResponse

import TwilioClass
import NocoClass

install(show_locals=True)

# class FlaskClass(Flask):


app = Flask(__name__)
twilio = TwilioClass.TwilioClass()
nocodb = NocoClass.NocoClass()


@app.route("/", methods=["GET", "POST"])
def hello():
    return "Hello, World!"


@app.route("/sms", methods=["GET", "POST"])
def sms_reply():
    """Respond to incoming messages with a text message."""
    # Start our TwiML response
    body = request.values.get("Body", None)
    print(request.values)

    resp = MessagingResponse()
    # TODO: change all if/elif statements to check a dictionary for the body. Make sure it matches the list in twilio opt in/out list

    if body == "updates" or body == "update" or body == "Updates":
        sender_phone_number = request.values.get("From", None)
        sender_phone_number.replace("+", "")
        int(sender_phone_number)
        nocodb.add_subscriber(sender_phone_number)
        # resp.message(
        #     "Thank you for signing up for updates form -building. We will keep these updates minimal but make sure you recive the info you need from our church. If at any point you wish to stop reciving these updates, simply reply 'stop'."
        # )

        # TODO: check if they are already in the list

    elif body == "stop" or body == "STOP" or body == "Stop":
        sender_phone_number = request.values.get("From", None)
        sender_phone_number.replace("+", "")
        int(sender_phone_number)
        nocodb.remove_subscriber(sender_phone_number)
        # resp.message(
        #     "You have been unsubscribed from updates. If you wish to resubscribe, simply reply 'updates'."
        # )
        # TODO: check if they are actually in the list before removing them to avoid errors

    else:
        # TODO: check if they are subscribed to customize this message
        resp.message(
            "Thank you for messaging -building. If you are looking for updates, please reply 'updates'. If you wish to stop reciving updates, simply reply 'stop'."
        )

    return str(resp)


if __name__ == "__main__":
    app.run(port=80, debug=True)

import os

from flask import Flask, request, redirect
from rich import print
from rich.traceback import install
from twilio.twiml.messaging_response import MessagingResponse

import TwilioClass
import NocoClass

install(show_locals=True)

# class FlaskClass(Flask):
from config import TwilioConfig, TextKeywords

app = Flask(__name__)
twilio = TwilioClass.TwilioClient()
nocodb = NocoClass.NocoClass()
text_keywords = TextKeywords()


@app.route("/", methods=["GET", "POST"])
def hello():
    return "Hello, World!"


@app.route("/sms", methods=["GET", "POST"])
def sms_reply():
    """Respond to incoming messages with a text message."""
    # Start our TwiML response
    body = request.values.get("Body", None)
    body = body.strip()
    body = body.lower()
    print(request.values)

    resp = MessagingResponse()
    # TODO: check if message is item in list, if not send them the help message
    # TODO: finish using the dictionary to check for the group a user needs to be added to
    # TODO: make messages not hardcoded so its easier to change in the future
    for keyword, group_data in text_keywords.text_update_groups.items():
        if keyword == body:
            sender_phone_number = request.values.get("From", None)
            subscriber_status = nocodb.check_if_subscribed(
                subscriber_number=sender_phone_number, group=group_data.nocodb_tag
            )
            sender_phone_number.replace("+", "")
            int(sender_phone_number)
            if subscriber_status:
                resp.message(
                    "You are already subscribed to updates. If you wish to stop reciving these updates, simply reply 'stop'."
                )
            else:
                nocodb.add_subscriber(sender_phone_number, group=group_data.nocodb_tag)
                resp.message(
                    "Welcome to one of the best text message thread you will ever be a part of. You have opted in to get text message updates for the Kingdom Outpost. We can’t wait to share more with you about what God is doing. If at any point you wish to stop reciving these updates, simply reply 'stop'.Msg&Data Rates May Apply."
                )
        # TODO: Make check to see if subsciber is in list before removing them. Could cause error if they arent
        elif body == "stop":
            sender_phone_number = request.values.get("From", None)
            sender_phone_number.replace("+", "")
            int(sender_phone_number)
            nocodb.remove_subscriber(sender_phone_number)
            resp.message(
                "You have been unsubscribed from updates. If you wish to resubscribe, simply reply 'updates'."
            )
        else:
            resp.message(
                "Thank you for messaging us. If you are looking for updates, please reply 'updates'. If you wish to stop reciving updates, simply reply 'stop'."
            )

    return str(resp)


# if __name__ == "__main__":
#     app.run(port=80, debug=True)

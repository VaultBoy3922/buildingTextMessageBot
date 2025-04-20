import dotenv
from flask import Flask, request, redirect
from rich import print
from rich.traceback import install
from twilio.twiml.messaging_response import MessagingResponse

import TwilioClass

install(show_locals=True)

# class FlaskClass(Flask):

app = Flask(__name__)
twilio = TwilioClass()


@app.route("/sms", methods=["GET", "POST"])
def sms_reply():
    """Respond to incoming messages with a text message."""
    # Start our TwiML response
    body = request.values.get("Body", None)

    resp = MessagingResponse()

    if body == "updates" or body == "update":
        resp.message(
            "Thank you for signing up for updates form -building. We will keep these updates minimal but make sure you recive the info you need from our church. If at any point you wish to stop reciving these updates, simply reply 'stop'."
        )
        # TODO: add user to nocodb Subscribers list and check if they are already in the list

    elif body == "stop" or body == "STOP":
        resp.message(
            "You have been unsubscribed from updates. If you wish to resubscribe, simply reply 'updates'."
        )
        # TODO: remove user from nocodb Subscribers list and check if they are actually in the list
        resp.message(
            "Thank you for messaging -building. If you are looking for updates, please reply 'updates'. If you wish to stop reciving updates, simply reply 'stop'."
        )


if __name__ == "__main__":
    app.run(port=5000, debug=True)

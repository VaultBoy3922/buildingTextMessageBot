import dotenv
from flask import Flask, request, redirect
from rich import print
from rich.traceback import install
from twilio.twiml.messaging_response import MessagingResponse

install(show_locals=True)

# class FlaskClass(Flask):

app = Flask(__name__)


@app.route("/sms", methods=["GET", "POST"])
def sms_reply():
    """Respond to incoming messages with a text message."""
    # Start our TwiML response
    resp = MessagingResponse()
    # Add a message
    resp.message("The Robots are coming! Head for the hills!")
    return str(resp)


if __name__ == "__main__":
    app.run(port=80, debug=True)

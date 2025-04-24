import os
import subprocess

import discord
from dotenv import load_dotenv
from rich import print
from rich.traceback import install

from DiscordClass import MyClient

install(show_locals=True)


# TODO: add print statements to a log file instead of the console
def main():
    # Start the Flask app through wsgi
    # subprocess.run(["shell", "uwsgi --socket 0.0.0.0:80 --protocol=http wsgi:app"])

    # Start the Discord bot
    client = MyClient(intents=discord.Intents.all())
    client.run(client.TOKEN)


if __name__ == "__main__":
    main()

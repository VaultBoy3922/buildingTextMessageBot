import os
import subprocess

import discord

from rich import print
from rich.traceback import install

from DiscordClass import MyClient

install(show_locals=True)


# TODO: add print statements to a log file instead of the console
def main():
    # Start the Flask app through wsgi
    # subprocess.run(["shell", "uwsgi --socket 0.0.0.0:80 --protocol=http wsgi:app"])

    # Start the Discord bot
    print("Starting Discord bot...")
    client = MyClient(intents=discord.Intents.all())
    print("Discord bot started.")
    print("Running Discord bot...")
    client.run(client.bot_token)


if __name__ == "__main__":
    main()

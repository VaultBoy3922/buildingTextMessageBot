import os

import discord
from dotenv import load_dotenv
from rich import print
from rich.traceback import install

from DiscordClass import MyClient

install(show_locals=True)


def main():
    client = MyClient(intents=discord.Intents.all())
    client.run(client.TOKEN)


if __name__ == "__main__":
    main()

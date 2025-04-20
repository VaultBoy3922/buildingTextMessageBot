import os

import discord
from dotenv import load_dotenv
from rich import print
from rich.traceback import install

install(show_locals=True)


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.envFile = None
        self.load_dotenv()
        self.TOKEN = os.getenv("DISCORD_TOKEN")
        self.GUILD = os.getenv("DISCORD_GUILD")

    def load_dotenv(self):
        load_dotenv()

    async def on_ready(self):
        guild = discord.utils.get(self.guilds, name=self.GUILD)
        print(
            f"Logged in as {self.user} in the following guild:\n"
            f"{guild.name}(id: {guild.id})\n"
            f"-------------------------"
        )

    # This event triggers when a message is sent in the Announcements channel
    # and the bot is mentioned
    async def on_message(self, message):
        self.ANNOUNCEMENTS_CHANNEL_ID = os.getenv("ANNOUNCEMENTS_CHANNEL_ID")
        # Ignore messages from the bot itself
        if message.author == self.user:
            return
        # Check if the message is in the Announcements channel
        if message.channel.id == self.ANNOUNCEMENTS_CHANNEL_ID:
            print(f"Message from {message.author}: {message.content}")
            if message.mentions == self.user:
                print(f"Message from {message.author}: {message.content}")
            else:
                return
        print(f"Message from {message.author}: {message.content}")

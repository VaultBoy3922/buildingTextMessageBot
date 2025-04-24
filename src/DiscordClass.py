import os
import time

import discord
from dotenv import load_dotenv
from rich import print
from rich.traceback import install

import TwilioClass
import NocoClass


install(show_locals=True)
TwilioClass = TwilioClass.TwilioClient()
NocoClass = NocoClass.NocoClass()


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.envFile = None
        self.load_dotenv()
        self.TOKEN = os.environ["DISCORD_TOKEN"]
        self.GUILD = os.environ["DISCORD_GUILD"]
        self.DISCORD_BOT_ID = os.environ["DISCORD_BOT_ID"]

    def load_dotenv(self):
        load_dotenv()

    def __check_if_mentioned(self, message):
        self.discord_message = message
        self.id_to_check = f"<@&{self.DISCORD_BOT_ID}>"
        if self.id_to_check in self.discord_message:
            return True
        else:
            return False

    def __check_channel_id(self, message_channel: int, channel_id: int):
        print(f"Message channel: {message_channel}")
        print(f"Channel id: {channel_id}")
        if str(message_channel) == str(channel_id):
            return True
        else:
            return False

    def __send_message_to_subscribers(self, message_content):
        self.message_content = message_content
        NocoClass.authorize()
        print(f"Message content: {self.message_content}")
        self.message_content = self.message_content.replace(
            f"<@&{self.DISCORD_BOT_ID}> ", ""
        )
        print(f"Message content: {self.message_content}")
        for i in NocoClass.subscriber_list:
            TwilioClass.send_message(
                body=self.message_content, to=f"+{i['PhoneNumber']}"
            )
            time.sleep(1)

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

        # print(f"Message from {message.author}: {message.content}")
        # print(message.channel.id)
        # print(self.message)
        self.message = message
        self.ANNOUNCEMENT_CHANNEL_ID = os.environ["ANNOUNCEMENT_CHANNEL_ID"]

        # print(f"Announcement channel id: {self.ANNOUNCEMENT_CHANNEL_ID}")
        # print(f"Channel id: {self.message.channel.id}")
        # print(f"Message mentions: {self.message.content.mentions}")
        # print(self.message.content)
        # Ignore messages from the bot itself

        if self.message.author == self.user:
            print("Message from bot")
            return
        # print(self.message.channel.id)
        # print(self.ANNOUNCEMENT_CHANNEL_ID)

        # Check if the message is in the Announcements channel
        channel_id_check = self.__check_channel_id(
            message.channel.id, self.ANNOUNCEMENT_CHANNEL_ID
        )
        # print(f"Channel id check: {channel_id_check}")
        # Check if the bot is mentioned
        check_if_mentioned = self.__check_if_mentioned(message.content)
        print(f"Check if mentioned: {check_if_mentioned}")

        if self.__check_channel_id(message.channel.id, self.ANNOUNCEMENT_CHANNEL_ID):
            print(f"check for channel id")
            if self.__check_if_mentioned(message.content):
                print(f"check for mention")
                self.__send_message_to_subscribers(message.content)
            else:
                print("Not a mention")
                return
        else:
            return
        print(f"Message from {message.author}: {message.content}")

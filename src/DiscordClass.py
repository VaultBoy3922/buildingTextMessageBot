import os
import time

import discord

from rich import print
from rich.traceback import install

import TwilioClass
import NocoClass
from config import load_discord_bot_config, load_text_update_groups


install(show_locals=True)
TwilioClass = TwilioClass.TwilioClient()
NocoClass = NocoClass.NocoClass()
config_data = load_discord_bot_config()
update_groups = load_text_update_groups()


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.envFile = None
        self.bot_token = config_data.bot_token
        self.guild = config_data.guild
        self.bot_id = config_data.bot_id
        # self.TOKEN = os.environ["DISCORD_TOKEN"]
        # self.GUILD = os.environ["DISCORD_GUILD"]
        # self.DISCORD_BOT_ID = os.environ["DISCORD_BOT_ID"]

    def __check_if_mentioned(self, message):
        self.discord_message = message
        print(f"Discord message: {self.discord_message}")
        self.id_to_check = f"<@&{self.bot_id}>"
        if self.id_to_check in self.discord_message:
            return True
        else:
            return False

    # def __check_channel_id(self, message_channel: int, channel_id: int):
    #     print(f"Message channel: {message_channel}")
    #     print(f"Channel id: {channel_id}")
    #     if str(message_channel) == str(channel_id):
    #         return True
    #     else:
    #         return False

    def __send_message_to_subscribers(self, message_content, group):
        self.message_content = message_content
        NocoClass.authorize()
        print(f"Message content: {self.message_content}")
        self.message_content = self.message_content.replace(f"<@&{self.bot_id}> ", "")
        print(f"Message content: {self.message_content}")

        for i in NocoClass.subscriber_list:
            if group in i[f"{NocoClass.subscriber_type_column}"]:
                print(f"Sending message to {i['PhoneNumber']}")
                TwilioClass.send_message(
                    body=self.message_content, to=f"+{i['PhoneNumber']}"
                )
            else:
                print(f"Subscriber {i['PhoneNumber']} is not in group {group}")
            time.sleep(1)

    async def on_ready(self):
        guild = discord.utils.get(self.guilds, name=self.guild)
        print(
            f"Logged in as {self.user} in the following guild:\n"
            f"{guild.name}(id: {guild.id})\n"
            f"-------------------------"
        )

    # This event triggers when a message is sent in the Announcements channel
    # and the bot is mentioned
    # TODO: add a check to see if bot needs to add text infront of the message to indicate which group it comes from
    async def on_message(self, message):
        self.message = message

        if self.message.author == self.user:
            print("Message from bot")
            return
        if self.__check_if_mentioned(self.message.content):
            print("Message is a mention")
        else:
            print("Message is not a mention")
            return
        for keyword, group_data in update_groups.text_update_groups.items():
            print(f"Keyword: {keyword}")
            print(f"Group data: {group_data}")
            if group_data.discord_channel_id == self.message.channel.id:
                print(f"Message is in a update group channel")
                self.__send_message_to_subscribers(
                    self.message.content, group=group_data.nocodb_tag
                )
                break
            else:
                print("Message is not in a update group channel")

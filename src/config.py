import os
import yaml
from rich import print
from typing_extensions import Dict

from rich.traceback import install
from pydantic import BaseModel, Field

# TODO: use pydantic to validate the config file
# TODO: find a way to create a model for the different text sign ups. These do not have set types and are changing depending on the users needs
# TODO: write down a config flow to plan how program will handle these variables and the text sign up flow
install(show_locals=True)


# cwd = os.getcwd()
# print(f"Current working directory: {cwd}")
class TwilioConfig(BaseModel):
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str


class DiscordBotConfig(BaseModel):
    guild: str
    bot_token: str
    bot_id: int


class NocoDBConfig(BaseModel):
    api_key: str
    url: str
    subscriber_tableid: str
    subscriber_baseid: str
    subscriber_viewid: str
    subscriber_type_column: str


class GroupConfig(BaseModel):
    discord_channel: str
    discord_channel_id: int
    nocodb_tag: str
    sign_up_via_text: bool


class TextKeywords(BaseModel):
    text_update_groups: Dict[str, GroupConfig] = Field(default_factory=dict)


def read_config():
    with open(f"src/config.yml", "r") as file:
        config_data = yaml.safe_load(file)
    return config_data


def load_twilio_config():
    config_data = read_config()
    return TwilioConfig(**config_data["twilio_config"])


def load_nocodb_data():
    config_data = read_config()
    return NocoDBConfig(**config_data["nocodb_config"])


def load_discord_bot_config():
    config_data = read_config()
    return DiscordBotConfig(**config_data["discord_bot_config"])


def load_text_update_groups():
    config_data = read_config()
    return TextKeywords(**config_data)


# if __name__ == "__main__":
#     config = read_config()
# text_update_groups = load_text_update_groups(config)

# for group_name, group in text_update_groups.text_update_groups.items():
#     print(
#         f"Group {group_name} → channel {group.discord_channel_id} {group.discord_channel}"
#     )

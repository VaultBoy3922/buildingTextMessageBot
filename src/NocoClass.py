import os
from datetime import datetime

import dotenv
import requests
from rich import print
from rich.traceback import install

from config import load_nocodb_data


install(show_locals=True)
config_data = load_nocodb_data()

class NocoClass:
    def __init__(self):
        self.api_key = config_data.api_key
        self.url = config_data.url
        self.subscriber_tabelid = config_data.subscriber_tableid
        self.subscriber_baseid = config_data.subscriber_baseid
        self.subscriber_viewid = config_data.subscriber_viewid
        self.subscriber_type_column = config_data.subscriber_type_column
        self.tableid_url = (
            f"{self.url}/api/v2/tables/{self.subscriber_tabelid}/records"
        )
        self.baseid_url = (
            f"{self.url}/api/v2/meta/bases/{self.subscriber_baseid}/info"
        ) 
        # self.NOCODB_API_KEY = os.environ["NOCODB_API_KEY"]
        # self.SUBSCRIBER_NOCODB_TABLEID = os.environ["SUBSCRIBER_NOCODB_TABLEID"]
        # self.SUBSCRIBER_NOCODB_BASEID = os.environ["SUBSCRIBER_NOCODB_BASEID"]
        # self.NOCODB_URL = os.environ["NOCODB_URL"]
        # self.tableid_url = (
        #     f"{self.NOCODB_URL}/api/v2/tables/{self.SUBSCRIBER_NOCODB_TABLEID}/records"
        # )
        # self.baseid_url = (
        #     f"{self.NOCODB_URL}/api/v2/meta/bases/{self.SUBSCRIBER_NOCODB_BASEID}/info"
        # )
        # self.SUBSCRIBER_NOCODB_VIEWID = os.environ["SUBSCRIBER_NOCODB_VIEWID"]

        self.authorize()

    def authorize(self):
        self.querystring = {
            "offset": "0",
            "limit": "25",
            "where": "",
            "viewId": f"{self.subscriber_viewid}",
        }
        self.headers = {"xc-token": f"{self.api_key}"}
        self.response = requests.request(
            "GET", self.tableid_url, headers=self.headers, params=self.querystring
        )
        self.get_subscribers()

    def get_subscribers(self):
        self.subscriber_json = self.response.json()
        self.subscriber_list = self.subscriber_json["list"]

    # def get_subscriber_from_group(self, group):
    #     self.group = group
    #     self.get_subscribers()
        
        # print(self.subscriber_list)

    def add_subscriber(self, phone_number, group, name=None):
        self.phone_number = phone_number
        self.name = name
        self.group = group
#TODO: decide if its worth it to hardcode the subscriber schema or create variable for all these options
        self.schema = {
            "Name": f"{self.name}",
            "PhoneNumber": int(self.phone_number),
            "DateSubscribed": f"{datetime.today().strftime('%Y-%m-%d')}",
            "Subscribed": "true",
            f"{self.subscriber_type_column}": f"{group}"
        }
        self.put_response = requests.request(
            "POST",
            self.tableid_url,
            headers=self.headers,
            params=self.querystring,
            data=self.schema,
        )

    def remove_subscriber(self, subscriber_number):
        self.subscriber_number = subscriber_number
        for i in self.subscriber_list:
            if i["PhoneNumber"] == int(self.subscriber_number):
                self.id_number = i["Id"]
                break
            else:
                pass
        self.schema = {"Id": int(self.id_number)}
        self.delete_response = requests.request(
            "DELETE",
            self.tableid_url,
            headers=self.headers,
            params=self.querystring,
            data=self.schema,
        )
    def check_if_subscribed(self, subscriber_number, group_to_check):
        self.subscriber_number = subscriber_number
        self.group_to_check = group_to_check
        self.authorize()
        self.result = bool
        for i in self.subscriber_list:
            if f"+{i["PhoneNumber"]}" == self.subscriber_number:
                if i[f"{self.subscriber_type_column}"] == self.group_to_check:
                    self.result = True
                    break
            else:
                self.result = False
        return self.result
        


# if __name__ == "__main__":
#     # Test the NocoClass
#     dotenv.load_dotenv()
#     NocoClass = NocoClass()
#     NocoClass.remove_subscriber(subscriber_number="5555555555")

import os
from datetime import datetime

import dotenv
import requests
from rich import print
from rich.traceback import install

install(show_locals=True)


class NocoClass:
    def __init__(self):

        self.NOCODB_API_KEY = os.environ["NOCODB_API_KEY"]
        self.SUBSCRIBER_NOCODB_TABLEID = os.environ["SUBSCRIBER_NOCODB_TABLEID"]
        self.SUBSCRIBER_NOCODB_BASEID = os.environ["SUBSCRIBER_NOCODB_BASEID"]
        self.NOCODB_URL = os.environ["NOCODB_URL"]
        self.tableid_url = (
            f"{self.NOCODB_URL}/api/v2/tables/{self.SUBSCRIBER_NOCODB_TABLEID}/records"
        )
        self.baseid_url = (
            f"{self.NOCODB_URL}/api/v2/meta/bases/{self.SUBSCRIBER_NOCODB_BASEID}/info"
        )
        self.SUBSCRIBER_NOCODB_VIEWID = os.environ["SUBSCRIBER_NOCODB_VIEWID"]

        self.authorize()

    def authorize(self):
        # TODO: add authorization to nocodb api
        self.querystring = {
            "offset": "0",
            "limit": "25",
            "where": "",
            "viewId": f"{self.SUBSCRIBER_NOCODB_VIEWID}",
        }
        self.headers = {"xc-token": f"{self.NOCODB_API_KEY}"}
        self.response = requests.request(
            "GET", self.tableid_url, headers=self.headers, params=self.querystring
        )
        self.get_subscribers()

    def get_subscribers(self):
        # TODO: get subscribers from nocodb api and return them as a list/json
        self.subscriber_json = self.response.json()
        self.subscriber_list = self.subscriber_json["list"]
        # print(self.subscriber_list)

    def add_subscriber(self, phone_number, name=None):
        self.phone_number = phone_number
        self.name = name

        self.schema = {
            "Name": f"{self.name}",
            "PhoneNumber": int(self.phone_number),
            "DateSubscribed": f"{datetime.today().strftime('%Y-%m-%d')}",
            "Sbuscribed": "true",
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


# if __name__ == "__main__":
#     # Test the NocoClass
#     dotenv.load_dotenv()
#     NocoClass = NocoClass()
#     NocoClass.remove_subscriber(subscriber_number="5555555555")

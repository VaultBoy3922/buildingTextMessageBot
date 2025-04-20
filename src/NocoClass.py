import dotenv


class NocoClass:
    def __init__(self):

        self.NOCODB_API_KEY = dotenv.get("NOCODB_API_KEY")
        self.SUBSCRIBER_NOCODB_TABLEID = dotenv.get("SUBSCRIBER_NOCODB_TABLEID")
        self.SUBSCRIBER_NOCODB_BASEID = dotenv.get("SUBSCRIBER_NOCODB_BASEID")
        self.NOCODB_URL = dotenv.get("NOCODB_URL")
        self.tableid_url = (
            f"{self.NOCODB_URL}/api/v2/tables/{self.SUBSCRIBER_NOCODB_TABLEID}/records"
        )
        self.baseid_url = (
            f"{self.NOCODB_URL}/api/v2/meta/bases/{self.SUBSCRIBER_NOCODB_BASEID}/info"
        )

    def authorize(self):
        # TODO: add authorization to nocodb api
        pass

    def get_subscribers(self):
        # TODO: get subscribers from nocodb api and return them as a list/json
        pass

import requests, urllib.parse
import os
import dotenv


class SendMessage:
    def __init__(self, message, number):
        self.message = message
        self.number = number

        self.send_message(message=self.message, number=self.number)

    def send_message(self, message, number):
        self.params = (
            ("apikey", os.getenv("SMS_API_KEY")),
            ("message", message),
            ("number", ",".join(number)),
        )
        try:
            path = "https://semaphore.co/api/v4/messages?" + urllib.parse.urlencode(
                self.params
            )
        except KeyError as err:
            print("Check your API Key", err)
        except requests.exceptions.HTTPError as err:
            print(err)
        except err:
            print("something went wrong", err)
        else:
            requests.post(path)
            print(path)  # get the output link for debugging!

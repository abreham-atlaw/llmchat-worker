import typing

import requests
import time
from abc import ABC, abstractmethod


class RequestProcessor(ABC):

    def __init__(self, host: str, model_id: str):
        self.host = host
        self.__model_id = model_id

    @abstractmethod
    def handle(self, request) -> typing.Any:
        pass

    def get_request(self):
        url = f"{self.host}/api/request/get?model={self.__model_id}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data["response"] is None:
            request_id = data["id"]
            query = data["params"]
            return request_id, query
        else:
            return None, None

    def send_response(self, request_id, response):
        url = f"{self.host}/api/request/respond"
        payload = {
            "id": request_id,
            "response": response
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Response recorded")
        else:
            print("Failed to send response")

    def start(self):
        while True:
            request_id, params = self.get_request()
            if request_id and params:
                processed_response = self.handle(params)
                self.send_response(request_id, processed_response)
            time.sleep(1)  # Wait for 1 second before checking for the next request


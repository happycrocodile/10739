import requests

class Middleware:
    def __init__(self, settings: dict) -> None:
        self.__base = settings["base"]

    def get(self, *options: tuple, url: str=None):
        if url == None:
            url = self.__base
            for option in options:
                url = url + "/" + str(option)

        try:
            response = requests.get(url=url).json()
            return response
        except:
            raise NameError(f"Error executing request {url}")

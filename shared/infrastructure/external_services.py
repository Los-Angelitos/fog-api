from dotenv import load_dotenv
import requests, os

load_dotenv()

class ExternalService:
    def __init__(self):
        self.base_url = os.getenv("EXTERNAL_SERVICE_URL", "https://sweet-manager-api.runasp.net/api/v1")

    def get(self, endpoint: str, params: dict = None):
        """
        Makes a GET request to the external service.

        :param endpoint: The endpoint to call.
        :param params: Optional parameters for the request.
        :return: The response from the external service.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
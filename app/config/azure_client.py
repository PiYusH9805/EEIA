import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class AzureClient:

    _client = None

    @classmethod
    def get_client(cls):

        if cls._client is None:

            cls._client = OpenAI(
                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                base_url=os.getenv("AZURE_OPENAI_ENDPOINT")
            )

        return cls._client


client = AzureClient.get_client()

deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
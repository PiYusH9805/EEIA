import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / '.env')


class AzureClient:
    """Initialize on demand so missing configuration does not break the UI."""
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            from openai import OpenAI, AzureOpenAI
            key = os.getenv('AZURE_OPENAI_API_KEY')
            endpoint = os.getenv('AZURE_OPENAI_ENDPOINT', '').rstrip('/')
            if not key or not endpoint or not os.getenv('AZURE_OPENAI_DEPLOYMENT'):
                raise ValueError('Configure AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_DEPLOYMENT in .env.')
            options = dict(api_key=key, timeout=60.0, max_retries=1)
            if '/openai/v1' in endpoint:
                cls._client = OpenAI(base_url=endpoint + '/', **options)
            else:
                cls._client = AzureOpenAI(azure_endpoint=endpoint,
                    api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-10-21'), **options)
        return cls._client

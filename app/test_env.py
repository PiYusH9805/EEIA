import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 50)

print("API KEY:", bool(os.getenv("AZURE_OPENAI_API_KEY")))
print("ENDPOINT:", os.getenv("AZURE_OPENAI_ENDPOINT"))
print("DEPLOYMENT:", os.getenv("AZURE_OPENAI_DEPLOYMENT"))
print("API VERSION:", os.getenv("AZURE_OPENAI_API_VERSION"))

print("=" * 50)
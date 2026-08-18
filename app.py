import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

print("Endpoint:", os.getenv("AZURE_OPENAI_ENDPOINT"))
print("Deployment:", os.getenv("AZURE_OPENAI_DEPLOYMENT"))

client = OpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT")
)

deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")

while True:

    query = input("You: ")

    if query.lower() == "exit":
        break

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {
                "role": "user",
                "content": query
            }
        ]
    )

    print("AI:", response.choices[0].message.content)
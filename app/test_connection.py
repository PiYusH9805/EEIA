from app.config.azure_client import client, deployment_name

response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {
            "role": "user",
            "content": "Reply with only the word: Connected"
        }
    ],
    temperature=0
)

print(response.choices[0].message.content)
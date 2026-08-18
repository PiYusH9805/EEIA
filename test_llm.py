from service.llm_service import LLMService

messages = [
    {
        "role": "user",
        "content": "Say Hello"
    }
]

response = LLMService.chat(messages)

print(response)

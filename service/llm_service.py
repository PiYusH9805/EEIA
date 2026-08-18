from app.config.azure_client import client, deployment_name


class LLMService:

    @staticmethod
    def chat(messages, temperature=0, response_format=None):
        """
        Generic Azure OpenAI Chat Completion Service
        """

        params = {
            "model": deployment_name,
            "messages": messages,
            "temperature": temperature
        }

        if response_format:
            params["response_format"] = response_format

        response = client.chat.completions.create(**params)

        return response.choices[0].message.content
    
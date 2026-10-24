class MemoryService:
    """Session-owned bounded memory, never shared between users."""
    def __init__(self, max_messages=20, max_characters=16000):
        self.history = []
        self.max_messages = max_messages
        self.max_characters = max_characters

    def add_message(self, role, content):
        if role not in ('user', 'assistant'):
            raise ValueError('Invalid conversation role.')
        self.history.append({'role': role, 'content': str(content)[:self.max_characters // 2]})
        while len(self.history) > self.max_messages or sum(len(x['content']) for x in self.history) > self.max_characters:
            self.history.pop(0)
        while self.history and self.history[0]['role'] != 'user':
            self.history.pop(0)

    def get_history(self):
        return [dict(message) for message in self.history]

    def clear(self):
        self.history.clear()

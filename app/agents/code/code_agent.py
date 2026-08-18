from app.services.repository_service import RepositoryService
from app.services.symbol_service import SymbolService
from app.services.search_service import SearchService
from app.services.llm_service import LLMService
from app.services.file_metrics_service import FileMetricsService

from app.tools.file_reader import FileReader

from app.agents.code.prompt import (
    CODE_AGENT_SYSTEM_PROMPT
)


class CodeAgent:

    def __init__(self):

        self.repository = RepositoryService()
        self.reader = FileReader(".")
        self.search = SearchService()
        self.symbol = SymbolService()

    def ask(self, question):

        # =====================================
        # FILE INTELLIGENCE
        # =====================================

        if ".py" in question:

            file_name = None

            for word in question.split():

                word = word.strip("\"'.,()[]{}")

                if word.endswith(".py"):

                    file_name = word
                    break

            if file_name:

                path = self.search.find_file(file_name)

                if path:

                    code = self.reader.read(path)

                    metrics = FileMetricsService.analyze(code)

                    messages = [

                        {
                            "role": "system",
                            "content": CODE_AGENT_SYSTEM_PROMPT
                        },

                        {
                            "role": "user",
                            "content": f"""

Explain this Python file in detail.

━━━━━━━━━━━━━━━━━━━━━━

File Name:
{file_name}

Location:
{path}

━━━━━━━━━━━━━━━━━━━━━━

FILE METRICS

Lines : {metrics['lines']}

Functions : {metrics['functions']}

Classes : {metrics['classes']}

Imports : {metrics['imports']}

━━━━━━━━━━━━━━━━━━━━━━

Source Code

{code}

━━━━━━━━━━━━━━━━━━━━━━

Please explain in this format:

1. File Purpose

2. Architecture Role

3. Functions

4. Classes

5. Imports

6. Execution Flow

7. Related Files

8. Improvements

9. Best Practices

"""
                        }

                    ]

                    return LLMService.chat(messages)

        # =====================================
        # SYMBOL INTELLIGENCE
        # =====================================

        words = question.replace("?", "").split()

        for word in words:

            result = self.symbol.find(word)

            if result:

                code = self.reader.read(result["file"])

                messages = [

                    {
                        "role": "system",
                        "content": CODE_AGENT_SYSTEM_PROMPT
                    },

                    {
                        "role": "user",
                        "content": f"""

Explain this {result['type']}.

Name:
{word}

File:
{result['file']}

Line:
{result['line']}

Source Code

{code}

Explain:

Purpose

Inputs

Outputs

Execution

Related Functions

Suggestions

"""
                    }

                ]

                return LLMService.chat(messages)

        # =====================================
        # REPOSITORY INTELLIGENCE
        # =====================================

        context = self.repository.get_repository_context()

        messages = [

            {
                "role": "system",
                "content": CODE_AGENT_SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content": f"""

Repository Context

{context}

Question

{question}

Please explain:

Project Architecture

Folder Structure

Dependencies

Execution Flow

Suggestions

"""
            }

        ]

        return LLMService.chat(messages)
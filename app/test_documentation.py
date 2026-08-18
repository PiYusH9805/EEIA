from app.agents.documentation.documentation_agent import DocumentationAgent

agent = DocumentationAgent()

question = input("Question: ")

response = agent.ask(question)

print("\n")
print(response)
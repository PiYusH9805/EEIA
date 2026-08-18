from app.agents.code.code_agent import CodeAgent

agent = CodeAgent()

while True:

    question = input("\nQuestion : ")

    if question.lower() == "exit":
        break

    answer = agent.ask(question)

    print("\n")
    print(answer)
from app.graph.workflow import graph

while True:

    q = input("Question : ")

    if q.lower() == "exit":
        break

    result = graph.invoke(

        {

            "question": q,

            "answer": ""

        }

    )

    print(result["answer"])
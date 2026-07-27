import asyncio
from agent.agent import response
def main():
    while True:
        user = str(input("Enter prompt: ")).lower()
        if user == "q":
            break
        print("-"*75)
        modelresponse = asyncio.run(response(user))
        print(modelresponse["messages"][-1].content)
        print("-"*75)
if __name__ == "__main__":
    main()
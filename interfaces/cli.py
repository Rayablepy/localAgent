import asyncio
from agent.agent import response
async def main():
    while True:
        user = str(input("Enter prompt: ")).lower()
        if user == "q":
            break
        print("-"*75)
        modelresponse = await response(user)
        print(modelresponse["messages"][-1].content)
        print("-"*75)
if __name__ == "__main__":
    asyncio.run(main())

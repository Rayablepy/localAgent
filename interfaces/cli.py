import asyncio
from agent.agent import response, list_threads
import uuid

async def menu():
    while True:
        print("""
        Option:
        1. New conversation
        2. List conversations
        3. Quit
        """)
        option = input("Choice: ")
        if option == "1":
            thread_id = str(uuid.uuid4())[:8]
            print(f"New conversation created with id: {thread_id}")
            print("-"*75)
            return thread_id
        elif option == "2":
            temp_choices = {}
            for index, thread_id in enumerate(await list_threads()):
                temp_choices[index] = thread_id
            if not temp_choices:
                print("No conversations found\n"+"-"*75)
                continue
            for key in temp_choices:
                print(f"{key}: {temp_choices[key]}")
            print("-"*75)
            thread_choice = input("Conversation Choice: ").strip()
            try:
                thread_id = temp_choices.get(int(thread_choice))
            except (ValueError, KeyError):
                thread_id = None
            if thread_id:
                return thread_id
            print("Invalid option")
        elif option == "3":
            return None
        else:
            print("Invalid option")

async def main():
    while True:
        user = str(input("Enter prompt: ")).strip().lower()
        if user == "q":
            break
        elif not user:
             continue
        print("-"*75)
        modelresponse = await response(user)
        print(modelresponse["messages"][-1].content)
        print("-"*75)
if __name__ == "__main__":
    asyncio.run(main())

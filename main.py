from handle_dialogue import handle
from bookings_db import initialise_db
from states import user_state
from uuid import uuid4


def main():
    initialise_db() #create database to store flight bookings
    user_state["chat_id"] = str(uuid4()) #each chat has a unique chat id that is used to reference the flight booking for that session
    print("You are now speaking with MP Chatbot. Type 'stop' to quit.")

    while True:
        user_input = input("You: ")
        
        if user_input.lower().strip() == "stop":
            print("MP: Goodbye!")
            break

        reply = handle(user_input)

        if reply is not None:
            print("MP: ", reply)
        
if __name__ == "__main__":
    main()
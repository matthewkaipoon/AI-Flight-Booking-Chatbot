from states import user_state
import random

def greet():
    return choose(["Hi! What is your name?", "Hi there! What's your name?", "Hello. What is your name?"])

def how_are_you():
    return choose(["Thank you for asking! I'm doing well.", "I'm doing well. Thanks for asking.", "I'm good thanks. How can I help you today?"])

def discoverability():
    return choose(["I can help you with booking a flight. I can also answer any question you may have, too.", 
                  "I can book flights for you and answer any general questions you may have.", 
                  "I'm here to help you book flights and to answer questions you may have."])

def ask_name():
    if user_state["name"]:
        return choose([f"{user_state['name']}! Of course I remember your name.",
                      f"You said your name was {user_state['name']}.",
                      f"I remember. Your name is {user_state['name']}."])
    return choose(["I'm sorry but I don't know your name yet. Could you tell me what it is?",
                  "I don't think I know your name yet. What should I call you?", 
                  "You haven't told me your name yet. What is it?"])

def thanks():
    return choose([f"You're welcome {user_state['name']}! Is there anything else I can help you with?", 
                  f"No problem, {user_state['name']}. Would you like help with anything else?",
                  f"No worries {user_state['name']}. Is there anything else you need help with?"])

def closing():
    return choose(["Okay. To end this chat, please type 'stop'.",
                  "Alright. If you’d like to finish, just type 'stop'.",
                  "Got it. When you’re ready to end the chat, type 'stop'."])



def choose(ops):
    return random.choice(ops)
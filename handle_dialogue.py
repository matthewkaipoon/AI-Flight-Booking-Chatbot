import nltk

from states import user_state
from intent_matching import detect_intent
from flight_booking import handle_booking, start_flight_booking
from smalltalk import greet, how_are_you, discoverability, ask_name, thanks, closing
from qa import get_answer
from query_bookings import booking

def fallback(user_query: str): #called if unable to match to any intent
    ans, score = get_answer(user_query)
    return f"{ans}"

#tokenise user input
def process(user_query):
    tokens = nltk.word_tokenize(user_query)
    return tokens

#main dialogue handler
def handle(user_input: str):
    processed_input = process(user_input)

    #next token is user's name
    if user_state["greeted"] and not user_state["name"]:
        tokens = [t for t in processed_input if t.isalpha()]
        if len(tokens) == 1:
            user_state["name"] = tokens[0].capitalize()
            return f"Nice to meet you, {user_state['name']}"
        
    #handles yes/no continuation
    if user_state.get("pending_followup"):
        lower = user_input.lower().strip()

        yes = ["yes", "yeah", "yep", "sure", "please", "ok", "okay", "yes please"]
        no = ["no", "nope", "nah", "no thanks", "nothing", "nothing else",
              "that is all", "thats all", "that's all", "im good", "i'm good", "no thank you"]
        
        if lower in yes:
            user_state["pending_followup"] = False
            return "Okay. What else can I help you with?"
        if lower in no:
            user_state["pending_followup"] = False
            return closing()
        user_state["pending_followup"] = False

    
    if user_state["booking_active"]:
        return handle_booking(user_input)

    #using ML classifier
    intent, score = detect_intent(user_input)

    #map intent to function
    if intent == "greet":
        user_state["greeted"] = True
        return greet()
    elif intent == "how_are_you":
        return how_are_you()
    elif intent == "discoverability":
        return discoverability()
    elif intent == "ask_name":
        return ask_name()
    elif intent == "start_flight_booking":
        return start_flight_booking()
    elif intent == "thank":
        user_state["pending_followup"] = True
        return thanks()
    elif intent == "closing":
        user_state["awaiting_followup"] = False
        return closing()
    elif intent == "query_booking":
        return booking(user_state["chat_id"])
    else:
        return fallback(user_input) # fallback into qa
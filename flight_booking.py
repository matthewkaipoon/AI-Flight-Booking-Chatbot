from states import user_state
from flights import search_flights, flight_exists
from utilities.date_norm_util import normalise_date
import re
from bookings_db import save_single_booking, save_return_booking
import random

BOOKING_ORDER = ["origin_city", "destination_city", "trip_type", "departure_date", "return_date"]
outbound_flights = None
return_flights = None

def start_flight_booking():
    user_state["booking_active"] = True
    user_state["pending_single_flight"] = False
    user_state["pending_outbound_flight"] = False
    user_state["pending_return_flight"] = False
    user_state["selected_outbound_id"] = None

    for i in user_state["booking_slots"]:
        user_state["booking_slots"][i] = None
    return "Great! I can help with that. Firstly, where are you flying from?"

def update_slot(slot, user_input):
    user_state["booking_slots"][slot] = user_input.strip()

def get_next_sequence_slot():
    slots = user_state["booking_slots"]
    for slot in BOOKING_ORDER:
        if slot == "return_date" and slots.get("trip_type") == "single":
            continue
        if slots.get(slot) is None:
            return slot
    return None #all filled

def ask_slot(slot):
    if slot == "origin_city":
        return "Which city are you flying from?"
    if slot == "destination_city":
        return "Thanks. And which city are you flying to?"
    if slot == "trip_type":
        return "Now, is this a single (one way) flight or a return flight?"
    if slot == "departure_date":
        return "And on what date would you like to depart?"
    if slot == "return_date":
        return "Finally, on what date would you like to return?"
    return "Could you provide more details for your flight?"
    


def handle_booking(user_input: str):

    input = user_input.strip()

    if user_state["pending_single_flight"]:
        return handle_single_flight(input)
    if user_state["pending_outbound_flight"]:
        return handle_outbound_flight(input)
    if user_state["pending_return_flight"]:
        return handle_return_flight(input)

    slot = get_next_sequence_slot()
    slots = user_state["booking_slots"]

    if slot is None:
        return complete_booking()
    
    if not input:
        return ask_slot(slot)
    
    if slot == "trip_type":
        lower = input.lower()
        if "return" in lower or "round" in lower:
            update_slot("trip_type", "return")
        elif "single" in lower or "one way" in lower:
            update_slot("trip_type", "single")
        else:
            return "Is that a single (one way) or a return flight?"
    elif slot in ("departure_date", "return_date"):
        norm = normalise_date(input)
        if norm is None:
            return "Sorry, I don't understand that date. Try 'DD/MM/YYYY'."
        update_slot(slot, norm)
    else:
        update_slot(slot, input)

    if slots.get("origin_city") and slots.get("destination_city") and slot in ("origin_city", "destination_city"):
        if not flight_exists(slots["origin_city"], slots["destination_city"]):
            false_origin = slots["origin_city"]
            false_dest = slots["destination_city"]

            slots["origin_city"] = None
            slots["destination_city"] = None

            return f"Sorry, I couldn't find any flights from {false_origin} to {false_dest}. Please choose a different origin city."

    next_slot = get_next_sequence_slot()
    if next_slot is None:
        return complete_booking()
    else:
        return ask_slot(next_slot)

def complete_booking():
    global outbound_flights, return_flights

    slots = user_state["booking_slots"]
    trip_type = slots.get("trip_type", "single")

    if trip_type == "single":
        matches = search_flights(slots)
        if matches.empty:
            slots["departure_date"] = None
            return "I couldn't find any flights on that departure date. Please choose a different date."
        
        outbound_flights = matches
        user_state["pending_single_flight"] = True

        origin = slots["origin_city"].title()
        dest = slots["destination_city"].title()
        dep_date = slots["departure_date"]
        count = len(matches)

        flight_word = plural("flight", count)

        intro = choose([f"I found {count} flights from {origin} to {dest} on {dep_date}:",
                       f"There {'is' if count == 1 else 'are'} {count} {flight_word} from {origin} to {dest} on {dep_date}:",
                       f"On {dep_date}, there {'is' if count == 1 else 'are'} {count} {flight_word} from {origin} to {dest}:",])

        lines = []
        lines.append(intro + "\n")
        lines.append(format_flight_list(matches))
        lines.append("\n\nWhich flight ID would you like to book? (FLXXX).")

        return "\n".join(lines)
    
    elif trip_type == "return":
        outbound_slots = {
            "origin_city": slots["origin_city"],
            "destination_city": slots["destination_city"],
            "departure_date": slots["departure_date"],}
        outbound_matches = search_flights(outbound_slots)

        if outbound_matches.empty:
            slots["departure_date"] = None
            return "I couldn't find any outbound flights on that date. Please choose a different date."
        
        return_slots = {
            "origin_city": slots["destination_city"],
            "destination_city": slots["origin_city"],
            "departure_date": slots["return_date"],
        }
        return_matches = search_flights(return_slots)

        if return_matches.empty:
            slots["return_date"] = None
            return "I couldn't find any return flights on that date. Please choose a different date."

        outbound_flights = outbound_matches
        return_flights = return_matches
        user_state["pending_outbound_flight"] = True

        origin = slots["origin_city"].title()
        dest = slots["destination_city"].title()
        dep_date = slots["departure_date"]
        ret_date = slots["return_date"]

        out_count = len(outbound_matches)
        ret_count = len(return_matches)

        out_flight_word = plural("flight", out_count)
        ret_flight_word = plural("flight", ret_count)
        
        out_intro = choose([
        f"For your outbound journey from {origin} to {dest} on {dep_date}, I found {out_count} {out_flight_word}:",
        f"For the outbound leg from {origin} to {dest} on {dep_date}, there {'is' if out_count == 1 else 'are'} {out_count} {out_flight_word}:",
        f"Outbound from {origin} to {dest} on {dep_date}, I can offer {out_count} {out_flight_word}:",])

        ret_intro = choose([
        f"For your return journey from {dest} to {origin} on {ret_date}, I found {ret_count} {ret_flight_word}:",
        f"For the return leg from {dest} to {origin} on {ret_date}, there {'is' if ret_count == 1 else 'are'} {ret_count} {ret_flight_word}:",
        f"Returning from {dest} to {origin} on {ret_date}, I can offer {ret_count} {ret_flight_word}:"])

        lines = []
        lines.append(out_intro + "\n")
        lines.append(format_flight_list(outbound_matches))
        lines.append("\n" + ret_intro + "\n")
        lines.append(format_flight_list(return_matches))
        lines.append("\nWhich Flight ID would you like to book for your outbound flight? (FLXXX).")

        return "\n".join(lines)

def get_flight_id(text: str):
    #extract FLXXX from the input
    inp = re.search(r"\bfl\d+\b", text, re.IGNORECASE)
    if inp:
        return inp.group(0).upper()
    return None


def handle_single_flight(text: str):
    global outbound_flights

    flight_id = get_flight_id(text)
    if not flight_id:
        return "Please type the flight ID you would like to book FLXXX"

    #check it exists in last search
    df = outbound_flights
    match = df[df["flight_id"].str.upper() == flight_id]

    if match.empty:
        return "I couldn't find that flight ID in the list above. Please type one of the IDs from the list (FLXXX)."

    row = match.iloc[0]

    chat_id = user_state.get("chat_id", "session")
    save_single_booking(chat_id, user_state["booking_slots"], row)

    #reset booking state
    user_state["booking_active"] = False
    user_state["pending_single_flight"] = False
    for key in user_state["booking_slots"]:
        user_state["booking_slots"][key] = None

    #confirm booking
    return (
        f"Great {user_state['name']}, I have booked flight {row['flight_id']} from "
        f"{row['origin_city']} to {row['destination_city']} on {row['departure_date']} "
        f"at {row['departure_time']} in {row['cabin_class']} class for you, "
        f"at a price of £{row['price']}.")


def handle_outbound_flight(text: str):
    global outbound_flights

    flight_id = get_flight_id(text)
    if not flight_id:
        return "Please type the outbound flight ID you would like to book (FLXXX)."

    out_df = outbound_flights
    out_match = out_df[out_df["flight_id"].str.upper() == flight_id]

    if out_match.empty:
        return "I couldn't find that flight ID in the list above. Please type one of the IDs from the list (FLXXX)."
    
  
    user_state["selected_outbound_id"] = flight_id
    user_state["pending_outbound_flight"] = False
    user_state["pending_return_flight"] = True

    return "Thank you! Please now select the return flight ID you would like to book (FLXXX)."


def handle_return_flight(text: str):
    global return_flights, outbound_flights

    flight_id = get_flight_id(text)
    if not flight_id:
        return "Please type the return flight ID you would like to book (FLXXX)."

    df = return_flights
    match = df[df["flight_id"].str.upper() == flight_id]

    if match.empty:
        return "I couldn't find that flight ID in the list above. Please type one of the IDs from the list (FLXXX)."
    
    #get outbound row for confirmation
    out_df = outbound_flights
    out_match = out_df[out_df["flight_id"].str.upper() == user_state["selected_outbound_id"]]
    out_row = out_match.iloc[0]
    ret_row = match.iloc[0]

    outbound_text = (
    f"outbound flight {out_row['flight_id']} from {out_row['origin_city']} "
    f"to {out_row['destination_city']} on {out_row['departure_date']} "
    f"at {out_row['departure_time']}"
    )

    return_text = (
        f"return flight {ret_row['flight_id']} from {ret_row['origin_city']} "
        f"to {ret_row['destination_city']} on {ret_row['departure_date']} "
        f"at {ret_row['departure_time']}"
    )

    total_price = float(out_row["price"]) + float(ret_row["price"])
    

    chat_id = user_state.get("chat_id", "session")
    save_return_booking(chat_id, user_state["booking_slots"], out_row, ret_row)

    #reset booking state
    user_state["booking_active"] = False
    user_state["pending_return_flight"] = False
    user_state["selected_outbound_id"] = None
    for i in user_state["booking_slots"]:
        user_state["booking_slots"][i] = None

    return (
    f"Great {user_state['name']}, I have booked your {outbound_text} "
    f"and {return_text} in {ret_row['cabin_class']} class for you, "
    f"at a price of £{total_price:.0f}."
    )

def format_flight_list(df):
    lines = []

    for _, row in df.iterrows():
        lines.append(
            f"- {row['flight_id']}: {row['origin_city']} to {row['destination_city']} "
            f"on {row['departure_date']} at {row['departure_time']} "
            f"({row['cabin_class']}, £{row['price']})")
    return "\n".join(lines)


def choose(ops):
    return random.choice(ops)

def plural(string: str, count:int):
    return string if count == 1 else string + "s"
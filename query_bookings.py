from bookings_db import get_latest_booking

def booking(chat_id):
    row = get_latest_booking(chat_id)

    #no bookings made yet
    if row is None:
        return "You have not made any bookings."
    
    (trip_type, origin, destination, depart, ret_date, cabin, out_id, ret_id, price) = row

    #handle single flight response
    if trip_type == "single":
        return f"Here are your flight details:\n Single flight {out_id}: {origin} to {destination} on {depart}.\n You will be flying {cabin} and your flight cost is £{price:.2f}"
    
    #handle return flight response
    return f"Here are your flight details:\n Outbound flight {out_id}: {origin} to {destination} on {depart}.\n Return flight {ret_id}: {destination} to {origin} on {ret_date}\nYou will be flying {cabin} and your total flight cost is £{price:.2f}"
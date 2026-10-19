import sqlite3

PATH = "bookings.db"

connection = sqlite3.connect(PATH)
cursor = connection.cursor()

def initialise_db():
    cursor.execute(''' CREATE TABLE IF NOT EXISTS bookings(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   chat_id TEXT,
                   trip_type TEXT,
                   origin_city TEXT,
                   destination_city TEXT,
                   departure_date TEXT,
                   return_date TEXT,
                   cabin_class TEXT,
                   outbound_flight_id TEXT,
                   return_flight_id TEXT,
                   price REAL
                   )''')
    connection.commit()



def save_single_booking(chat_id, slots, flight_row):
    cursor.execute(''' INSERT INTO bookings(
                   chat_id, trip_type, origin_city, destination_city,
                   departure_date, return_date, cabin_class, outbound_flight_id, return_flight_id, price)
                   VALUES (?,?,?,?,?,?,?,?,?,?)''',(
                       chat_id, "single", flight_row["origin_city"], flight_row["destination_city"], flight_row["departure_date"],
                       None, flight_row["cabin_class"], flight_row["flight_id"], None, float(flight_row["price"]),
                   ))
    connection.commit()

def save_return_booking(chat_id, slots, out_row, ret_row):
    cursor.execute(''' INSERT INTO bookings(
                   chat_id, trip_type, origin_city, destination_city,
                   departure_date, return_date, cabin_class, outbound_flight_id, return_flight_id, price)
                   VALUES (?,?,?,?,?,?,?,?,?,?)''',(
                       chat_id, "return", out_row["origin_city"], out_row["destination_city"], out_row["departure_date"],
                       ret_row["departure_date"], out_row["cabin_class"], out_row["flight_id"], ret_row["flight_id"], float(out_row["price"] + float (ret_row["price"])),
                   ))
    connection.commit()

def get_latest_booking(chat_id):
    cursor.execute('''
        SELECT trip_type, origin_city, destination_city,
               departure_date, return_date, cabin_class,
               outbound_flight_id, return_flight_id, price
        FROM bookings
        WHERE chat_id = ?
        ORDER BY id DESC
        LIMIT 1
    ''', (chat_id,))
    row = cursor.fetchone()
    return row
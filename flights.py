import pandas as pd
from utilities.data_util import load_csv

#load flight dataset
flights_df = load_csv("Flights_Dataset.csv", required_cols=[
    "flight_id", "origin_city", "destination_city",
    "departure_date", "departure_time", "arrival_date",
    "flight_duration", "cabin_class", "price"
])

#retrieves all flights that match the users booking details
def search_flights(booking_slots):
    origin = booking_slots["origin_city"].strip().lower()
    destination = booking_slots["destination_city"].strip().lower()
    dep_date = booking_slots["departure_date"].strip().lower()

    df = flights_df.copy()

    #filtering to return only entries that match user details
    matches = df[
        (df["origin_city"].str.lower() == origin) &
        (df["destination_city"].str.lower() == destination) &
        (df["departure_date"].str.lower() == dep_date)]

    return matches

#checks if a flight exists between any two cities
def flight_exists(origin_city: str, destination_city: str):
    origin = origin_city.lower().strip()
    dest = destination_city.lower().strip()

    flight_df = flights_df.copy()

    matches =flight_df[(flight_df["origin_city"].str.lower() == origin) & (flight_df["destination_city"].str.lower() == dest)]

    return not matches.empty
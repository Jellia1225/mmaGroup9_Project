import sqlite3
from datetime import date
import pandas as pd


import nbformat
from nbclient import NotebookClient

import json
from pathlib import Path

STATE_FILE = Path(__file__).parent / "search_state.json"

# save the searching date into a json for price_model.ipynb
def save_search_date(search_date):
    STATE_FILE.write_text(json.dumps({"search_date": str(search_date)}))

DB_PATH = "potter_airlines.db"


# define a function to search for flights based on user input

# this function is for calculating the final price of flights based on the search date. 

# set default search date as 2027-01-01
default_search_date = pd.Timestamp("2027-01-01").strftime("%Y-%m-%d")

def search_flights():
    origin = input("Please Enter Origin: ")
    destination = input("Please Enter Destination: ")

    # get the simulation search date, if not provided, use 2027-01-01 as the default date
    # this search date will be used in the price_model.ipynb to calculate the final price of flights
    # in real world, this search date would be the current date, but for simulation purposes
    # for simulation purposes, we ask "user" to provide a search date

    search_departure_date = input(
        f"Search Date (YYYY-MM-DD), press Enter for {default_search_date}): "
    ).strip()

    save_search_date(search_departure_date)

    if search_departure_date == "":
        search_departure_date = default_search_date

    # get the maximum price from the user, if not provided, no maximum price filter will be applied
    max_price = input("Maximum Price (optional): ")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Build the SQL query based on user input
    query = """
    SELECT
        flight_id,
        origin,
        destination,
        departure_date
    FROM flights
    WHERE LOWER(origin) = LOWER(?)
        AND LOWER(destination) = LOWER(?)

    """
    params = [origin, destination]

    # if the user provided a departure date, add it to the query
    if search_departure_date.strip():
        query += " AND departure_date >= ?"
        params.append(search_departure_date)


    cursor.execute(query, params)

    flight_results = cursor.fetchall()

    # if there are no matching flights, return an empty list
    if not flight_results:
        print("Sorry, no matching flights found.")
        return []

    # Execute the price model notebook to update the final_price table
    nb = nbformat.read("price_model.ipynb", as_version=4)
    NotebookClient(
        nb,
        timeout=600,
        extra_arguments=["--IPKernelApp.log_level=ERROR"],
        resources={"metadata": {"path": "."}},
    ).execute()
    nbformat.write(nb, "price_model.ipynb")

    pairs = [(row[0], row[3]) for row in flight_results]
    join_params = [v for pair in pairs for v in pair]

    join_cursor = conn.cursor()

    # Join the flights and final_price tables to get the final price for each flight
    join_query = """
    SELECT
        f.flight_id,
        f.origin,
        f.destination,
        f.departure_date,
        p.price
    FROM flights f
    JOIN final_price p ON f.flight_id = p.flight_id
            AND p.departure_date = f.departure_date
    WHERE (f.flight_id, f.departure_date) IN ({})
    """.format(",".join("(?, ?)" for _ in pairs))

    # if the user provided a maximum price, add it to the query
    if max_price.strip():
        query += " AND p.price <= ?"
        params.append(float(max_price))

    join_cursor.execute(join_query, join_params)

    join_results = join_cursor.fetchall()

    conn.close()

    return join_results


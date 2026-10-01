
import subprocess
import pandas as pd
import sys
import sqlite3
from contextlib import closing
from config import DB_PATH
import subprocess
import sys, asyncio
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Run the config.py script to set the path
subprocess.run([sys.executable, "config.py"])

# Check if the database is ready
def db_is_ready():
    if not DB_PATH.exists():
        return False
    with closing(sqlite3.connect(DB_PATH)) as conn:
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
        if not {"flights", "final_price"} <= tables:
            return False
        return conn.execute("SELECT COUNT(*) FROM flights").fetchone()[0] > 0

# If the database is not ready, run the necessary scripts to set it up
if not db_is_ready():
    subprocess.run([sys.executable, "flight_class.py"], check=True)
    subprocess.run([sys.executable, "database.py"], check=True)

# Run the search_flight.py and booking.py scripts 
subprocess.run([sys.executable, "search_flight.py"])
subprocess.run([sys.executable, "booking.py"])

# import the search_flights and book_flight functions from their respective modules
from search_flight import search_flights
from booking import book_flight

# Search for flights and display the results
results = search_flights()

display = pd.DataFrame(
    results,
    columns=["flight_id", "origin", "destination", "departure_date", "price"],
)
display["price"] = display["price"].map("${:,.2f}".format)

# if there are results, display them and prompt the user to select a flight 
        # and departure date for booking
if results:
    print(display)

    # Prompt the user to select a flight and departure date for booking
    flight_id = input(
        "Enter the Flight ID to book (or press Enter to cancel): "
    ).strip().upper()

    # If the user choose to stop, print a message and exit the booking process
    if not flight_id:
        print("Booking Process Interrupted. No flight booked.")
    else:
        departure_date = input(
            "Enter the Departure Date (YYYY-MM-DD) (or press Enter to cancel): "
        ).strip()

        if not departure_date:
            print("Booking Process Interrupted. No flight booked.")
        else:
            book_flight(flight_id, departure_date)





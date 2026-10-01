
import subprocess
import sys
import sqlite3
from contextlib import closing
from config import DB_PATH
import subprocess
import sys, asyncio
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


subprocess.run([sys.executable, "config.py"])

def db_is_ready():
    if not DB_PATH.exists():
        return False
    with closing(sqlite3.connect(DB_PATH)) as conn:
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
        if not {"flights", "final_price"} <= tables:
            return False
        return conn.execute("SELECT COUNT(*) FROM flights").fetchone()[0] > 0

if not db_is_ready():
    subprocess.run([sys.executable, "flight_class.py"], check=True)
    subprocess.run([sys.executable, "database.py"], check=True)

subprocess.run([sys.executable, "search_flight.py"])
subprocess.run([sys.executable, "booking.py"])

# subprocess.run([sys.executable, "price_model.ipynb"])

from search_flight import search_flights
from booking import book_flight

results = search_flights()

if results:
    for flight in results:
        print(flight)

    flight_id = input(
        "Enter the Flight ID to book (or press Enter to cancel): "
    ).strip().upper()

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





import sqlite3

from config import DB_PATH
from validation import validate_booking




def book_flight(flight_id, departure_date):
    # Handle non-integer user input before opening the database.
    try:
        ticket_number = int(
            input("How many tickets would you like to book? ")
        )
    except ValueError:
        print("Booking error: Enter a whole number of tickets.")
        return

    conn = sqlite3.connect(DB_PATH)

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT seats_remaining
            FROM flights
            WHERE flight_id = ?
              AND departure_date = ?
        """, (flight_id, departure_date))

        result = cursor.fetchone()

        # Handle an unknown flight or a mismatched departure date.
        if result is None:
            print(
                "Booking error: Flight ID and departure date "
                "do not match an existing flight."
            )
            return

        seats_remaining = result[0]

        # Validate before changing the number of available seats.
        try:
            validate_booking(ticket_number, seats_remaining)
        except AssertionError as error:
            print(f"Booking error: {error}")
            return

        cursor.execute("""
            UPDATE flights
            SET seats_remaining = seats_remaining - ?
            WHERE flight_id = ?
              AND departure_date = ?
              AND seats_remaining >= ?
        """, (
            ticket_number,
            flight_id,
            departure_date,
            ticket_number
        ))

        if cursor.rowcount != 1:
            print("Booking error: Not enough seats available.")
            return

        conn.commit()
        print("Booking successful!")

    finally:
        # Close the connection on success, rejection, or error.
        conn.close()
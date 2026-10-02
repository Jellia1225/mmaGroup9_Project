import sqlite3
import csv
from pathlib import Path
import pandas as pd

from flight_class import Flight

from config import BASE_DIR, DB_PATH, INPUT_CSV, CSV_PATH



def get_connection():
    return sqlite3.connect(DB_PATH)

def create_database():
    # connection to the database
    conn = get_connection()
    cursor = conn.cursor()

    # create flights table
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS flights ( 
            flight_id TEXT NOT NULL, 
            origin TEXT NOT NULL, 
            destination TEXT NOT NULL, 
            departure_date TEXT NOT NULL, 
            base_fare REAL NOT NULL,
            seats_remaining INTEGER NOT NULL, 
            capacity INTEGER NOT NULL, 
            route_demand REAL NOT NULL, 
            season TEXT NOT NULL, 
            is_weekend BOOLEAN NOT NULL,
            PRIMARY KEY (flight_id, departure_date)
            ) 
        """) 

    # save changes
    conn.commit()

    # close database connection
    conn.close()


# Read the original CSV
df = pd.read_csv(INPUT_CSV)

# Drop every row that has at least one NA cell
df = df.dropna()

# reset the row index after dropping
df = df.reset_index(drop=True)

# Standardize date format to YYYY-MM-DD
df["departure_date"] = pd.to_datetime(
    df["departure_date"]
).dt.strftime("%Y-%m-%d")

# Standardize True / False values
df["is_weekend"] = (
    df["is_weekend"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map({"true": True, "false": False})
)

# Save the standardized CSV
df.to_csv(CSV_PATH, index=False)
print("CSV standardized and saved as flights_formatted.csv")


def insert_filghts_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # delete existing data
    cursor.execute("DELETE FROM flights")

    with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):

            # csv -> Flight object
            flight = Flight(
                            flight_id=row["flight_id"],
                            origin=row["origin"],
                            destination=row["destination"],
                            departure_date=row["departure_date"],
                            base_fare=row["base_fare"],
                            seats_remaining=row["seats_remaining"],
                            capacity=row["capacity"],
                            route_demand=row["route_demand"],
                            season=row["season"],
                            is_weekend=row["is_weekend"] == "True",
                        )

            # Flight object -> database row

            cursor.execute("""
                INSERT OR REPLACE INTO flights (
                    flight_id,
                    origin,
                    destination,
                    departure_date,
                    base_fare,
                    seats_remaining,
                    capacity,
                    route_demand,
                    season,
                    is_weekend
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                flight.flight_id,
                flight.origin,
                flight.destination,
                flight.departure_date,
                flight.base_fare,
                flight.seats_remaining,
                flight.capacity,
                flight.route_demand,
                flight.season,
                flight.is_weekend,
                        
            ))        

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    insert_filghts_data()
    print("Flight data inserted successfully.")

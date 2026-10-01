import sqlite3
import csv
from pathlib import Path
import pandas as pd

from config import BASE_DIR
from config import DB_PATH
from config import INPUT_CSV



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
df.to_csv("flights_formatted.csv", index=False)

print("CSV standardized and saved as flights_formatted.csv")

CSV_PATH = BASE_DIR / "flights_formatted.csv"

def insert_filghts_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(CSV_PATH, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        # delete existing data
        cursor.execute("DELETE FROM flights")

        for row in reader:
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
                row["flight_id"],
                row["origin"],
                row["destination"],
                row["departure_date"],
                float(row["base_fare"]),
                int(row["seats_remaining"]),
                int(row["capacity"]),
                float(row["route_demand"]),
                row["season"],
                row["is_weekend"]
            ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    insert_filghts_data()
    print("Flight data inserted successfully.")

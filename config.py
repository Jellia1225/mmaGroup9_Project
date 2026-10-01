from pathlib import Path

# get the folder path
BASE_DIR = Path(__file__).resolve().parent

# Database will be created inside the project folder
DB_PATH = BASE_DIR / "potter_airlines.db"

# get the dataset csv file path
INPUT_CSV = BASE_DIR / "flights.csv"


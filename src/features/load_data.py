"""
This file is for loading the dataset
"""

import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

movie_file_path = os.getenv("MOVIE_DATA_FILE_PATH")

def load_movies(path=movie_file_path) -> pd.DataFrame:
    return pd.read_csv(path)

if __name__ == "__main__":
    print("Loading data...")
    df = load_movies()
    print(df.head())
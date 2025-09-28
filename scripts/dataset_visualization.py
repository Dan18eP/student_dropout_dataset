from pathlib import Path
import pandas as pd
import numpy as np

# Path to dataset
DATASET_PATH = Path(__file__).resolve().parent.parent / "data" / "dataset_dropout.csv"

def analyze_dataset(path=DATASET_PATH):
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print(f"Error reading dataset: {e}")
        return

    print("\n=== HEAD ===")
    print(df.head())

    print("\n=== INFO ===")
    df.info()

    print("\n=== DESCRIBE (numeric) ===")
    print(df.describe(include=[np.number]))

    print("\n=== DESCRIBE (categorical) ===")
    try:
        print(df.describe(include=[object]))
    except:
        print("No categorical columns.")

    print("\n=== MISSING VALUES ===")
    print(df.isnull().sum())

    if "dropout" in df.columns:
        print("\n=== TARGET: dropout ===")
        print(df["dropout"].value_counts(dropna=False))
        rate = df["dropout"].mean() * 100
        print(f"Dropout rate: {rate:.2f}%")

# Run on import
analyze_dataset()
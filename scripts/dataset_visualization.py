from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    
    #Correlation matrix  when dropout== 1        
    print("\n=== CORRELATION MATRIX ===")
    print(df.corr(numeric_only=True)['dropout'])
    
    #Histograms
    print("\n=== HISTOGRAMS ===")
    df.hist(bins=20, figsize=(12, 8))
    plt.tight_layout()
    plt.show()
    
    


# Run on import
analyze_dataset()
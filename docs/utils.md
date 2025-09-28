# Functions Documentation

This document describes the functions and configurations used to generate a **synthetic dataset** for student dropout prediction.  
The dataset is tailored to a context where most students come from nearby cities and attend the *Universidad de la Costa*.

---

## **1. Overview**

The script generates a dataset with **500** student records containing demographic, academic, and financial information.  
The data includes null values to simulate real-world inconsistencies.

The final dataset is saved as a CSV file in the `/data/` directory.

---

## **2. Libraries Used**

The following libraries are required:

- **NumPy** (`numpy`): Used for numerical operations and random value generation
- **Pandas** (`pandas`): Used for creating and handling the dataset in DataFrame format
- **Random** (`random`): Provides additional randomization tools
- **OS** (`os`): Helps in managing file paths for saving the dataset

```python
import numpy as np
import pandas as pd
import random
import os
```

---

## **3. Configuration**

The configuration section defines global parameters and paths used throughout the dataset generation script.

```python
# Number of records to generate
NUM_RECORDS = 500  # Minimum number of rows required

# Output file path
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "dataset_dropout.csv")

# Ensure reproducibility
np.random.seed(42)
```

### Explanation of Variables

- `NUM_RECORDS`: Sets the number of synthetic student records to generate. Default value is 500.
- `OUTPUT_PATH`: Specifies the path where the generated dataset will be saved as a CSV file inside the `/data/` folder.
- `np.random.seed(42)`: Ensures that the random number generator produces the same output each time the script runs, making the dataset generation reproducible.

---

## **4. Helper Functions**

### 4.1 `introduce_nulls()`

This function introduces null values in specified columns with different random percentages for each column.

```python
def introduce_nulls(df, columns, null_percentage=None)
```

#### Parameters:
- `df`: pandas DataFrame to modify
- `columns`: List of column names where nulls will be introduced
- `null_percentage`: Percentage of nulls to introduce (if None, randomly generates between 5-15% for each column)

#### Returns:
- Modified DataFrame with null values introduced

#### Example:
```python
# Introduce random nulls in specific columns
df = introduce_nulls(df, ['gender', 'origin', 'high_school_gpa'])
```

### 4.2 `introduce_outliers()`

This function introduces outliers in numerical columns based on statistical distribution measures.

```python
def introduce_outliers(df, n_std=3, contamination_rate=0.05)
```

#### Parameters:
- `df`: pandas DataFrame to modify
- `n_std`: Number of standard deviations to consider for outlier bounds (default=3)
- `contamination_rate`: Percentage of outliers to introduce (0-1, default=0.05)

#### Affected Columns:
- `age`: Introduces age outliers while maintaining realistic values
- `high_school_gpa`: Introduces GPA outliers within 0-5 range
- `admission_exam_score`: Introduces score outliers within 0-100 range

#### Statistical Method:
1. Calculates median, Q1, Q3, and IQR for each column
2. Defines outlier bounds using IQR method
3. Generates outliers specific to each column's constraints:
   - Age: Integer values outside normal range
   - GPA: Float values between 0-5
   - Admission Score: Integer values between 0-100

#### Returns:
- Modified DataFrame with outliers introduced in numerical columns

#### Example:
```python
# Introduce 5% outliers in numerical columns
df = introduce_outliers(df, n_std=3, contamination_rate=0.05)
```



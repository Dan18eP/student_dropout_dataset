# Functions Documentation - utils.py

This document describes the functions and configurations used to generate a **synthetic dataset** for student dropout prediction.  
The dataset is tailored to a context where most students come from nearby cities and attend the *Universidad de la Costa*.

---

## **1. Overview**

**Authors**: Daniel Echeverría, Andrés Negrete  
**University**: Universidad de la Costa  
**Date**: 2025-09-28

The script generates a dataset with **500** student records containing demographic, academic, and financial information.  
The data includes null values and outliers to simulate real-world inconsistencies and create realistic scenarios.

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
- `OUTPUT_PATH`: Specifies the path where the generated dataset will be saved as a CSV file inside the `/data/` folder, located two directories up from the current script.
- `np.random.seed(42)`: Ensures that the random number generator produces the same output each time the script runs, making the dataset generation reproducible.

---

## **4. Helper Functions**

### 4.1 `introduce_nulls(df, columns, null_percentage=None)`

This function introduces null values in specified columns with different random percentages for each column to simulate realistic missing data patterns.

#### Parameters:
- `df` (pandas.DataFrame): DataFrame to modify
- `columns` (list): List of column names where nulls will be introduced
- `null_percentage` (float, optional): Specific percentage of nulls to introduce. If `None`, randomly generates between 5-15% for each column

#### Functionality:
1. Calculates total number of rows in the DataFrame
2. For each specified column:
   - Determines null percentage (random 5-15% if not specified)
   - Calculates number of null values to introduce
   - Randomly selects indices for null placement
   - Sets selected cells to `np.nan`

#### Returns:
- Modified DataFrame with null values introduced

#### Example:
```python
# Introduce random nulls (5-15%) in specific columns
df = introduce_nulls(df, ['gender', 'origin', 'high_school_gpa'])

# Introduce specific percentage of nulls
df = introduce_nulls(df, ['financial_aid'], null_percentage=0.10)
```

---

### 4.2 `introduce_outliers(df, n_std=3, contamination_rate=0.05)`

This function introduces realistic outliers in numerical columns based on statistical distribution measures, creating extreme but plausible values.

#### Parameters:
- `df` (pandas.DataFrame): DataFrame to modify
- `n_std` (int): Number of standard deviations to consider for outlier bounds (default=3)
- `contamination_rate` (float): Percentage of outliers to introduce (0-1, default=0.05 or 5%)

#### Affected Columns:
The function specifically handles these numerical columns:
- `age`: Student age values
- `high_school_gpa`: High school Grade Point Average
- `admission_exam_score`: University admission exam scores
- `first_semester_gpa`: First semester Grade Point Average

#### Statistical Method:
1. **Statistical Analysis**: Calculates median, Q1 (25th percentile), Q3 (75th percentile), and IQR for each column
2. **Outlier Bounds**: Defines bounds using `Q1 - (n_std * IQR)` and `Q3 + (n_std * IQR)`
3. **Column-Specific Outlier Generation**:

#### Age Outliers:
- **Young outliers**: Ages 14-15 years (30% of outliers)
- **Older outliers**: Ages 30-50 years (70% of outliers)
- **Data type**: Integer values
- **Shuffling**: Applied to avoid clustering patterns

#### GPA Outliers (high_school_gpa, first_semester_gpa):
- **Low outliers**: Values between 0.5 and (Q1 - 0.5), minimum 0.0
- **High outliers**: Values between (Q3 + 0.5) and 5.0, maximum 5.0
- **Data type**: Float values rounded to 2 decimal places
- **Distribution**: 50% low outliers, 50% high outliers
- **Shuffling**: Applied to avoid clustering patterns

#### Admission Exam Score Outliers:
- **Low outliers**: Values between 50 and (Q1 - 5)
- **High outliers**: Values between (Q3 + 5) and 99
- **Data type**: Integer values
- **Distribution**: 50% low outliers, 50% high outliers (adjusts if insufficient low values)
- **Constraints**: Maintains realistic exam score range (50-100)
- **Shuffling**: Applied to avoid clustering patterns

#### Error Handling:
- Skips columns that are entirely NaN
- Handles cases where outlier ranges are insufficient
- Adjusts outlier distribution when constraints limit available values

#### Returns:
- Modified DataFrame with outliers introduced in specified numerical columns

#### Example:
```python
# Introduce 5% outliers using 3 standard deviations
df = introduce_outliers(df, n_std=3, contamination_rate=0.05)

# Introduce 10% outliers using 2 standard deviations
df = introduce_outliers(df, n_std=2, contamination_rate=0.10)
```

---

## **5. Key Features**

### Realistic Data Simulation
- **Missing Data**: Random null percentages (5-15%) per column simulate real-world data collection issues
- **Outliers**: Statistically-based outliers maintain data realism while introducing edge cases
- **Reproducibility**: Fixed random seed ensures consistent dataset generation across runs

### Data Quality Considerations
- **Age Constraints**: Outliers remain within realistic university student age ranges
- **GPA Bounds**: All GPA values stay within valid 0.0-5.0 scale
- **Score Limits**: Admission scores maintain realistic 50-100 range
- **Distribution Balance**: Even distribution of outliers prevents skewed patterns

### Technical Implementation
- **Memory Efficiency**: Uses appropriate data types (int32, float32) for optimization
- **Random Distribution**: Shuffling prevents clustering of outliers
- **Error Resilience**: Handles edge cases and missing data gracefully
# Script to generate a synthetic dataset for predicting future student dropout.
# Authors: Daniel Echeverría, Andrés Negrete
# University: Universidad de la Costa
# Date: 2025-09-28

#Import necessary libraries
import numpy as np
import pandas as pd
import random
import os

#Configuration
NUM_RECORDS = 500  # Minimum number of rows required
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "dataset_dropout.csv")

#Ensure reproducibility
np.random.seed(42)

def introduce_nulls(df, columns, null_percentage=None):
    """
    Introduce null values in specified columns with different random percentages for each column.
    
    Args:
        df: DataFrame to modify
        columns: List of columns where to introduce nulls
        null_percentage: Percentage of nulls (if None, randomly generated per column)
    """
    total_rows = len(df)
    for column in columns:
        #Generate different random percentage for each column
        column_null_percentage = null_percentage if null_percentage is not None else random.uniform(0.05, 0.15)
        
        num_nulls = int(total_rows * column_null_percentage)
        null_indices = np.random.choice(df.index, num_nulls, replace=False)
        df.loc[null_indices, column] = np.nan
    return df

def introduce_outliers(df, n_std=3, contamination_rate=0.05):
    """
    Introduce outliers in numerical columns based on data distribution.
    
    Args:
        df: DataFrame to modify
        n_std: Number of standard deviations to consider for outliers
        contamination_rate: Percentage of outliers to introduce (0-1)
    """
    num_outliers = int(len(df) * contamination_rate)
    
    for column in ['age', 'high_school_gpa', 'admission_exam_score', 'first_semester_gpa']:
        #Skip if column is all NaN
        if df[column].isna().all():
            continue
            
        #Calculate statistical measures
        median = df[column].median()
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        
        #Define outlier bounds
        lower_bound = q1 - (n_std * iqr)
        upper_bound = q3 + (n_std * iqr)
        
        #Generate outliers
        if column == 'age':
            #Generate outliers for both very young and older students
            young_outliers = list(range(14, 16))  #Outliers between 14 and 15 years
            older_outliers = list(range(30, 51))  #Outliers between 30 and 50 years
            all_outliers = young_outliers + older_outliers
            
            #Split outliers: 30% young, 70% older
            young_count = int(num_outliers * 0.3)
            older_count = num_outliers - young_count
            
            outliers = np.array(
                np.random.choice(young_outliers, size=young_count).tolist() +
                np.random.choice(older_outliers, size=older_count).tolist(),
                dtype=np.int32
            )
            #Shuffle outliers to avoid clustering
            np.random.shuffle(outliers)
        elif column in ['high_school_gpa', 'first_semester_gpa']:
            # For GPAs, keep values between 0.0 and 5.0
            low_outliers = np.round(np.random.uniform(
                low=max(0, 0.5),
                high=max(0, q1-0.5),
                size=num_outliers // 2
            ), 2)  #Round to 2 decimal places
            
            high_outliers = np.round(np.random.uniform(
                low=min(q3+0.5, 4.5),
                high=5.0,
                size=num_outliers - num_outliers // 2
            ), 2)  #Redondear a 2 decimales
            
            outliers = np.concatenate([low_outliers, high_outliers])
            outliers = np.array(outliers, dtype=np.float32)
            #Shuffle outliers to avoid clustering
            np.random.shuffle(outliers)
        else:  #admission_exam_score   
            #Ensure outliers are between 50 and 100
            #For low outliers, use range between 50 and q1-5
            low_outliers = list(range(50, max(51, int(q1-5))))
            #For high outliers, use values close to 100
            high_outliers = list(range(min(int(q3+5), 95), 100))
            
            #If there aren't enough values in the low range, use more from the high range
            if len(low_outliers) == 0:
                low_count = 0
                high_count = num_outliers
            else:
                low_count = num_outliers // 2
                high_count = num_outliers - low_count
            
            outliers = np.array(
                np.random.choice(low_outliers, size=low_count).tolist() +
                np.random.choice(high_outliers, size=high_count).tolist(),
                dtype=np.int32
            )
            #Shuffle outliers to avoid clustering
            np.random.shuffle(outliers)
            
        #Insert outliers
        df.loc[random.sample(range(len(df)), num_outliers), column] = outliers
    
    return df


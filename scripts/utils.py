#Script to generate a synthetic dataset for predicting future student dropout.
#Authors: Daniel Echeverría, Andrés Negrete
#University: Universidad de la Costa
#Date: 2025-09-26

#Import necessary libraries
import numpy as np
import pandas as pd
import random
import os

#Configuration
NUM_RECORDS = 500  #Minimum number of rows required
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "dataset_dropout.csv")

#Ensure reproducibility
np.random.seed(42)

#Some Functions
def introduce_nulls(df, columns, null_percentage= random(0.05, 0.15)):
    
    total_rows = len(df)
    for column in columns:
        num_nulls = int(total_rows * null_percentage)
        null_indices = np.random.choice(df.index, num_nulls, replace=False)
        df.loc[null_indices, column] = np.nan
    return df

#Introduce outliers in numerical columns based on data distribution
def introduce_outliers(df, n_std=3, contamination_rate=0.05):
    """
    Args:
        df: DataFrame to modify
        n_std: Number of standard deviations to consider for outliers
        contamination_rate: Percentage of outliers to introduce (0-1)
    """
    num_outliers = int(len(df) * contamination_rate)
    
    for column in ['age', 'high_school_gpa', 'admission_exam_score']:
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
            outliers = np.random.choice(
                list(range(int(lower_bound-5), int(q1-2))) + 
                list(range(int(q3+2), int(upper_bound+5))),
                size=num_outliers
            )
        elif column == 'high_school_gpa':
            outliers = np.random.uniform(
                low=max(0, lower_bound-0.5),
                high=min(5.0, upper_bound+0.5),
                size=num_outliers
            )
        #admission_exam_score   
        else:  
            outliers = np.random.choice(
                list(range(int(lower_bound-10), int(q1-5))) + 
                list(range(int(q3+5), min(100, int(upper_bound+10)))),
                size=num_outliers
            )
            
        #Insert outliers
        df.loc[random.sample(range(len(df)), num_outliers), column] = outliers
    
    return df


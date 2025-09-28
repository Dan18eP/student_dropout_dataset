# NECESSARY IMPORTS
import numpy as np
from utils import NUM_RECORDS, OUTPUT_PATH, introduce_nulls, introduce_outliers
import pandas as pd
import os

def generate_dataset():
    print("\n=== Starting Dataset Generation ===")
    print(f"Generating data for {NUM_RECORDS} students...")
    
    # Demographic data
    age = np.random.randint(16, 30, NUM_RECORDS)
    gender = np.random.choice(['M', 'F', 'Other'], NUM_RECORDS)
    print("\n[1] Generated demographic data (age and gender)")
    
    #Cities with their probabilities
    cities = [
        #Caribbean Coast (60% total probability)
        'Barranquilla',    # 15%
        'Cartagena',       # 12%
        'Santa Marta',     # 8%
        'Soledad',         # 6%
        'Valledupar',      # 5%
        'Sincelejo',       # 4%
        'Riohacha',        # 4%
        'Malambo',         # 2%
        'Puerto Colombia', # 2%
        'Sabanalarga',     # 2%
        #Rest of the country (40% total probability)
        'Bogota',          # 10%
        'Medellin',        # 8%
        'Cali',            # 6%
        'Bucaramanga',     # 4%
        'Cucuta',          # 3%
        'Pereira',         # 2%
        'Ibague',          # 2%
        'Villavicencio',   # 2%
        'Manizales',       # 2%
        'Pasto'            # 1%
    ]

    probabilities = [
        0.15, 0.12, 0.08, 0.06, 0.05, 0.04, 0.04, 0.02, 0.02, 0.02,  #Caribbean Coast (60%)
        0.10, 0.08, 0.06, 0.04, 0.03, 0.02, 0.02, 0.02, 0.02, 0.01   #Rest of country (40%)
    ]

    origin = np.random.choice(cities, NUM_RECORDS, p=probabilities)
    print("[2] Generated origin data with city distribution")

    #Available majors/programs
    programs = [
        'Business Administration',
        'Banking and Finance',
        'International Business',
        'Architecture',
        'Social Communication',
        'Psychology',
        'Public Accounting',
        'Law',
        'Civil Engineering',
        'Computer Engineering',
        'Electronic Engineering',
        'Mechanical Engineering',
        'Industrial Engineering',
        'Environmental Engineering',
        'Medicine',
        'Nursing',
        'Graphic Design',
        'International Trade',
        'Marketing and Advertising',
        'Electrical Engineering'
    ]
    
    #Academic data
    major = np.random.choice(programs, NUM_RECORDS)
    high_school_gpa = np.round(np.random.uniform(2.0, 5.0, NUM_RECORDS), 2)
    admission_exam_score = np.random.randint(50, 100, NUM_RECORDS)
    first_semester_gpa = np.round(np.random.uniform(1.0, 5.0, NUM_RECORDS), 2)
    print("[3] Generated academic data (major, GPAs, admission scores)")

    #Financial data
    socioeconomic_level = np.random.choice([1, 2, 3, 4, 5, 6], NUM_RECORDS)
    scholarship = np.random.choice([0, 1], NUM_RECORDS, p=[0.75, 0.25])  # 25% chance of having a scholarship
    loan = np.random.choice([0, 1], NUM_RECORDS, p=[0.6, 0.4])        # 40% chance of having a loan
    financial_aid = np.random.choice([0, 1], NUM_RECORDS, p=[0.8, 0.2]) # 20% chance of having financial aid
    print("[4] Generated financial data (socioeconomic level, scholarships, loans, aid)")

    #Target variable: dropout

    dropout_probs = []

    for i in range(NUM_RECORDS):
        prob = 0.18  #base probability 18%

        # Academic factors
        if high_school_gpa[i] < 3.0:
            prob += 0.25
        if first_semester_gpa[i] < 3.0:
            prob += 0.35

        # Financial factors
        if socioeconomic_level[i] <= 2:  #Low socioeconomic level
            prob += 0.20
        if scholarship[i] == 1:  #Has scholarship
            prob -= 0.25  #Scholarship helps reduce dropout
        if loan[i] == 1:  #Has educational loan
            prob += 0.15  #Loans can increase dropout risk
        if financial_aid[i] == 1:  #Has additional financial aid
            prob -= 0.15  #Financial aid helps reduce dropout

        # Geographic factors
        if origin[i] not in [ 'Barranquilla',
        'Cartagena',       
        'Santa Marta',     
        'Soledad',         
        'Valledupar',      
        'Sincelejo',       
        'Riohacha',        
        'Malambo',         
        'Puerto Colombia', 
        'Sabanalarga',]:
            prob += 0.05

        # Bound probability between 0 and 1
        prob = min(max(prob, 0), 1)

        dropout_probs.append(prob)

    # Generate dropout based on probabilities
    dropout = np.random.binomial(1, dropout_probs)

    #Combine into a DataFrame
    df = pd.DataFrame({
        'student_id': range(1, NUM_RECORDS + 1),
        'age': age,
        'gender': gender,
        'origin': origin,
        'major': major,
        'high_school_gpa': high_school_gpa,
        'admission_exam_score': admission_exam_score,
        'first_semester_gpa': first_semester_gpa,
        'socioeconomic_level': socioeconomic_level,
        'scholarship': scholarship,
        'loan': loan,
        'financial_aid': financial_aid,
        'dropout': dropout
    })


    #Introduce outliers
    df_before_outliers = df.copy()
    df = introduce_outliers(df)
    
    # Print outlier information
    print("\n=== Outlier Information ===")
    for column in ['age', 'high_school_gpa', 'admission_exam_score', 'first_semester_gpa']:
        outliers = df[column][df[column] != df_before_outliers[column]]
        if not outliers.empty:
            print(f"\nOutliers in {column}:")
            print(f"Original values: {df_before_outliers.loc[outliers.index, column].values}")
            print(f"Modified values: {outliers.values}")
            
    #Round GPA columns
    df['high_school_gpa'] = df['high_school_gpa'].round(2)
    df['first_semester_gpa'] = df['first_semester_gpa'].round(2)
    
    print("\n[5] Introduced outliers in numeric columns")
    
        
    #Introduce nulls
    df = introduce_nulls(df, ['gender', 'origin', 'high_school_gpa', 'first_semester_gpa', 'admission_exam_score'])
    print("\n[6] Introduced null values in selected columns")
    
    #Validate and adjust extreme inconsistencies in dropout values
    def validate_dropout(row):
        #Case 1: Excellent performance and financial support -> unlikely to drop out
        if (
            row['high_school_gpa'] >= 4.0 and
            row['first_semester_gpa'] >= 4.0 and
            row['scholarship'] == 1 and
            row['dropout'] == 1  # Only correct if currently mislabeled
        ):
            return 0  
        
        #Case 2: Very poor performance and no financial support -> high probability of dropout
        if (
            row['high_school_gpa'] < 2.0 and
            row['first_semester_gpa'] < 2.0 and
            row['scholarship'] == 0 and
            row['dropout'] == 0  #Only correct if currently mislabeled
        ):
            return 1  
        
        #For all other cases, keep the original value
        return row['dropout']

    print("\n[7] Validated and adjusted dropout values for extreme inconsistencies")
    
    #Apply the validation function to adjust dropout values
    df['dropout'] = df.apply(validate_dropout, axis=1)

    print("\n[8] Applied dropout validation to the entire dataset")


    
    
    
    #Save to CSV
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Dataset successfully generated and saved to {OUTPUT_PATH}")

#Run script
if __name__ == "__main__":
    generate_dataset()
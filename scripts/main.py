import numpy as np
from utils import NUM_RECORDS, OUTPUT_PATH, introduce_nulls, introduce_outliers

def generate_dataset():
    # Demographic data
    age = np.random.randint(16, 30, NUM_RECORDS)
    gender = np.random.choice(['M', 'F', 'Other'], NUM_RECORDS)
    
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

    #Financial data
    socioeconomic_level = np.random.choice([1, 2, 3, 4, 5, 6], NUM_RECORDS)
    scholarship = np.random.choice([0, 1], NUM_RECORDS, p=[0.7, 0.3])  # 30% chance of having a scholarship
    loan = np.random.choice([0, 1], NUM_RECORDS, p=[0.6, 0.4])        # 40% chance of having a loan
    financial_aid = np.random.choice([0, 1], NUM_RECORDS, p=[0.8, 0.2]) # 20% chance of having financial aid

    #Target variable: dropout

    dropout_probs = []

    for i in range(NUM_RECORDS):
        prob = 0.2  # base probability 20%

        # Academic factors
        if high_school_gpa[i] < 3.0:
            prob += 0.25
        if first_semester_gpa[i] < 3.0:
            prob += 0.35

        # Financial factors
        if socioeconomic_level[i] == 'Low':
            prob += 0.15
        if scholarship[i] == 1:  # Has scholarship
            prob -= 0.10

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
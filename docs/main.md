# Main Script Documentation - main.py

## Overview
The `main.py` script is responsible for generating the synthetic student dataset using utility functions imported from `utils.py`. It creates a comprehensive dataset that simulates realistic patterns and relationships between demographic, academic, financial variables and student dropout behavior.

---

## **Dependencies**

```python
import numpy as np
from utils import NUM_RECORDS, OUTPUT_PATH, introduce_nulls, introduce_outliers
import pandas as pd
import os
```

### Required Imports
- **NumPy**: For numerical operations and random data generation
- **Utils**: Custom module that provides:
  - `NUM_RECORDS`: Number of records to generate (500)
  - `OUTPUT_PATH`: Output file path for CSV storage
  - `introduce_nulls`: Function to introduce null values
  - `introduce_outliers`: Function to introduce outliers
- **Pandas**: For DataFrame creation and manipulation
- **OS**: For directory and file path management

---

## **Main Function: `generate_dataset()`**

### Purpose
Generates a synthetic dataset for student dropout prediction, simulating realistic patterns and relationships between variables with a focus on Colombian university context.

---

## **Data Generation Components**

### **1. Demographic Data**
```python
age = np.random.randint(16, 30, NUM_RECORDS)
gender = np.random.choice(['M', 'F', 'Other'], NUM_RECORDS)
```

- **Age**: Random integers between 16-29 years (typical university age range)
- **Gender**: Random selection from Male ('M'), Female ('F'), and Other categories

### **2. Geographic Data (Origin Cities)**

#### City Distribution Strategy
The script implements a realistic geographic distribution focusing on Colombian Caribbean Coast cities:

**Caribbean Coast Cities (60% total probability)**:
- Barranquilla (15%) - Major coastal city
- Cartagena (12%) - Historical port city
- Santa Marta (8%) - Coastal tourist city
- Soledad (6%) - Metropolitan area
- Valledupar (5%) - Regional capital
- Sincelejo (4%) - Interior city
- Riohacha (4%) - Northern coast
- Malambo (2%) - Small city
- Puerto Colombia (2%) - Port city
- Sabanalarga (2%) - Local city

**Rest of Colombia (40% total probability)**:
- Bogotá (10%) - National capital
- Medellín (8%) - Major urban center
- Cali (6%) - Pacific region
- Bucaramanga (4%) - Eastern region
- Cúcuta (3%) - Border city
- Pereira (2%) - Coffee region
- Ibagué (2%) - Central region
- Villavicencio (2%) - Eastern plains
- Manizales (2%) - Coffee region
- Pasto (1%) - Southern region

```python
origin = np.random.choice(cities, NUM_RECORDS, p=probabilities)
```

### **3. Academic Data**

#### Available Programs (20 majors)
```python
programs = [
    'Business Administration', 'Banking and Finance', 'International Business',
    'Architecture', 'Social Communication', 'Psychology', 'Public Accounting',
    'Law', 'Civil Engineering', 'Computer Engineering', 'Electronic Engineering',
    'Mechanical Engineering', 'Industrial Engineering', 'Environmental Engineering',
    'Medicine', 'Nursing', 'Graphic Design', 'International Trade',
    'Marketing and Advertising', 'Electrical Engineering'
]
```

#### Academic Variables
- **Major**: Random selection from 20 university programs
- **High School GPA**: Uniform distribution 2.0-5.0, rounded to 2 decimals
- **Admission Exam Score**: Integer values 50-99
- **First Semester GPA**: Uniform distribution 1.0-5.0, rounded to 2 decimals

```python
major = np.random.choice(programs, NUM_RECORDS)
high_school_gpa = np.round(np.random.uniform(2.0, 5.0, NUM_RECORDS), 2)
admission_exam_score = np.random.randint(50, 100, NUM_RECORDS)
first_semester_gpa = np.round(np.random.uniform(1.0, 5.0, NUM_RECORDS), 2)
```

### **4. Financial Data**

#### Financial Variables
- **Socioeconomic Level**: Scale 1-6 (1 = lowest, 6 = highest)
- **Scholarship**: Binary (0/1) with 25% probability of having scholarship
- **Loan**: Binary (0/1) with 40% probability of having educational loan
- **Financial Aid**: Binary (0/1) with 20% probability of receiving financial aid

```python
socioeconomic_level = np.random.choice([1, 2, 3, 4, 5, 6], NUM_RECORDS)
scholarship = np.random.choice([0, 1], NUM_RECORDS, p=[0.75, 0.25])
loan = np.random.choice([0, 1], NUM_RECORDS, p=[0.6, 0.4])
financial_aid = np.random.choice([0, 1], NUM_RECORDS, p=[0.8, 0.2])
```

---

## **Dropout Probability Generation**

### **Base Probability**
- Starting probability: **18%** for all students

### **Risk Factors (Increase Dropout Probability)**

#### Academic Risk Factors
- **Low High School GPA** (< 3.0): +25% probability
- **Low First Semester GPA** (< 3.0): +35% probability

#### Financial Risk Factors
- **Low Socioeconomic Level** (≤ 2): +20% probability
- **Educational Loan** (has loan): +15% probability

#### Geographic Risk Factors
- **Non-Caribbean Coast Origin**: +5% probability
  - Students from cities outside the Caribbean coast region

### **Protective Factors (Decrease Dropout Probability)**

#### Financial Support
- **Scholarship** (has scholarship): -25% probability
- **Financial Aid** (has aid): -15% probability

### **Probability Calculation Logic**
```python
for i in range(NUM_RECORDS):
    prob = 0.16  # Base probability 16%

    # Academic factors
    if high_school_gpa[i] < 3.0:
        prob += 0.25
    if first_semester_gpa[i] < 3.0:
        prob += 0.35

    # Financial factors
    if socioeconomic_level[i] <= 2:
        prob += 0.20
    if scholarship[i] == 1:
        prob -= 0.25
    if loan[i] == 1:
        prob += 0.15
    if financial_aid[i] == 1:
        prob -= 0.15

    # Geographic factors
    if origin[i] not in [Caribbean_coast_cities]:
        prob += 0.05

    # Bound probability between 0 and 1
    prob = min(max(prob, 0), 1)
    dropout_probs.append(prob)

# Generate dropout based on probabilities
dropout = np.random.binomial(1, dropout_probs)
```

---

## **DataFrame Creation and Processing**

### **1. DataFrame Structure**
```python
df = pd.DataFrame({
    'student_id': range(1, NUM_RECORDS + 1),      # Unique identifier
    'age': age,                                   # Student age
    'gender': gender,                             # Gender
    'origin': origin,                             # City of origin
    'major': major,                               # Study program
    'high_school_gpa': high_school_gpa,          # High school GPA
    'admission_exam_score': admission_exam_score, # Admission score
    'first_semester_gpa': first_semester_gpa,    # First semester GPA
    'socioeconomic_level': socioeconomic_level,  # Socioeconomic level
    'scholarship': scholarship,                   # Scholarship (0/1)
    'loan': loan,                                # Loan (0/1)
    'financial_aid': financial_aid,              # Financial aid (0/1)
    'dropout': dropout                           # Target variable (0/1)
})
```

### **2. Data Processing Steps**

#### **Step 1: Outliers Introduction**
```python
df_before_outliers = df.copy()
df = introduce_outliers(df)
```

**Outlier Information Display**:
- Shows original vs modified values
- Affects: age, high_school_gpa, admission_exam_score, first_semester_gpa
- Uses statistical methods (IQR-based) for realistic outliers

#### **Step 2: GPA Rounding**
```python
df['high_school_gpa'] = df['high_school_gpa'].round(2)
df['first_semester_gpa'] = df['first_semester_gpa'].round(2)
```

#### **Step 3: Null Values Introduction**
```python
df = introduce_nulls(df, [
    'gender', 
    'origin', 
    'high_school_gpa', 
    'first_semester_gpa', 
    'admission_exam_score'
])
```
- Random null values: 5-15% per column
- Simulates real-world missing data patterns

#### **Step 4: Dropout Validation and Adjustment**

**Validation Function Logic**:
```python
def validate_dropout(row):
    # Case 1: Excellent performance + financial support → unlikely dropout
    if (
        row['high_school_gpa'] >= 4.0 and
        row['first_semester_gpa'] >= 4.0 and
        row['scholarship'] == 1 and
        row['dropout'] == 1
    ):
        return 0  # Correct to non-dropout
    
    # Case 2: Poor performance + no support → high dropout probability
    if (
        row['high_school_gpa'] < 2.0 and
        row['first_semester_gpa'] < 2.0 and
        row['scholarship'] == 0 and
        row['dropout'] == 0
    ):
        return 1  # Correct to dropout
    
    # Keep original value for all other cases
    return row['dropout']
```

**Validation Cases**:
- **Case 1**: Students with excellent GPAs (≥4.0) AND scholarships should rarely drop out
- **Case 2**: Students with poor GPAs (<2.0) AND no financial support should often drop out
- **Default**: Maintains original probabilistic assignment for all other combinations

---

## **Dataset Storage**

### **File Output Process**
```python
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)
print(f"Dataset successfully generated and saved to {OUTPUT_PATH}")
```

- **Directory Creation**: Ensures output directory exists
- **CSV Export**: Saves without pandas index
- **Location**: `data/dataset_dropout.csv`
- **Confirmation**: Console message with file path

---

## **Script Execution**

### **Progress Tracking**
The script provides detailed console output:
```
=== Starting Dataset Generation ===
Generating data for 500 students...

[1] Generated demographic data (age and gender)
[2] Generated origin data with city distribution
[3] Generated academic data (major, GPAs, admission scores)
[4] Generated financial data (socioeconomic level, scholarships, loans, aid)
[5] Introduced outliers in numeric columns
[6] Introduced null values in selected columns
[7] Validated and adjusted dropout values for extreme inconsistencies
[8] Applied dropout validation to the entire dataset
```

### **Usage Methods**

#### **Direct Execution**
```bash
python main.py
```

#### **As Module**
```python
from main import generate_dataset
generate_dataset()
```

---

## **Key Features**

### **Realistic Simulation**
- **Geographic Focus**: Caribbean Coast bias reflects Universidad de la Costa context
- **Academic Progression**: Logical relationship between high school and university performance
- **Financial Impact**: Multiple financial factors affecting dropout probability
- **Data Quality Issues**: Realistic missing data and outliers

### **Statistical Rigor**
- **Probability-Based Target**: Dropout generation uses evidence-based risk factors
- **Validation Logic**: Corrects extreme inconsistencies while preserving realistic variability
- **Balanced Distribution**: Maintains realistic dropout rates across different student profiles

### **Technical Implementation**
- **Reproducibility**: Fixed random seed ensures consistent results
- **Error Handling**: Robust file operations and directory management
- **Memory Efficiency**: Appropriate data types and processing methods
# Main Script Documentation

## Overview
The `main.py` script is responsible for generating the synthetic student dataset using utility functions imported from `utils.py`.

## Dependencies
- **NumPy**: For numerical operations and random data generation
- **Utils**: Custom module that provides:
  - `NUM_RECORDS`: Number of records to generate
  - `OUTPUT_PATH`: Output file path
  - `introduce_nulls`: Function to introduce null values
  - `introduce_outliers`: Function to introduce outliers

## Main Function: `generate_dataset()`

### Purpose
Generates a synthetic dataset for student dropout prediction, simulating realistic patterns and relationships between variables.

### Data Components
#### 1. Demographic Data
- Age (16-30)
- Gender (M/F/Other)
- Origin (Cities with weighted probabilities)
   ```python
   age = np.random.randint(16, 30, NUM_RECORDS)
   gender = np.random.choice(['M', 'F', 'Other'], NUM_RECORDS)
   ```

#### 2. Academic Data
- Major (20 different programs)
- High School GPA (2.0-5.0)
- Admission Exam Score (50-100)
- First Semester GPA (1.0-5.0)
   ```python
   major = np.random.choice(programs, NUM_RECORDS)
   high_school_gpa = np.round(np.random.uniform(2.0, 5.0, NUM_RECORDS), 2)
   ```

#### 3. Financial Data
- Socioeconomic Level (1-6)
- Scholarship (Binary, 30% probability)
- Loan (Binary, 40% probability)
- Financial Aid (Binary, 20% probability)
   ```python
   socioeconomic_level = np.random.choice([1, 2, 3, 4, 5, 6], NUM_RECORDS)
   scholarship = np.random.choice([0, 1], NUM_RECORDS, p=[0.7, 0.3])
   ```

### DataFrame Creation and Processing

#### 1. DataFrame Structure
```python
df = pd.DataFrame({
    'student_id': range(1, NUM_RECORDS + 1),  # Unique identifier
    'age': age,                               # Student age
    'gender': gender,                         # Gender
    'origin': origin,                         # City of origin
    'major': major,                           # Study program
    'high_school_gpa': high_school_gpa,       # High school GPA
    'admission_exam_score': admission_exam_score, # Admission score
    'first_semester_gpa': first_semester_gpa,    # First semester GPA
    'socioeconomic_level': socioeconomic_level,  # Socioeconomic level
    'scholarship': scholarship,                   # Scholarship (0/1)
    'loan': loan,                                # Loan (0/1)
    'financial_aid': financial_aid,              # Financial aid (0/1)
    'dropout': dropout                           # Target variable (0/1)
})
```

#### 2. Data Processing
1. **Null Values Introduction**
   ```python
   df = introduce_nulls(df, [
       'gender', 
       'origin', 
       'high_school_gpa', 
       'first_semester_gpa'
   ])
   ```
   - Random null values introduction
   - Null percentage: 5-15% per column

2. **Outliers Introduction**
   ```python
   df = introduce_outliers(df)
   ```
   - Affects numerical columns: age, high_school_gpa, admission_exam_score
   - Uses IQR method for realistic outliers

#### 3. Dataset Storage
```python
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)
```
- Creates directory if it doesn't exist
- Saves as CSV without index
- Location: `data/dataset_dropout.csv`

### Script Usage

1. **Direct Execution**
   ```bash
   python scripts/main.py
   ```

2. **As Module**
   ```python
   from scripts.main import generate_dataset
   dataset = generate_dataset()
   ```

### Output
- CSV file with synthetic dataset
- Console confirmation message
- Data structure ready for predictive analysis
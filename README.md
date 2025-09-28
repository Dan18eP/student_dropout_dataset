# STUDENT DROPOUT DATASET

### Python version of the project
Python 3

### create enviroment
python -m venv venv

### activate enviroment linux
source venv/bin/activate

### activate enviroment windows
venv\Scripts\activate.bat

### install requeriments
pip  install -r requirements.txt 

### run Script
python main.py


# Student Dropout Synthetic Dataset

This repository focuses on generating a synthetic dataset that simulates university student dropout cases.  
It includes demographic, academic, and financial variables, along with null values, outliers, and categorical variables to create realistic scenarios.

---

## Project Structure
STUDENT_DROPOUT_DATASET/
│
├── data/                       # Folder to store generated datasets
│   └── dataset_dropout.csv     # Generated synthetic dataset
│
├── docs/                       # Documentation folder
│   ├── main.md                # Main script documentation
│   └── utils.md               # Utils module documentation
│
├── scripts/                    # Python scripts
│   ├── main.py                # Main script to generate the dataset
│   ├── utils.py               # Utility functions
│   └── dataset_visualization.py # Visualization and exploration of data
│
├── .gitignore                 # Files and folders to ignore in Git
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation


---

## Next Steps
1. Generate the synthetic dataset with at least 500 records.  
2. Add null values, outliers, and categorical variables.  
3. Document the process and dataset details in this README.  
4. Upload the final dataset to GitHub for review and collaboration.  

---

## Notes
- Grades will follow the Colombian grading scale (0 to 5).  
- This dataset will later be used to train a Random Forest model for dropout prediction.

---
## Dataset Features

### Demographic Variables
- `student_id`: Unique identifier
- `age`: Student age (16-30)
- `gender`: M/F/Other
- `origin`: City of origin (weighted towards Caribbean Coast)

### Academic Variables
- `major`: Study program (20 different options)
- `high_school_gpa`: High school average (0-5)
- `admission_exam_score`: University admission test score (0-100)
- `first_semester_gpa`: First semester average (0-5)

### Financial Variables
- `socioeconomic_level`: Level 1-6
- `scholarship`: Binary (0/1)
- `loan`: Binary (0/1)
- `financial_aid`: Binary (0/1)

### Target Variable
- `dropout`: Binary (0: No dropout, 1: Dropout)

---

## Data Generation Details
- 500 synthetic records
- Includes null values (5-15% per affected column)
- Contains outliers in numerical variables
- Simulates close-realistic patterns and relationships

---

## Documentation
Detailed documentation for the project modules can be found in:
- `/docs/main.md`: Documentation for main script functionality
- `/docs/utils.md`: Documentation for utility functions and configurations
- `/docs/dataset_visualization.md`: Documentation for statistical summaries, data quality assessment, and visualization components

## Usage
1. Clone the repository
2. Create and activate virtual environment
3. Install requirements
4. Run main script
5. Check generated dataset in `/data` folder

## Dependencies
Project's specific versions to ensure reproducibility:

- numpy==2.3.3           # Library for numerical computing and arrays
- pandas==2.3.2          # Data manipulation and analysis
- python-dateutil==2.9.0.post0  # Date handling extensions
- pytz==2025.2          # Timezone management
- six==1.17.0           # Python 2 and 3 compatibility
- tzdata==2025.2        # Timezone database
- matplotlib==3.10.6    # Data visualization and plotting
- random                # Built-in module for random number generation
- os                    # Built-in module for OS operations

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Authors
- Daniel Echeverría
- Andrés Negrete


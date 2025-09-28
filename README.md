# STUDENT DROPOUT DATASET

# Python version of the project
Python 3

# create enviroment
python -m venv venv

# activate enviroment linux
source venv/bin/activate

# activate enviroment windows
venv\Scripts\activate.bat


# install requeriments
pip  install -r requirements.txt 

# run Script
python main.py


# Student Dropout Synthetic Dataset

This repository focuses on generating a synthetic dataset that simulates university student dropout cases.  
It includes demographic, academic, and financial variables, along with null values, outliers, and categorical variables to create realistic scenarios.

---

## Project Structure
STUDENT_DROPOUT_DATASET/
│
├── data/ # Folder to store generated datasets
│
├── scripts/ # Python scripts
│ ├── main.py # Main script to generate the dataset
│ ├── utils.py # Utility functions
│ └── dataset_visualization.py # Visualization and exploration of data
│
├── .gitignore # Files and folders to ignore in Git
└── README.md # Project documentation


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


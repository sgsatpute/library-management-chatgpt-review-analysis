# Library Management and ChatGPT Review Analysis

This repository contains a Python final-year project with two parts:

1. A console-based Library Management System.
2. A machine-learning notebook that analyzes ChatGPT Android app reviews.

## Project Contents

- `library_management.py` - Python CLI application for managing books, patrons, borrowing, returns, reviews, overdue checks, and role-based login.
- `final_chatgptreview.ipynb` - Jupyter notebook for ChatGPT review visualization and ML modeling.
- `chatgpt_reviews.csv` - Dataset used by the notebook.
- `lib management and ML IITKGP.docx` and `lib management and ML IITKGP.pdf` - Project report.
- `Project report on Python and ML TEAM NO.4.pptx` - Project presentation.
- `Project_Statement_COEP_Tech_Team_4.pdf` - Original project statement.

## Library Management Features

- Register patrons and admins.
- Login with SHA-256 hashed passwords.
- Add, view, search, and delete books.
- Add, view, and delete patrons.
- Borrow and return books.
- Add book reviews.
- Track due dates and overdue fines.
- Store data in CSV files.

## Machine Learning Work

The notebook analyzes daily ChatGPT Android app reviews using:

- Data loading and inspection with pandas.
- Rating and thumbs-up visualizations with matplotlib and seaborn.
- Text feature extraction using TF-IDF.
- Linear regression for rating prediction.
- Neural network modeling using TensorFlow/Keras.
- Word cloud generation for frequent review terms.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the library management app:

```bash
python library_management.py
```

Open the notebook:

```bash
jupyter notebook final_chatgptreview.ipynb
```

## Notes

The library app creates `books.csv`, `patrons.csv`, and `borrowed_books.csv` at runtime. These generated files are ignored by git.

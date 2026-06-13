# Library Management and ChatGPT Review Analysis

This repository contains a Python final-year project with two parts:

1. A console-based Library Management System.
2. A machine-learning project that analyzes ChatGPT Android app reviews.

The machine-learning part is the main data science component and is explained in detail below for placement and interview preparation.

## Project Contents

- `library_management.py` - Python CLI application for managing books, patrons, borrowing, returns, reviews, overdue checks, and role-based login.
- `final_chatgptreview.ipynb` - Jupyter notebook for ChatGPT review analysis, visualization, feature extraction, and ML modeling.
- `chatgpt_reviews.csv` - Dataset used by the notebook.
- `lib management and ML IITKGP.docx` and `lib management and ML IITKGP.pdf` - Project report.
- `Project report on Python and ML TEAM NO.4.pptx` - Project presentation.
- `Project_Statement_COEP_Tech_Team_4.pdf` - Original project statement.
- `requirements.txt` - Python dependencies required to run the notebook.

## Library Management System

The Library Management System is a Python console application that uses CSV files for data storage.

### Features

- Register patrons and admins.
- Login with SHA-256 hashed passwords.
- Add, view, search, and delete books.
- Add, view, and delete patrons.
- Borrow and return books.
- Add book reviews.
- Track due dates and overdue fines.
- Store books, patrons, and borrowing records in CSV files.

## Machine Learning Project: ChatGPT Android App Review Analysis

### Problem Statement

The goal of this ML project is to analyze user reviews of the ChatGPT Android app and understand how users rate the app based on their written feedback.

The project focuses on:

- Exploring real-world user review data.
- Understanding rating distribution and user engagement.
- Visualizing common review patterns.
- Converting review text into numerical features.
- Training ML models to predict review ratings.
- Comparing model performance using regression metrics.

This project is useful because app reviews contain direct customer feedback. Analyzing this feedback can help product teams understand user satisfaction, identify common issues, and prioritize improvements.

## Dataset

The dataset used is `chatgpt_reviews.csv`, which contains user reviews and ratings for the ChatGPT Android app.

### Dataset Size

- Total rows: `136,224`
- Total columns: `8`

### Columns

| Column | Description |
| --- | --- |
| `reviewId` | Unique ID for each review |
| `userName` | Name of the user who posted the review |
| `content` | Review text written by the user |
| `score` | Rating given by the user, from 1 to 5 |
| `thumbsUpCount` | Number of users who found the review helpful |
| `reviewCreatedVersion` | App version when the review was created |
| `at` | Date and time of the review |
| `appVersion` | App version related to the review |

### Key Dataset Observations

- The average rating is approximately `4.49`.
- The median rating is `5`.
- Most reviews are positive.
- The maximum `thumbsUpCount` is `1193`.
- Most reviews have very few thumbs-up votes.
- The data is imbalanced because 5-star reviews are much more common than low-rated reviews.

## ML Workflow

The complete machine-learning workflow is implemented in `final_chatgptreview.ipynb`.

### 1. Data Loading

The dataset is loaded using pandas:

```python
df = pd.read_csv("chatgpt_reviews.csv")
```

Pandas is used to inspect columns, preview rows, and calculate basic statistics.

### 2. Exploratory Data Analysis

The notebook performs EDA to understand the dataset before modeling.

EDA includes:

- Displaying dataset columns.
- Viewing sample reviews.
- Checking summary statistics.
- Studying the distribution of ratings.
- Studying the distribution of thumbs-up counts.
- Checking correlation between `score` and `thumbsUpCount`.

### 3. Data Visualization

The project uses matplotlib and seaborn for visualization.

Visualizations include:

- Rating distribution chart.
- Thumbs-up count distribution chart.
- Correlation heatmap.
- Actual vs predicted rating scatter plot.
- Residual plot.
- Neural network training and validation loss graph.
- Word cloud of common review words.

These visualizations help explain user behavior and model performance clearly.

### 4. Text Feature Extraction

The `content` column contains review text, which cannot be directly passed into ML models. The notebook converts text into numerical features using TF-IDF.

```python
tfidf = TfidfVectorizer(max_features=1000)
X = tfidf.fit_transform(df["content"].values.astype("U")).toarray()
```

TF-IDF stands for Term Frequency-Inverse Document Frequency. It gives higher importance to words that are meaningful in a review and lower importance to very common words.

In this project:

- Input feature `X`: TF-IDF vector created from review text.
- Target variable `y`: review rating from the `score` column.

### 5. Train-Test Split

The data is split into training and testing sets:

```python
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

- 80% of the data is used for training.
- 20% of the data is used for testing.
- `random_state=42` is used for reproducible results.

### 6. Feature Scaling

The TF-IDF features are standardized using `StandardScaler`.

```python
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
```

Scaling helps models train more consistently, especially neural networks.

## Models Used

### Model 1: Linear Regression

Linear Regression is used to predict the exact rating score from the review text features.

It learns a linear relationship between TF-IDF word features and the rating score.

```python
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)
```

### Model 2: Neural Network

A simple feed-forward neural network is built using TensorFlow/Keras.

Architecture:

| Layer | Details |
| --- | --- |
| Input layer | TF-IDF features |
| Hidden layer 1 | 128 neurons, ReLU activation |
| Hidden layer 2 | 64 neurons, ReLU activation |
| Output layer | 1 neuron for predicted rating |

Model code:

```python
nn_model = Sequential()
nn_model.add(Dense(128, input_dim=X_train.shape[1], activation="relu"))
nn_model.add(Dense(64, activation="relu"))
nn_model.add(Dense(1))
```

The model is compiled using Adam optimizer and Mean Squared Error loss:

```python
nn_model.compile(optimizer="adam", loss="mean_squared_error")
```

## Evaluation Metric

The project uses Mean Squared Error, also called MSE.

```python
mse = mean_squared_error(y_test, y_pred)
```

MSE measures the average squared difference between actual ratings and predicted ratings.

- Lower MSE means better prediction.
- MSE is suitable here because the task is rating prediction, which is treated as a regression problem.

## Results

| Model | MSE | Interpretation |
| --- | ---: | --- |
| Linear Regression | `0.7231` | Best result in the current notebook |
| Neural Network | `0.7609` | Good result, but slightly weaker than Linear Regression |

### Result Interpretation

Linear Regression performed slightly better than the Neural Network because it achieved a lower MSE.

Approximate RMSE values:

| Model | RMSE |
| --- | ---: |
| Linear Regression | `0.85` rating points |
| Neural Network | `0.87` rating points |

This means the models usually predict ratings within about 1 rating point of the actual user rating.

### Final ML Conclusion

The project shows that review text can be used to predict app ratings with reasonable accuracy. The dataset is highly positive, with most users giving 5-star ratings. Because of this imbalance, simple models like Linear Regression can perform competitively.

In the current implementation, Linear Regression gives the best result with an MSE of approximately `0.72`.

## Important Insights

- Most ChatGPT Android app users gave positive ratings.
- Text-based features are useful for predicting ratings.
- TF-IDF is a simple but effective technique for converting review text into ML-ready features.
- Neural networks do not always outperform traditional ML models, especially when the dataset is imbalanced or the features are simple.
- Model evaluation should match the problem type. Since rating prediction is treated as regression, MSE is more appropriate than accuracy.

## Limitations

- The dataset is imbalanced toward 5-star reviews.
- The notebook currently predicts numerical ratings, not sentiment labels.
- More text preprocessing can improve results, such as stopword removal, lemmatization, and emoji handling.
- Advanced models like Random Forest, XGBoost, LSTM, or transformer-based models could be tested.
- The presentation mentions Logistic Regression, but the current notebook mainly implements Linear Regression and Neural Network models.

## Future Improvements

- Add sentiment classification, such as positive, neutral, and negative.
- Add Logistic Regression for classification and compare accuracy, precision, recall, and F1-score.
- Use confusion matrix for classification results.
- Perform better text cleaning and preprocessing.
- Handle class imbalance using sampling techniques.
- Deploy the model as a small web app or API.
- Add model saving using `pickle` or `joblib`.
- Add a dashboard for review trends over time.

## Placement Preparation: How to Explain This Project

### Short Interview Explanation

This project analyzes ChatGPT Android app reviews using Python and machine learning. I used pandas for data analysis, matplotlib and seaborn for visualization, and TF-IDF for converting review text into numerical features. I trained Linear Regression and a Neural Network to predict user ratings from review text. Linear Regression performed slightly better with an MSE of 0.7231, while the Neural Network achieved an MSE of 0.7609. The project helped me understand text preprocessing, feature extraction, regression modeling, and model evaluation.

### Technical Concepts Used

- Data analysis with pandas.
- Data visualization with matplotlib and seaborn.
- Text vectorization using TF-IDF.
- Train-test split.
- Feature scaling.
- Linear Regression.
- Neural Network using TensorFlow/Keras.
- Model evaluation using MSE and RMSE.
- Word cloud generation.

### Questions You Can Expect

| Question | Suggested Answer |
| --- | --- |
| What problem does this project solve? | It analyzes user reviews and predicts app ratings from review text. |
| Why did you use TF-IDF? | ML models need numerical input, and TF-IDF converts text into meaningful numeric features. |
| Why did you use MSE? | The model predicts ratings as numeric values, so it is a regression problem. MSE measures prediction error. |
| Which model performed better? | Linear Regression performed slightly better with an MSE of 0.7231. |
| Why did the Neural Network not perform better? | The dataset is highly skewed toward positive ratings, and simple TF-IDF features may not require a complex model. |
| How can you improve this project? | Add better preprocessing, sentiment classification, Logistic Regression, class balancing, and advanced NLP models. |

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the library management app:

```bash
python library_management.py
```

Open the ML notebook:

```bash
jupyter notebook final_chatgptreview.ipynb
```

## Notes

The library app creates `books.csv`, `patrons.csv`, and `borrowed_books.csv` at runtime. These generated files are ignored by git.

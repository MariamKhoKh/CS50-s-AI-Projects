# Shopping Prediction using K-Nearest Neighbors

This project implements a simple machine learning model to predict whether a user will complete a purchase on an online shopping website, based on data collected during their browsing session.

The model is based on the k-nearest neighbors algorithm (k=1) and is implemented in Python using the scikit-learn library.

---

## Objective

The primary objective of this project is to train a binary classifier that can predict user purchasing behavior based on features such as the number of pages visited, session duration, browser used, day of the week, and more. The classifier attempts to distinguish between users who will make a purchase (positive label) and those who will not (negative label).

---

## Requirements

- Python 3.6 or later
- `scikit-learn` Python library

To install the required package, run:
```bash
pip install scikit-learn
```

How to Run
To execute the program, run the following command:

```bash
python shopping.py shopping.csv
```
Upon execution, the script will output the number of correct and incorrect predictions, along with the true positive rate (sensitivity) and true negative rate (specificity).

## Implementation Overview
1. load_data(filename)
Loads and parses data from the provided CSV file.

Converts each row into a list of numerical features (evidence) and a corresponding label.

Handles categorical and boolean values by converting them to numerical form:

Month strings are converted to integer indices (January = 0, ..., December = 11).

VisitorType is mapped to 1 for returning visitors, and 0 otherwise.

Weekend and Revenue fields are converted to 1 (True) or 0 (False).

2. train_model(evidence, labels)
Initializes and trains a k-nearest neighbors classifier with k=1 using the provided training data.

3. evaluate(labels, predictions)
Compares predicted labels to actual labels and calculates:

Sensitivity (True Positive Rate): The proportion of actual positive labels correctly predicted.

Specificity (True Negative Rate): The proportion of actual negative labels correctly predicted.

Data Description
Each row in the CSV dataset represents a user session and contains the following 17 features (used as evidence):

Administrative (int)

Administrative_Duration (float)

Informational (int)

Informational_Duration (float)

ProductRelated (int)

ProductRelated_Duration (float)

BounceRates (float)

ExitRates (float)

PageValues (float)

SpecialDay (float)

Month (int: 0 for January through 11 for December)

OperatingSystems (int)

Browser (int)

Region (int)

TrafficType (int)

VisitorType (int: 1 for returning, 0 otherwise)

Weekend (int: 1 if true, 0 otherwise)

The label is a single integer:

1 if the user made a purchase

0 otherwise
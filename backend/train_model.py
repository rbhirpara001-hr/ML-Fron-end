import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_PATH = os.path.join(
    BASE_DIR,
    "cardio_train.csv"
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "cardio_model.pkl"
)

SCALER_PATH = os.path.join(
    BASE_DIR,
    "scaler.pkl"
)


# ============================================================
# CHECK CSV
# ============================================================

print("==========================================")
print(" CARDIOVASCULAR MODEL TRAINING")
print("==========================================")

print("\nChecking CSV file...")

if not os.path.exists(CSV_PATH):

    print("ERROR: CSV file not found!")
    print("Expected location:")
    print(CSV_PATH)

    exit(1)

print("CSV found:")
print(CSV_PATH)


# ============================================================
# LOAD DATASET
# ============================================================

try:

    df = pd.read_csv(
        CSV_PATH,
        sep=";"
    )

    print("\nDataset loaded successfully!")
    print("Dataset shape:", df.shape)

except Exception as e:

    print("\nERROR reading dataset:")
    print(e)

    exit(1)


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [
    "id",
    "age",
    "gender",
    "height",
    "weight",
    "ap_hi",
    "ap_lo",
    "cholesterol",
    "gluc",
    "smoke",
    "alco",
    "active",
    "cardio"
]


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    print("\nERROR: Missing columns:")
    print(missing_columns)

    exit(1)


print("\nAll required columns found!")


# ============================================================
# AGE CONVERSION
# ============================================================
# Dataset age is stored in days.
# Frontend sends age in years.
# Therefore convert dataset age to years.

df["age"] = np.ceil(
    df["age"] / 365
).astype(int)

print("\nAge converted from days to years.")


# ============================================================
# REMOVE INVALID BLOOD PRESSURE VALUES
# ============================================================

before_filter = len(df)

df = df[
    (df["ap_hi"] >= 60) &
    (df["ap_hi"] <= 250) &
    (df["ap_lo"] >= 40) &
    (df["ap_lo"] <= 200)
]

after_filter = len(df)

print("\nBlood pressure filtering completed.")

print(
    "Rows before filtering:",
    before_filter
)

print(
    "Rows after filtering:",
    after_filter
)


# ============================================================
# FEATURES
# ============================================================
# IMPORTANT:
# id is NOT used as a prediction feature.
#
# Only these 11 fields are used.

feature_columns = [
    "age",
    "gender",
    "height",
    "weight",
    "ap_hi",
    "ap_lo",
    "cholesterol",
    "gluc",
    "smoke",
    "alco",
    "active"
]


X = df[feature_columns]

Y = df["cardio"]


print("\n==========================================")
print("MODEL FEATURES")
print("==========================================")

for index, column in enumerate(
    feature_columns,
    start=1
):

    print(
        f"{index}. {column}"
    )


print("\nTotal features:", len(feature_columns))


# ============================================================
# TRAIN TEST SPLIT
# ============================================================

X_train, X_test, Y_train, Y_test = train_test_split(

    X,
    Y,

    test_size=0.20,

    random_state=42,

    stratify=Y
)


print("\n==========================================")
print("TRAIN / TEST SPLIT")
print("==========================================")

print(
    "Training rows:",
    len(X_train)
)

print(
    "Testing rows:",
    len(X_test)
)


# ============================================================
# STANDARD SCALER
# ============================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(
    X_train
)

X_test_scaled = scaler.transform(
    X_test
)


# ============================================================
# TRAIN MODEL
# ============================================================

print("\nTraining Logistic Regression model...")

model = LogisticRegression(
    max_iter=2000,
    random_state=42
)

model.fit(
    X_train_scaled,
    Y_train
)


print("Model training completed!")


# ============================================================
# MODEL EVALUATION
# ============================================================

Y_pred = model.predict(
    X_test_scaled
)

accuracy = accuracy_score(
    Y_test,
    Y_pred
)


print("\n==========================================")
print("MODEL EVALUATION")
print("==========================================")

print(
    f"Test Accuracy: {accuracy * 100:.2f}%"
)

print("\nClassification Report:")

print(
    classification_report(
        Y_test,
        Y_pred
    )
)


# ============================================================
# SAVE MODEL
# ============================================================

joblib.dump(
    model,
    MODEL_PATH
)

print("\nModel saved successfully:")
print(MODEL_PATH)


# ============================================================
# SAVE SCALER
# ============================================================

joblib.dump(
    scaler,
    SCALER_PATH
)

print("\nScaler saved successfully:")
print(SCALER_PATH)


# ============================================================
# FINAL
# ============================================================

print("\n==========================================")
print(" TRAINING PROCESS COMPLETED SUCCESSFULLY")
print("==========================================")

print("\nGenerated files:")

print("1. cardio_model.pkl")
print("2. scaler.pkl")

print("\nFeatures used by model:")

print(feature_columns)

print("\nTotal features used:", len(feature_columns))

print("\n==========================================")
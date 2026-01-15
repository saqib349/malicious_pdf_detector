from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import joblib
import numpy as np

# Load dataset
df = pd.read_parquet("PDFMalware2022.parquet")

PDFID_FEATURES = [
    "Obj", "Stream", "JS", "Javascript",
    "Launch", "EmbeddedFile", "XFA",
    "Encrypt", "Acroform"
]

# Keep only required columns
df = df[PDFID_FEATURES + ["Class"]]

# Map labels
df["Class"] = df["Class"].map({"Benign": 0, "Malicious": 1})

# Convert to numeric
for col in PDFID_FEATURES:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

# -------------------------------
# FEATURE ENGINEERING
# -------------------------------

# Avoid division by zero
df["Obj_safe"] = df["Obj"] + 1

# ---- Ratio features (behavior intensity) ----
df["JS_ratio"] = df["JS"] / df["Obj_safe"]
df["Stream_ratio"] = df["Stream"] / df["Obj_safe"]
df["XFA_ratio"] = df["XFA"] / df["Obj_safe"]
df["EmbeddedFile_ratio"] = df["EmbeddedFile"] / df["Obj_safe"]

# ---- Binary flags (capability presence) ----
df["HasJS"] = (df["JS"] > 0).astype(int)
df["HasLaunch"] = (df["Launch"] > 0).astype(int)
df["HasEmbeddedFile"] = (df["EmbeddedFile"] > 0).astype(int)
df["HasXFA"] = (df["XFA"] > 0).astype(int)
df["IsEncrypted"] = (df["Encrypt"] > 0).astype(int)

# ---- Complexity awareness ----
df["IsComplexPDF"] = (df["Obj"] > 500).astype(int)

# Final feature set (IMPORTANT)
FEATURE_COLUMNS = [
    "JS_ratio",
    "Stream_ratio",
    "XFA_ratio",
    "EmbeddedFile_ratio",
    "HasJS",
    "HasLaunch",
    "HasEmbeddedFile",
    "HasXFA",
    "IsEncrypted",
    "IsComplexPDF"
]

X = df[FEATURE_COLUMNS].copy()

X.replace([np.inf, -np.inf], np.nan, inplace=True)
X.fillna(0, inplace=True)
X = X.clip(upper=1.0)
X = X.astype("float32")
y = df["Class"]

# -------------------------------
# TRAIN / TEST SPLIT
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# -------------------------------
# TRAIN MODEL
# -------------------------------
model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced",
    max_depth=12
)

model.fit(X_train, y_train)

# -------------------------------
# EVALUATION
# -------------------------------
y_pred = model.predict(X_test)

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# -------------------------------
# SAVE MODEL
# -------------------------------
joblib.dump(model, "rf_pdfid_engineered_model.pkl")

print("\nModel saved as rf_pdfid_engineered_model.pkl")

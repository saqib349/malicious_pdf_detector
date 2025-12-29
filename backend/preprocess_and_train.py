from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import joblib


df = pd.read_parquet("PDFMalware2022.parquet")
PDFID_FEATURES = [
    "Obj", "Endobj", "Stream", "Endstream",
    "Xref", "Trailer", "StartXref", "ObjStm",
    "JS", "Javascript", "AA", "OpenAction",
    "Acroform", "JBIG2Decode", "RichMedia",
    "Launch", "EmbeddedFile", "XFA", "Encrypt"
]

df = df[PDFID_FEATURES + ["Class"]]

# Map Class labels
df["Class"] = df["Class"].map({"Benign": 0, "Malicious": 1})

# Convert all PDFID features to numeric (int)
for col in PDFID_FEATURES:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

X = df.drop(columns=["Class"])
y = df["Class"]


print(X.dtypes)


# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train Random Forest
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

joblib.dump(model, "rf_pdfid_only_model.pkl")

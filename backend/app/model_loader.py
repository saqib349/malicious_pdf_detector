import joblib

MODEL_PATH = "rf_pdf_malware_model.pkl"

model = joblib.load(MODEL_PATH)
print(f"Model loaded from {MODEL_PATH}")

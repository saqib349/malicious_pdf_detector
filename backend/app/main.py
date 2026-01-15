from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import shutil
import os
import uuid
import numpy as np

from app.feature_extractor import extract_pdfid_features
from app.feature_engineering import engineer_features, ENGINEERED_FEATURES

app = FastAPI(title="PDF Malware Detector")

# CORS (React support)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load trained model
model = joblib.load("rf_pdfid_engineered_model.pkl")

@app.post("/scan-pdf")
async def scan_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDFs allowed.")

    tmp_path = f"tmp_{uuid.uuid4()}.pdf"

    try:
        # Save uploaded file
        with open(tmp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # 1️⃣ Extract raw PDFID features
        raw_features = extract_pdfid_features(tmp_path)

        # 2️⃣ Apply feature engineering (SAME AS TRAINING)
        engineered = engineer_features(raw_features)
        print ("Engineered features:", engineered)

        # 3️⃣ Create model input DataFrame (correct order)
        X = pd.DataFrame([[engineered[f] for f in ENGINEERED_FEATURES]],
                         columns=ENGINEERED_FEATURES)

        X = X.astype("float32")

        # 4️⃣ Predict probability
        proba = model.predict_proba(X)[0][1]
        print("Predicted probability of being malicious:", proba)

        mal_prob = model.predict_proba(X)[0][1]

        if mal_prob >= 0.8:
            prediction = "Malicious"
            confidence = mal_prob
        else:
            prediction = "Benign"
            confidence = 1 - mal_prob


        return {
            "prediction": prediction,
            "confidence": round(float(confidence), 4),
            "risk_score": round(float(mal_prob), 4),
            "engineered_features": engineered
        }


    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

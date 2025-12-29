from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import joblib
import shutil
import os
import uuid

from app.feature_extractor import extract_pdfid_features as extract_pdf_features

app = FastAPI(title="PDF Malware Detector")

# CORS (React support)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = joblib.load("rf_pdfid_only_model.pkl")

FEATURES = [
    "Obj", "Endobj", "Stream", "Endstream",
    "Xref", "Trailer", "StartXref", "ObjStm",
    "JS", "Javascript", "AA", "OpenAction",
    "Acroform", "JBIG2Decode", "RichMedia",
    "Launch", "EmbeddedFile", "XFA", "Encrypt"
]

@app.post("/scan-pdf")
async def scan_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDFs allowed.")

    tmp = f"tmp_{uuid.uuid4()}.pdf"
    with open(tmp, "wb") as f:
        shutil.copyfileobj(file.file, f)

    feats = extract_pdf_features(tmp)
    row = {f: feats.get(f, 0) for f in FEATURES}
    df = pd.DataFrame([row])


    pred = model.predict(df)[0]
    conf = model.predict_proba(df).max()

    os.remove(tmp)

    return {
        "prediction": "Malicious" if pred == 1 else "Benign",
        "confidence": round(float(conf), 4),
        "features": row
    }

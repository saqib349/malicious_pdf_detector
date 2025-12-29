📄 Malicious PDF Detector
🔐 Project Overview

The Malicious PDF Detector is a machine learning–based security application designed to identify whether a PDF file is malicious or benign.
The system analyzes structural features of PDF files (using pdfid) rather than file content, making it lightweight, fast, and safe for testing.

This project is developed as part of an Information Security academic project.

🎯 Objectives

Detect malicious PDF files safely without executing them

Use static analysis instead of dynamic execution

Apply machine learning to classify PDFs

Provide a user-friendly web interface for scanning PDFs

🧠 Detection Approach
Feature Extraction

We use PDFID to extract static structural features such as:

/JS, /JavaScript

/AA, /OpenAction

/Launch

/EmbeddedFile

/XFA

/Encrypt

Object and stream counts

These features are commonly associated with malicious behavior in PDFs.

📊 Dataset Description
Dataset Name

Malicious and Benign PDF Dataset (PDFID-based)

Sources

The dataset is compiled from publicly available and safe-for-research sources:

Contagio Malware Dump

https://contagiodump.blogspot.com

VirusShare (Academic Use)

https://virusshare.com

Benign PDFs

Google Books

arXiv.org

University lecture slides and reports

⚠️ Note:
All malicious PDFs are used only for static analysis and are never executed.

⚙️ Tech Stack
Backend

Python

FastAPI

Scikit-learn

Pandas

NumPy

PDFID

Machine Learning Model

Random Forest Classifier

Trained on PDF structural features

Binary classification:

0 → Benign

1 → Malicious

Frontend

React.js

Tailwind CSS

Axios

🧪 Workflow

Upload a PDF file

Extract PDFID features

Normalize and preprocess data

Pass features to trained ML model

Predict result:

Malicious

Benign

Display result in the UI

🖥️ User Interface Features

PDF upload functionality

Scan progress indication

Clear result display (Malicious / Benign)

Future enhancement: feature contribution breakdown

🚀 How to Run the Project
Backend (FastAPI)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

Frontend (React)
cd frontend/pdf_detector
npm install
npm start

📁 Project Structure
malicious_pdf_detector/
│
├── backend/
│   ├── model/
│   ├── preprocess_and_train.py
│   ├── predict.py
│   └── main.py
│
├── frontend/
│   └── pdf_detector/
│       ├── src/
│       └── public/
│
└── README.md

🛡️ Safety Notice

This project does not execute PDFs

Malicious samples are used only for static feature extraction

Safe for academic and educational environments

📌 Future Improvements

Feature importance visualization

Confidence score for predictions

Support for batch scanning

Improved UI with animations

Deep learning models (CNN / RNN on sequences)

👨‍🎓 Author

Saqib Akber
BS Information Technology – 7th Semester
Information Security Project

📜 License

This project is intended for educational and academic use only.
import subprocess
import re

PDFID_FEATURES = [
    "obj", "endobj", "stream", "endstream",
    "xref", "trailer", "startxref",
    "objstm", "js", "javascript", "aa",
    "openaction", "acroform", "jbig2decode",
    "richmedia", "launch", "embeddedfile",
    "xfa", "encrypt"
]

def extract_pdfid_features(pdf_path: str) -> dict:
    # Run pdfid.py and capture output
    result = subprocess.run(
        ["python", "pdfid.py", pdf_path],
        capture_output=True,
        text=True
    )
    output = result.stdout.lower()

    # Mapping pdfid output to capitalized feature names
    FEATURE_NAME_MAP = {
        "obj": "Obj",
        "endobj": "Endobj",
        "stream": "Stream",
        "endstream": "Endstream",
        "xref": "Xref",
        "trailer": "Trailer",
        "startxref": "StartXref",
        "objstm": "ObjStm",
        "js": "JS",
        "javascript": "Javascript",
        "aa": "AA",
        "openaction": "OpenAction",
        "acroform": "Acroform",
        "jbig2decode": "JBIG2Decode",
        "richmedia": "RichMedia",
        "launch": "Launch",
        "embeddedfile": "EmbeddedFile",
        "xfa": "XFA",
        "encrypt": "Encrypt"
    }

    features = {}
    for key, name in FEATURE_NAME_MAP.items():
        match = re.search(rf"{key}\s+(\d+)", output)
        features[name] = int(match.group(1)) if match else 0

    return features

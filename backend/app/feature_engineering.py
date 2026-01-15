import numpy as np

# MUST match training order
ENGINEERED_FEATURES = [
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

def engineer_features(raw: dict) -> dict:
    # Avoid division by zero (same as training)
    obj_safe = raw.get("Obj", 0) + 1

    engineered = {
        # ---- Ratio features ----
        "JS_ratio": raw.get("JS", 0) / obj_safe,
        "Stream_ratio": raw.get("Stream", 0) / obj_safe,
        "XFA_ratio": raw.get("XFA", 0) / obj_safe,
        "EmbeddedFile_ratio": raw.get("EmbeddedFile", 0) / obj_safe,

        # ---- Binary flags ----
        "HasJS": int(raw.get("JS", 0) > 0),
        "HasLaunch": int(raw.get("Launch", 0) > 0),
        "HasEmbeddedFile": int(raw.get("EmbeddedFile", 0) > 0),
        "HasXFA": int(raw.get("XFA", 0) > 0),
        "IsEncrypted": int(raw.get("Encrypt", 0) > 0),

        # ---- Complexity ----
        "IsComplexPDF": int(raw.get("Obj", 0) > 500)
    }

    # Same cleanup as training
    for k in engineered:
        engineered[k] = float(np.clip(engineered[k], 0, 1))

    return engineered

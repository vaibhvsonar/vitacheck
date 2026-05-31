from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
RESULTS_DIR = REPORTS_DIR / "results"

TRAIN_FILE = BASE_DIR / "Symptom2Disease.csv"

MODEL_NAME = "microsoft/BiomedNLP-BiomedBERT-base-uncased-abstract-fulltext"

MAX_LENGTH = 128
RANDOM_STATE = 42
HIGH_CONFIDENCE_THRESHOLD = 0.50
LOW_CONFIDENCE_THRESHOLD = 0.20

for p in [PROCESSED_DATA_DIR, MODELS_DIR, FIGURES_DIR, RESULTS_DIR]:
    p.mkdir(parents=True, exist_ok=True)

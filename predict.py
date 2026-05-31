import torch
import joblib
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from config import MODELS_DIR, MAX_LENGTH

_MODEL = None
_TOKENIZER = None
_LABEL_ENCODER = None


def load_artifacts():
    global _MODEL, _TOKENIZER, _LABEL_ENCODER

    if _MODEL is None or _TOKENIZER is None or _LABEL_ENCODER is None:
        model_dir = MODELS_DIR / "best_model"
        _TOKENIZER = AutoTokenizer.from_pretrained(str(model_dir))
        _MODEL = AutoModelForSequenceClassification.from_pretrained(str(model_dir))
        _MODEL.eval()
        _LABEL_ENCODER = joblib.load(MODELS_DIR / "label_encoder.pkl")

    return _MODEL, _TOKENIZER, _LABEL_ENCODER


def predict_label(text: str):
    model, tokenizer, le = load_artifacts()

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.nn.functional.softmax(outputs.logits, dim=1)
    confidence, pred = torch.max(probs, dim=1)
    label = le.inverse_transform([pred.item()])[0]

    return label, float(confidence.item())


def predict_top_k(text: str, k: int = 3):
    model, tokenizer, le = load_artifacts()

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.nn.functional.softmax(outputs.logits, dim=1)[0]
    top_probs, top_indices = torch.topk(probs, k=min(k, len(probs)))

    results = []
    for prob, idx in zip(top_probs.tolist(), top_indices.tolist()):
        label = le.inverse_transform([idx])[0]
        results.append({
            "label": label,
            "confidence": float(prob)
        })

    # Normalize top-k confidences so they sum to 100%
    total = sum(item["confidence"] for item in results)
    if total > 0:
        for item in results:
            item["confidence"] = (item["confidence"] / total) * 100

    return results
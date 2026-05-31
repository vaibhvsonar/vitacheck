import pandas as pd
from sklearn.metrics import classification_report, accuracy_score
from config import REALTIME_FILE, RESULTS_DIR, CONFIDENCE_THRESHOLD
from predict import predict_label
from safety import safety_override

def main(limit=None):
    df = pd.read_csv(REALTIME_FILE)
    text_col = "user_text" if "user_text" in df.columns else ("text" if "text" in df.columns else None)
    label_col = "label" if "label" in df.columns else None

    if text_col is None:
        raise ValueError(f"Could not find text column in realtime file. Columns: {list(df.columns)}")

    if limit:
        df = df.head(limit).copy()

    rows = []
    for _, row in df.iterrows():
        text = str(row[text_col])
        if safety_override(text):
            pred_label = "chest_pain_breathing" if "chest" in text.lower() or "breathe" in text.lower() else "severe_bleeding"
            confidence = 1.0
        else:
            pred_label, confidence = predict_label(text)

        rows.append({
            "text": text,
            "true_label": row[label_col] if label_col else None,
            "pred_label": pred_label,
            "confidence": confidence,
            "low_confidence": confidence < CONFIDENCE_THRESHOLD
        })

    out_df = pd.DataFrame(rows)
    out_df.to_csv(RESULTS_DIR / "realtime_predictions.csv", index=False)

    if label_col:
        valid_df = out_df.dropna(subset=["true_label"])
        if len(valid_df):
            acc = accuracy_score(valid_df["true_label"], valid_df["pred_label"])
            report = classification_report(valid_df["true_label"], valid_df["pred_label"], zero_division=0)
            with open(RESULTS_DIR / "realtime_classification_report.txt", "w", encoding="utf-8") as f:
                f.write(f"Accuracy: {acc:.4f}\n\n")
                f.write(report)
            print(f"Realtime accuracy: {acc:.4f}")
            print(report)

    print("Saved realtime predictions to reports/results/realtime_predictions.csv")

if __name__ == "__main__":
    main()

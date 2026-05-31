import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer

from config import MODELS_DIR, RESULTS_DIR, FIGURES_DIR, MAX_LENGTH
from preprocess import infer_column, POSSIBLE_TEXT_COLS
from dataset_utils import SymptomDataset

def main():
    test_path = RESULTS_DIR / "test_split.csv"
    if not test_path.exists():
        raise FileNotFoundError("Test split not found. Run train.py first.")

    test_df = pd.read_csv(test_path)
    text_col = infer_column(test_df, POSSIBLE_TEXT_COLS)

    le = joblib.load(MODELS_DIR / "label_encoder.pkl")
    model_dir = MODELS_DIR / "best_model"

    tokenizer = AutoTokenizer.from_pretrained(str(model_dir))
    model = AutoModelForSequenceClassification.from_pretrained(str(model_dir))

    encodings = tokenizer(
        test_df[text_col].tolist(),
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH
    )
    dataset = SymptomDataset(encodings, test_df["label_encoded"].tolist())

    trainer = Trainer(model=model)
    pred_output = trainer.predict(dataset)
    preds = pred_output.predictions.argmax(axis=1)
    true_labels = pred_output.label_ids

    report = classification_report(
        true_labels,
        preds,
        target_names=le.classes_,
        zero_division=0
    )
    cm = confusion_matrix(true_labels, preds)

    with open(RESULTS_DIR / "classification_report.txt", "w", encoding="utf-8") as f:
        f.write(report)

    pd.DataFrame(cm, index=le.classes_, columns=le.classes_).to_csv(
        RESULTS_DIR / "confusion_matrix.csv"
    )

    plt.figure(figsize=(12, 10))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=le.classes_,
        yticklabels=le.classes_
    )
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=45)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "confusion_matrix.png", dpi=300)
    plt.close()

    print(report)
    print("Saved classification report and confusion matrix.")

if __name__ == "__main__":
    main()
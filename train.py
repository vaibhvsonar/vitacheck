import json
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback,
)

from config import TRAIN_FILE, MODELS_DIR, MODEL_NAME, MAX_LENGTH, RESULTS_DIR
from preprocess import load_raw_dataframe, clean_dataframe, encode_labels, create_splits
from dataset_utils import SymptomDataset

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=1)
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, predictions, average="weighted", zero_division=0
    )
    acc = accuracy_score(labels, predictions)
    return {
        "accuracy": acc,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }

def main():
    print("Loading dataset...")
    raw_df = load_raw_dataframe(TRAIN_FILE)
    df, text_col, label_col = clean_dataframe(raw_df)
    df, le = encode_labels(df, label_col)
    train_df, val_df, test_df = create_splits(df)

    print(f"Detected text column: {text_col}")
    print(f"Detected label column: {label_col}")
    print(f"Number of classes: {len(le.classes_)}")
    print(f"Train size: {len(train_df)} | Val size: {len(val_df)} | Test size: {len(test_df)}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    train_encodings = tokenizer(
        train_df[text_col].tolist(),
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH
    )
    val_encodings = tokenizer(
        val_df[text_col].tolist(),
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH
    )
    test_encodings = tokenizer(
        test_df[text_col].tolist(),
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH
    )

    train_dataset = SymptomDataset(train_encodings, train_df["label_encoded"].tolist())
    val_dataset = SymptomDataset(val_encodings, val_df["label_encoded"].tolist())
    test_dataset = SymptomDataset(test_encodings, test_df["label_encoded"].tolist())

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=len(le.classes_)
    )

    training_args = TrainingArguments(
        output_dir=str(MODELS_DIR / "results"),
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_strategy="epoch",
        learning_rate=2e-5,
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        save_total_limit=2,
        report_to="none"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
    )

    print("Training started...")
    trainer.train()

    best_model_dir = MODELS_DIR / "best_model"
    trainer.save_model(str(best_model_dir))
    tokenizer.save_pretrained(str(best_model_dir))

    metrics = trainer.evaluate(test_dataset)
    with open(MODELS_DIR / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    split_info = {
        "text_column": text_col,
        "label_column": label_col,
        "train_size": len(train_df),
        "val_size": len(val_df),
        "test_size": len(test_df),
        "labels": list(le.classes_)
    }
    with open(RESULTS_DIR / "dataset_info.json", "w", encoding="utf-8") as f:
        json.dump(split_info, f, indent=2)

    train_df.to_csv(RESULTS_DIR / "train_split.csv", index=False)
    val_df.to_csv(RESULTS_DIR / "val_split.csv", index=False)
    test_df.to_csv(RESULTS_DIR / "test_split.csv", index=False)

    print("Training complete.")
    print("Saved model to:", best_model_dir)
    print("Test metrics:", metrics)

if __name__ == "__main__":
    main()
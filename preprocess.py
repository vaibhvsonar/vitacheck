import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

from config import TRAIN_FILE, MODELS_DIR, RANDOM_STATE

POSSIBLE_TEXT_COLS = ["text", "user_text", "query", "utterance"]
POSSIBLE_LABEL_COLS = ["label", "intent", "category"]

def infer_column(df: pd.DataFrame, possible_names):
    for c in possible_names:
        if c in df.columns:
            return c
    raise ValueError(
        f"Could not find one of expected columns: {possible_names}. "
        f"Found columns: {list(df.columns)}"
    )

def load_raw_dataframe(filepath=TRAIN_FILE):
    return pd.read_csv(filepath)

def clean_dataframe(df: pd.DataFrame):
    text_col = infer_column(df, POSSIBLE_TEXT_COLS)
    label_col = infer_column(df, POSSIBLE_LABEL_COLS)

    df = df[[text_col, label_col]].copy()
    df[text_col] = df[text_col].astype(str).str.strip()
    df[label_col] = df[label_col].astype(str).str.strip()

    df = df.dropna(subset=[text_col, label_col])
    df = df[(df[text_col] != "") & (df[label_col] != "")]
    df = df.drop_duplicates(subset=[text_col, label_col]).reset_index(drop=True)

    return df, text_col, label_col

def encode_labels(df: pd.DataFrame, label_col: str):
    le = LabelEncoder()
    df["label_encoded"] = le.fit_transform(df[label_col])
    joblib.dump(le, MODELS_DIR / "label_encoder.pkl")
    return df, le

def create_splits(df: pd.DataFrame, label_encoded_col="label_encoded"):
    train_df, temp_df = train_test_split(
        df,
        test_size=0.20,
        stratify=df[label_encoded_col],
        random_state=RANDOM_STATE
    )

    val_df, test_df = train_test_split(
        temp_df,
        test_size=0.50,
        stratify=temp_df[label_encoded_col],
        random_state=RANDOM_STATE
    )

    train_df = train_df.copy()
    val_df = val_df.copy()
    test_df = test_df.copy()

    train_df["split"] = "train"
    val_df["split"] = "val"
    test_df["split"] = "test"

    return train_df, val_df, test_df
# VitaCheck - AI Symptom Intelligence

VitaCheck is an AI-powered healthcare assistant designed to analyze user-described symptoms and predict possible underlying conditions using a fine-tuned transformer model (BiomedBERT). It provides real-time confidence scores, safety/triage warnings, and educational guidance about the predicted conditions.

## Features

- **Symptom Analysis**: Users describe their symptoms in natural language, and the system predicts the top 3 most likely medical conditions.
- **BiomedBERT Integration**: Utilizes a fine-tuned Hugging Face `AutoModelForSequenceClassification` based on a custom dataset (`Symptom2Disease.csv`).
- **Dual Interfaces**:
  - **Flask REST API**: A lightweight backend serving predictions (`app.py`).
  - **Streamlit Web App**: An interactive web-based frontend for easy testing and demonstration (`streamlit_app.py`).
- **Safety & Triage Mechanisms**: 
  - Overrides for emergency situations (e.g., severe chest pain, extreme bleeding).
  - Out-of-scope filters to reject non-medical queries.
- **Confidence Scoring**: Returns predictions grouped into High, Moderate, and Low confidence tiers.

## Project Structure

- `app.py`: Flask API server exposing the `/analyse` endpoint.
- `streamlit_app.py`: Streamlit frontend application.
- `train.py`: Training script for fine-tuning the BiomedBERT model.
- `predict.py`: Inference module that loads the trained model and returns predictions.
- `preprocess.py`: Data cleaning, label encoding, and train/val/test splitting logic.
- `dataset_utils.py`: PyTorch custom `Dataset` class for feeding data into the trainer.
- `config.py`: Configuration variables (thresholds, paths, model names).
- `input_filter.py` / `safety.py` / `triage.py`: Utility modules for handling safety checks, greetings, and emergency triage.

## Setup Instructions

1. **Clone the repository or download the source code.**
2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Train the Model (If not already trained):**
   ```bash
   python train.py
   ```
   *This will read `Symptom2Disease.csv`, fine-tune the model, and save it in the `models/best_model` directory.*
5. **Run the Application:**
   - **For Streamlit App:**
     ```bash
     streamlit run streamlit_app.py
     ```
   - **For Flask API:**
     ```bash
     python app.py
     ```

## Disclaimer
*This tool is for educational and informational use only. It does not provide diagnosis or treatment recommendations. Always consult a qualified healthcare professional for medical advice.*"# VitaCheck_2" 
"# vitacheck" 

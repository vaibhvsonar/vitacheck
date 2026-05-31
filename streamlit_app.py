import sys
from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from predict import predict_label, predict_top_k
from responses import format_primary_response, format_uncertain_response, OUT_OF_SCOPE_RESPONSE
from safety import safety_override
from input_filter import get_greeting_response, is_capability_or_chat_query, looks_like_symptom_input
from triage import is_hospital_query, get_hospital_recommendation
from config import HIGH_CONFIDENCE_THRESHOLD, LOW_CONFIDENCE_THRESHOLD

def get_status(confidence: float, emergency: bool = False):
    if emergency:
        return "Emergency", "🔴"
    if confidence >= HIGH_CONFIDENCE_THRESHOLD:
        return "Higher Confidence", "🟢"
    if confidence >= LOW_CONFIDENCE_THRESHOLD:
        return "Moderate Confidence", "🟡"
    return "Low Confidence", "⚪"

HELP_MESSAGE = (
    "Please enter a symptom description such as: "
    "'I have fever, body pain, and chills since yesterday.'"
)

st.set_page_config(page_title="Healthcare Chatbot", layout="centered")

st.title("Symptom-Based Healthcare Guidance Chatbot")
st.caption("Powered by BiomedBERT")

user_input = st.text_area("Describe your symptoms")

if st.button("Analyze Symptoms"):
    if not user_input.strip():
        st.warning(HELP_MESSAGE)

    else:
        greeting = get_greeting_response(user_input)
        if greeting:
            st.success(greeting)

        elif is_capability_or_chat_query(user_input):
            st.info(
                "I analyze symptom descriptions and return possible disease associations "
                "with confidence scores. " + HELP_MESSAGE
            )

        elif not looks_like_symptom_input(user_input):
            st.warning("That input does not look like a symptom description. " + HELP_MESSAGE)

        elif safety_override(user_input):
            level, icon = get_status(1.0, emergency=True)
            st.error(f"{icon} {level}: Your symptoms may indicate an emergency. Please seek immediate medical attention.")

        else:
            label, confidence = predict_label(user_input)
            top_predictions = predict_top_k(user_input, k=3)
            level, icon = get_status(confidence)

            st.subheader("Result")
            st.write(f"**Top Predicted Condition:** {label}")
            st.write(f"**Raw Model Confidence:** {confidence * 100:.1f}%")
            st.write(f"**Status:** {icon} {level}")

            if confidence >= HIGH_CONFIDENCE_THRESHOLD:
                st.success(format_primary_response(label, confidence))
            elif confidence >= LOW_CONFIDENCE_THRESHOLD:
                st.warning(format_uncertain_response(top_predictions))
            else:
                st.warning(OUT_OF_SCOPE_RESPONSE)

            st.subheader("Top 3 Possible Associated Conditions")
            st.caption("These percentages are normalized across the top 3 predictions and sum to 100%.")

            for idx, item in enumerate(top_predictions, start=1):
                st.write(f"{idx}. **{item['label']}** — {item['confidence']:.1f}%")

            if is_hospital_query(user_input):
                triage = get_hospital_recommendation(user_input, top_predictions)

                if triage["level"] == "emergency":
                    st.error(triage["message"])
                elif triage["level"] in ["urgent", "doctor_soon"]:
                    st.warning(triage["message"])
                else:
                    st.info(triage["message"])

st.info(
    "This tool is for educational and informational use only. "
    "It does not provide diagnosis or treatment recommendations."
)
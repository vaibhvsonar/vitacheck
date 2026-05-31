# src/triage.py

EMERGENCY_KEYWORDS = [
    "chest pain",
    "cannot breathe",
    "can't breathe",
    "difficulty breathing",
    "shortness of breath",
    "severe bleeding",
    "unconscious",
    "fainted",
    "seizure",
    "tight chest",
]

SEVERE_SYMPTOM_WORDS = [
    "severe",
    "very high fever",
    "high fever",
    "extreme pain",
    "persistent vomiting",
    "vomiting continuously",
    "confusion",
    "unable to walk",
    "very weak",
    "blurred vision",
]

HOSPITAL_QUERY_WORDS = [
    "should i go to the hospital",
    "should i visit the hospital",
    "do i need to go to the hospital",
    "should i see a doctor",
    "do i need a doctor",
    "should i visit a doctor",
    "do i need medical attention",
]

HIGH_RISK_DISEASES = {
    "Malaria",
    "Dengue",
    "Pneumonia",
    "Heart attack",
    "Tuberculosis",
    "Typhoid",
}

MODERATE_RISK_DISEASES = {
    "Bronchial Asthma",
    "Jaundice",
    "Urinary tract infection",
    "Migraine",
    "Peptic ulcer diseae",
    "GERD",
}

def contains_any(text: str, phrases: list[str]) -> bool:
    t = text.lower()
    return any(p.lower() in t for p in phrases)

def is_hospital_query(text: str) -> bool:
    return contains_any(text, HOSPITAL_QUERY_WORDS)

def get_hospital_recommendation(user_text: str, top_predictions: list[dict]) -> dict:
    """
    Returns a triage recommendation dict:
    {
        "level": "emergency" | "urgent" | "doctor_soon" | "monitor",
        "message": "...",
    }
    """
    text = user_text.lower()

    # 1. Emergency keywords override everything
    if contains_any(text, EMERGENCY_KEYWORDS):
        return {
            "level": "emergency",
            "message": (
                "Your symptoms may require immediate hospital care. "
                "Please seek urgent medical attention now."
            ),
        }

    # 2. Severe wording + likely serious prediction
    if top_predictions:
        top_label = top_predictions[0]["label"]
        top_conf = top_predictions[0]["confidence"]

        if contains_any(text, SEVERE_SYMPTOM_WORDS) and top_label in HIGH_RISK_DISEASES:
            return {
                "level": "urgent",
                "message": (
                    f"Your symptoms may be associated with {top_label}, and because your description suggests "
                    "more severe symptoms, it is advisable to seek medical care as soon as possible."
                ),
            }

        if top_label in HIGH_RISK_DISEASES and top_conf >= 0.40:
            return {
                "level": "doctor_soon",
                "message": (
                    f"Your symptoms may be associated with {top_label}. "
                    "It would be advisable to visit a doctor or healthcare facility promptly for evaluation."
                ),
            }

        if top_label in MODERATE_RISK_DISEASES and top_conf >= 0.40:
            return {
                "level": "doctor_soon",
                "message": (
                    f"Your symptoms may be associated with {top_label}. "
                    "Please consider arranging a medical consultation, especially if symptoms continue or worsen."
                ),
            }

    # 3. Default low-risk guidance
    return {
        "level": "monitor",
        "message": (
            "Based on the available information, this does not appear to require immediate hospital care. "
            "However, you should monitor your symptoms and seek medical advice if they worsen, persist, or new concerning symptoms appear."
        ),
    }
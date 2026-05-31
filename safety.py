EMERGENCY_KEYWORDS = [
    "chest pain",
    "shortness of breath",
    "can't breathe",
    "cannot breathe",
    "difficulty breathing",
    "trouble breathing",
    "severe bleeding",
    "heavy bleeding",
    "unconscious",
    "fainted",
    "seizure",
    "tight chest"
]

def safety_override(user_text: str) -> bool:
    text = user_text.lower()
    return any(keyword in text for keyword in EMERGENCY_KEYWORDS)
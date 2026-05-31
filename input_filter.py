import re

GREETING_RESPONSES = {
    # English
    "hi": "Hello!",
    "hello": "Hi there!",
    "hey": "Hello!",
    "good morning": "Good morning!",
    "good afternoon": "Good afternoon!",
    "good evening": "Good evening!",
    "good night": "Good night!",

    # Nepali / Hindi
    "namaste": "Namaste 🙏",
    "namaskar": "Namaste 🙏",
    "नमस्ते": "नमस्ते 🙏",
    "नमस्कार": "नमस्ते 🙏",

    # Spanish
    "hola": "Hola 👋",

    # French
    "bonjour": "Bonjour 👋",

    # German
    "hallo": "Hallo 👋",

    # Italian
    "ciao": "Ciao 👋",

    # Portuguese
    "ola": "Olá 👋",
    "olá": "Olá 👋",

    # Arabic
    "salam": "Salam 👋",
    "assalamualaikum": "Wa Alaikum Salam 🤲",
    "as-salamu alaikum": "Wa Alaikum Salam 🤲",

    # Chinese
    "ni hao": "你好 👋",
    "你好": "你好 👋",

    # Japanese
    "konnichiwa": "こんにちは 👋",
}

CAPABILITY_PATTERNS = [
    r"\bwhat can you do\b",
    r"\bwhat kind of\b",
    r"\bhow do you work\b",
    r"\bwho are you\b",
    r"\bcan you help\b",
    r"\bcan you diagnose\b",
    r"\bwhat symptoms analysis\b",
    r"\bwhat do you do\b",
    r"\bhow can you help\b",
]

CHAT_PATTERNS = [
    r"\bthanks\b",
    r"\bthank you\b",
    r"\bokay\b",
]

SYMPTOM_HINT_WORDS = [
    "pain", "fever", "cough", "cold", "rash", "itch", "vomit", "vomiting",
    "nausea", "breathing", "breathe", "dizzy", "dizziness", "weakness",
    "weak", "headache", "migraine", "urinating", "urination", "burning",
    "stomach", "abdomen", "skin", "chest", "throat", "fatigue", "swelling",
    "chills", "body pain", "mucus", "blood", "bleeding", "back pain",
    "joint pain", "rash", "itchy", "pressure", "red patches", "irritation"
]

def get_greeting_response(text: str):
    t = text.lower().strip()

    for key, response in GREETING_RESPONSES.items():
        if re.search(rf"\b{re.escape(key)}\b", t):
            return response

    return None

def is_capability_or_chat_query(text: str) -> bool:
    t = text.lower().strip()

    for pattern in CAPABILITY_PATTERNS + CHAT_PATTERNS:
        if re.search(pattern, t):
            return True
    return False

def looks_like_symptom_input(text: str) -> bool:
    t = text.lower().strip()

    if any(word in t for word in SYMPTOM_HINT_WORDS):
        return True

    if len(t.split()) < 3:
        return False

    return False
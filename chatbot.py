from predict import predict_label, predict_top_k
from responses import format_primary_response, format_uncertain_response, OUT_OF_SCOPE_RESPONSE
from safety import safety_override
from input_filter import get_greeting_response, is_capability_or_chat_query, looks_like_symptom_input
from triage import is_hospital_query, get_hospital_recommendation
from config import HIGH_CONFIDENCE_THRESHOLD, LOW_CONFIDENCE_THRESHOLD

DISCLAIMER = (
    "This chatbot provides informational results only. "
    "It does not diagnose diseases or prescribe treatment."
)

HELP_MESSAGE = (
    "Please describe your symptoms in natural language. "
    "For example: 'I have fever, body pain, and chills since yesterday.'"
)

def chatbot():
    print("\nSymptom-Based Healthcare Guidance Chatbot")
    print(DISCLAIMER)
    print("Describe multiple symptoms for better results.")
    print("Type 'quit' to stop.\n")

    while True:
        user_text = input("You: ").strip()

        if user_text.lower() == "quit":
            print("Bot: Take care.")
            break

        if not user_text:
            print("Bot:", HELP_MESSAGE)
            continue

        greeting = get_greeting_response(user_text)
        if greeting:
            print("Bot:", greeting)
            continue

        if is_capability_or_chat_query(user_text):
            print("Bot: I analyze symptom descriptions and return possible disease associations with confidence scores. " + HELP_MESSAGE)
            continue

        if not looks_like_symptom_input(user_text):
            print("Bot: That does not look like a symptom description. " + HELP_MESSAGE)
            continue

        if safety_override(user_text):
            print("Bot: Your symptoms may indicate an emergency. Please seek immediate medical attention.")
            continue

        label, confidence = predict_label(user_text)
        top_predictions = predict_top_k(user_text, k=3)

        if confidence >= HIGH_CONFIDENCE_THRESHOLD:
            print("Bot:", format_primary_response(label, confidence))
        elif confidence >= LOW_CONFIDENCE_THRESHOLD:
            print("Bot:", format_uncertain_response(top_predictions))
        else:
            print("Bot:", OUT_OF_SCOPE_RESPONSE)

        print("[Top 3 possible associated conditions]")
        for idx, item in enumerate(top_predictions, start=1):
print(f"  {idx}. {item['label']} | Confidence: {item['confidence']:.1f}%")
        # New hospital logic
        if is_hospital_query(user_text):
            triage = get_hospital_recommendation(user_text, top_predictions)
            print("Bot:", triage["message"])

if __name__ == "__main__":
    chatbot()
def format_primary_response(label: str, confidence: float) -> str:
    return (
        f"Your symptoms may be associated with {label} "
        f"(confidence: {confidence:.2f}). "
        "This is not a confirmed diagnosis. Please consult a qualified healthcare professional "
        "for proper evaluation."
    )

def format_uncertain_response(top_predictions):
    if not top_predictions:
        return (
            "The model is not confident enough to provide a reliable result. "
            "Please provide more detailed symptoms and consult a healthcare professional."
        )

    formatted = ", ".join(
        [f"{item['label']} ({item['confidence']:.2f})" for item in top_predictions]
    )

    return (
        "Possible associated conditions include: "
        f"{formatted}. "
        "Please provide more detailed symptoms and consult a qualified healthcare professional."
    )

OUT_OF_SCOPE_RESPONSE = (
    "I am not confident enough to provide a reliable result. "
    "Please describe your symptoms in more detail and consult a healthcare professional."
)
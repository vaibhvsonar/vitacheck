GUIDANCE_BY_DISEASE = {
    "Acne": {
        "next_steps": "Keep the affected skin clean, avoid picking or squeezing lesions, and monitor whether breakouts are increasing or becoming more inflamed.",
        "seek_help": "Please seek medical advice if the condition becomes severe, painful, persistent, or leaves significant scarring."
    },
    "Arthritis": {
        "next_steps": "Monitor joint pain, swelling, and stiffness, especially if symptoms affect movement or daily activities.",
        "seek_help": "Please arrange a medical consultation if joint pain or stiffness persists, worsens, or limits normal movement."
    },
    "Bronchial Asthma": {
        "next_steps": "Monitor breathing difficulty, wheezing, chest tightness, and coughing episodes closely, especially at night or with activity.",
        "seek_help": "Please seek medical attention if breathing becomes more difficult, chest tightness worsens, or symptoms do not improve."
    },
    "Cervical spondylosis": {
        "next_steps": "Monitor neck pain, stiffness, headaches, and whether symptoms worsen with posture, sitting, or movement.",
        "seek_help": "Please seek medical advice if pain persists, worsens, or affects movement and daily activity."
    },
    "Chicken pox": {
        "next_steps": "Monitor rash progression, itching, and fever, and try to avoid scratching the skin lesions.",
        "seek_help": "Please seek medical advice if symptoms worsen, spread significantly, or are associated with breathing difficulty, severe weakness, or persistent fever."
    },
    "Common Cold": {
        "next_steps": "Rest, stay hydrated, and monitor congestion, sneezing, sore throat, cough, and fever.",
        "seek_help": "Please seek medical advice if symptoms persist, worsen, or are associated with breathing difficulty or high fever."
    },
    "Dengue": {
        "next_steps": "Rest, maintain hydration, and monitor fever, weakness, body pain, and any worsening symptoms closely.",
        "seek_help": "Please seek medical attention promptly if symptoms worsen or if you develop severe weakness, vomiting, bleeding, dizziness, or dehydration."
    },
    "Dimorphic Hemorrhoids": {
        "next_steps": "Monitor pain, itching, swelling, or bleeding during bowel movements, and avoid straining if possible.",
        "seek_help": "Please arrange a medical consultation if symptoms persist, worsen, or if bleeding becomes frequent."
    },
    "Fungal infection": {
        "next_steps": "Monitor whether the affected skin patches are spreading, becoming more itchy, or more irritated.",
        "seek_help": "Please seek medical advice if the rash persists, spreads, or becomes increasingly uncomfortable."
    },
    "Hypertension": {
        "next_steps": "Monitor headache, dizziness, fatigue, or any recurring symptoms carefully.",
        "seek_help": "Please arrange a medical consultation if symptoms persist, recur frequently, or are associated with chest discomfort or vision changes."
    },
    "Impetigo": {
        "next_steps": "Monitor whether the sores are spreading, crusting further, or becoming more irritated.",
        "seek_help": "Please consult a healthcare professional if the lesions spread, worsen, or affect larger areas of skin."
    },
    "Jaundice": {
        "next_steps": "Monitor yellowing of the eyes or skin, appetite changes, fatigue, dark urine, and abdominal discomfort.",
        "seek_help": "Please seek medical assessment promptly, as jaundice usually requires professional evaluation."
    },
    "Malaria": {
        "next_steps": "Monitor recurring fever, chills, sweating, weakness, and body pain carefully, and rest as much as possible.",
        "seek_help": "Please arrange medical evaluation promptly, especially if fever persists, symptoms worsen, or weakness becomes significant."
    },
    "Migraine": {
        "next_steps": "Rest in a quiet, low-light environment and monitor headache severity, nausea, and sensitivity to light or sound.",
        "seek_help": "Please seek medical advice if headaches are severe, recurrent, worsening, or associated with unusual neurological symptoms."
    },
    "Pneumonia": {
        "next_steps": "Monitor cough, mucus production, chest discomfort, breathing difficulty, and fever closely.",
        "seek_help": "Please seek medical attention promptly, especially if breathing difficulty, high fever, or weakness is worsening."
    },
    "Psoriasis": {
        "next_steps": "Monitor whether the affected skin areas are spreading, becoming more irritated, or causing increasing discomfort.",
        "seek_help": "Please consult a healthcare professional if the rash persists, worsens, or affects a larger area of skin."
    },
    "Typhoid": {
        "next_steps": "Monitor persistent fever, abdominal discomfort, weakness, and appetite loss closely.",
        "seek_help": "Please seek medical assessment if symptoms continue for several days, worsen, or you feel increasingly weak."
    },
    "Varicose Veins": {
        "next_steps": "Avoid standing or sitting in one position for long periods and monitor for worsening heaviness, swelling, or visible vein discomfort.",
        "seek_help": "Please arrange a medical consultation if the discomfort is persistent, worsening, or associated with swelling, skin changes, or increasing pain."
    },
    "allergy": {
        "next_steps": "Monitor itching, rash, sneezing, redness, or any progression of symptoms after exposure to possible triggers.",
        "seek_help": "Please seek medical advice if symptoms worsen, persist, or are associated with swelling or breathing difficulty."
    },
    "diabetes": {
        "next_steps": "Monitor thirst, urination frequency, fatigue, and any recurring symptoms closely.",
        "seek_help": "Please arrange a medical consultation if these symptoms persist or worsen."
    },
    "drug reaction": {
        "next_steps": "Monitor rash, itching, irritation, or any spread of symptoms carefully, especially after taking medication.",
        "seek_help": "Please seek medical advice promptly, especially if symptoms worsen or involve swelling, breathing difficulty, or extensive rash."
    },
    "gastroesophageal reflux disease": {
        "next_steps": "Monitor whether symptoms worsen after meals or when lying down, and avoid large, spicy, or oily meals if they seem to trigger discomfort.",
        "seek_help": "Please seek medical advice if symptoms are frequent, severe, persistent, or associated with vomiting, weight loss, or chest discomfort."
    },
    "peptic ulcer disease": {
        "next_steps": "Monitor burning stomach pain, bloating, nausea, and whether symptoms change with meals or an empty stomach.",
        "seek_help": "Please consult a healthcare professional if symptoms persist, worsen, or are associated with vomiting, bleeding, or severe abdominal pain."
    },
    "urinary tract infection": {
        "next_steps": "Maintain hydration and monitor burning urination, frequency, lower abdominal discomfort, and fever.",
        "seek_help": "Please seek medical advice if symptoms persist, worsen, or are associated with fever or increasing pain."
    },
}

DEFAULT_GUIDANCE = {
    "next_steps": "Monitor your symptoms carefully and consider entering more detailed symptom information for better analysis.",
    "seek_help": "Please consult a qualified healthcare professional if symptoms persist, worsen, or cause concern."
}

def get_guidance_for_top_disease(top_predictions):
    if not top_predictions:
        return DEFAULT_GUIDANCE

    top_label = top_predictions[0]["label"]
    return GUIDANCE_BY_DISEASE.get(top_label, DEFAULT_GUIDANCE)
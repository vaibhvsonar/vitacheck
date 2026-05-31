DISEASE_INFO = {
    "Acne": {
        "description": "Acne is a skin condition commonly associated with pimples, inflamed bumps, oily skin, and breakouts, especially on the face, chest, shoulders, or back."
    },
    "Arthritis": {
        "description": "Arthritis is commonly associated with joint pain, stiffness, swelling, and reduced movement, often affecting daily activities."
    },
    "Bronchial Asthma": {
        "description": "Bronchial asthma is a condition commonly associated with wheezing, chest tightness, coughing, and episodes of breathing difficulty."
    },
    "Cervical spondylosis": {
        "description": "Cervical spondylosis is commonly associated with neck pain, stiffness, headaches, and discomfort that may worsen with posture or movement."
    },
    "Chicken pox": {
        "description": "Chicken pox is a contagious viral illness commonly associated with fever followed by itchy red spots and fluid-filled blisters spreading across the body."
    },
    "Common Cold": {
        "description": "Common cold is a mild viral illness commonly associated with sneezing, runny nose, sore throat, congestion, and mild fever."
    },
    "Dengue": {
        "description": "Dengue is a mosquito-borne viral illness commonly associated with high fever, severe headache, pain behind the eyes, joint pain, muscle pain, and weakness."
    },
    "Dimorphic Hemorrhoids": {
        "description": "Dimorphic hemorrhoids are commonly associated with pain, discomfort, itching, swelling, and sometimes bleeding during bowel movements."
    },
    "Fungal infection": {
        "description": "Fungal infection commonly affects the skin and may be associated with itching, redness, scaling, irritation, and spreading rash-like patches."
    },
    "Hypertension": {
        "description": "Hypertension, or high blood pressure, may sometimes be associated with headaches, dizziness, fatigue, or no obvious symptoms at all."
    },
    "Impetigo": {
        "description": "Impetigo is a skin infection commonly associated with red sores, blisters, itching, and yellow crusts, often around the mouth or nose."
    },
    "Jaundice": {
        "description": "Jaundice is commonly associated with yellowing of the eyes and skin, dark urine, fatigue, appetite loss, and possible abdominal discomfort."
    },
    "Malaria": {
        "description": "Malaria is a mosquito-borne infectious disease commonly associated with recurring fever, chills, sweating, weakness, headache, and body aches."
    },
    "Migraine": {
        "description": "Migraine is commonly associated with severe headache, nausea, vomiting, dizziness, and sensitivity to light or sound."
    },
    "Pneumonia": {
        "description": "Pneumonia is a lung infection commonly associated with fever, cough, mucus production, chest discomfort, weakness, and difficulty breathing."
    },
    "Psoriasis": {
        "description": "Psoriasis is a chronic inflammatory skin condition commonly associated with red, scaly, itchy patches and skin irritation."
    },
    "Typhoid": {
        "description": "Typhoid is a bacterial infection commonly associated with persistent fever, weakness, stomach pain, headache, and loss of appetite."
    },
    "Varicose Veins": {
        "description": "Varicose veins are enlarged, swollen veins that commonly appear in the legs and may cause heaviness, aching, and discomfort after long periods of standing or sitting."
    },
    "allergy": {
        "description": "Allergy is commonly associated with itching, rash, redness, sneezing, watery eyes, or irritation after exposure to a trigger."
    },
    "diabetes": {
        "description": "Diabetes is commonly associated with excessive thirst, frequent urination, fatigue, blurred vision, and increased hunger."
    },
    "drug reaction": {
        "description": "Drug reaction is commonly associated with skin rash, itching, irritation, redness, or worsening symptoms after taking a medication."
    },
    "gastroesophageal reflux disease": {
        "description": "Gastroesophageal reflux disease is commonly associated with heartburn, acid reflux, burning chest discomfort, and symptoms that worsen after meals or when lying down."
    },
    "peptic ulcer disease": {
        "description": "Peptic ulcer disease is commonly associated with burning upper stomach pain, bloating, nausea, and discomfort that may worsen when the stomach is empty."
    },
    "urinary tract infection": {
        "description": "Urinary tract infection is commonly associated with burning during urination, frequent urge to urinate, lower abdominal discomfort, and sometimes fever."
    },
}

DEFAULT_DISEASE_DESCRIPTION = (
    "This condition is one of the possible disease associations identified from the entered symptoms. "
    "Please note that this is not a confirmed diagnosis."
)

def get_disease_description(label: str) -> str:
    return DISEASE_INFO.get(label, {}).get("description", DEFAULT_DISEASE_DESCRIPTION)
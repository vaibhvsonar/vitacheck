"""
VitaCheck — AI Symptom Intelligence
Flask API backend (BiomedBERT)

Run:
    pip install flask flask-cors
    python app.py
"""

import sys, os, time
from pathlib import Path

ROOT = os.path.abspath(os.path.dirname(__file__))
for p in (ROOT,):
    if p not in sys.path:
        sys.path.insert(0, p)

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from safety       import safety_override
from input_filter import get_greeting_response, is_capability_or_chat_query, looks_like_symptom_input
from responses    import format_primary_response, format_uncertain_response, OUT_OF_SCOPE_RESPONSE
from config       import HIGH_CONFIDENCE_THRESHOLD, LOW_CONFIDENCE_THRESHOLD
from guidance     import get_guidance_for_top_disease
import predict as predict_module

try:
    from disease_info import get_disease_description
    HAS_DISEASE_INFO = True
    print("  disease_info.py loaded [OK]", flush=True)
except ImportError:
    HAS_DISEASE_INFO = False

try:
    from triage import is_hospital_query, get_hospital_recommendation
    HAS_TRIAGE = True
    print("  triage.py loaded [OK]", flush=True)
except ImportError:
    HAS_TRIAGE = False
    def is_hospital_query(text): return False
    def get_hospital_recommendation(text, top_k): return None

DISEASE_DESCRIPTIONS = {
    "Acne": "Acne is a skin condition that occurs when hair follicles become clogged with oil and dead skin cells.",
    "Arthritis": "Arthritis refers to inflammation of one or more joints, causing pain, swelling, stiffness, and reduced range of motion.",
    "Bronchial Asthma": "Bronchial asthma is a chronic respiratory condition characterized by inflammation and narrowing of the airways.",
    "Cervical spondylosis": "Cervical spondylosis is age-related wear and tear of spinal discs in the neck.",
    "Chicken pox": "Chickenpox is a highly contagious viral infection causing an itchy blister-like rash, fever, tiredness, and loss of appetite.",
    "Common Cold": "The common cold is a viral infection of the upper respiratory tract causing runny nose, sneezing, sore throat, mild cough.",
    "Dengue": "Dengue is a mosquito-borne viral infection causing high fever, severe headache, pain behind the eyes, joint and muscle pain.",
    "Dimorphic Hemorrhoids": "Hemorrhoids are swollen veins in the rectum or anus that can cause pain, itching, discomfort, and bleeding.",
    "Fungal infection": "Fungal skin infections produce itchy, scaly, or discolored patches on the skin.",
    "Hypertension": "Hypertension is persistently elevated blood pressure that can lead to serious heart and kidney complications.",
    "Impetigo": "Impetigo is a superficial bacterial skin infection causing red sores, blisters, itching, and yellow crusting.",
    "Jaundice": "Jaundice causes yellowing of the skin and whites of the eyes due to a build-up of bilirubin in the blood.",
    "Malaria": "Malaria is a mosquito-borne disease causing recurring fever, chills, sweating, headache, nausea, and fatigue.",
    "Migraine": "Migraines are intense recurring headaches accompanied by nausea, vomiting, and sensitivity to light and sound.",
    "Pneumonia": "Pneumonia is a lung infection causing cough with phlegm, fever, chills, and difficulty breathing.",
    "Psoriasis": "Psoriasis is a chronic autoimmune skin condition causing rapid skin cell buildup that forms scales and red, itchy patches.",
    "Typhoid": "Typhoid fever is a bacterial infection producing sustained high fever, abdominal pain, weakness, headache.",
    "Varicose Veins": "Varicose veins are swollen, twisted, enlarged veins occurring just under the skin, most commonly in the legs.",
    "allergy": "Allergies occur when the immune system reacts to a foreign substance, causing sneezing, itching, rash, or swelling.",
    "diabetes": "Diabetes affects how the body processes blood sugar. Symptoms include increased thirst, frequent urination, fatigue.",
    "drug reaction": "A drug reaction is an adverse response to a medication causing skin rash, itching, hives, swelling, or fever.",
    "gastroesophageal reflux disease": "GERD is a digestive disorder where stomach acid flows back into the esophagus, causing heartburn.",
    "peptic ulcer disease": "Peptic ulcers are open sores on the lining of the stomach or small intestine.",
    "urinary tract infection": "A UTI is an infection in the urinary system causing burning urination, frequent urges to urinate, and lower abdominal pain.",
}
DEFAULT_DESCRIPTION = "This condition was identified based on your described symptoms. Please consult a licensed healthcare professional for a proper evaluation."


def get_description(label):
    try:
        from disease_info import get_disease_description as _gdd
        result = _gdd(label)
        if result and result != DEFAULT_DESCRIPTION:
            return result
    except Exception:
        pass
    return DISEASE_DESCRIPTIONS.get(label, DEFAULT_DESCRIPTION)


print("\n  Loading BiomedBERT model…", flush=True)
t0 = time.time()
predict_module.load_artifacts()
print(f"  Model ready in {time.time()-t0:.1f}s [OK]", flush=True)

predict_label = predict_module.predict_label
predict_top_k = predict_module.predict_top_k

FRONTEND_ROOT = os.path.join(ROOT, "frontend")
app = Flask(__name__, static_folder=FRONTEND_ROOT, static_url_path="")
CORS(app)


@app.route("/")
def index():
    return send_from_directory(FRONTEND_ROOT, "index.html")


@app.route("/logo_dark.jpg")
def logo_dark():
    return send_from_directory(FRONTEND_ROOT, "logo_dark.jpg")


@app.route("/logo_light.jpg")
def logo_light():
    return send_from_directory(FRONTEND_ROOT, "logo_light.jpg")


def normalize_top_k(top_k):
    return [{"label": i["label"], "confidence": round(i["confidence"], 1), "normalized_pct": round(i["confidence"], 1)} for i in top_k]


@app.route("/analyse", methods=["POST"])
def analyse():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()

    if not text:
        return jsonify({"error": "No input provided."}), 400

    if safety_override(text):
        return jsonify({"type": "emergency"})

    greeting = get_greeting_response(text)
    if greeting:
        return jsonify({"type": "greeting", "message": greeting})

    if is_capability_or_chat_query(text):
        return jsonify({"type": "capability"})

    if not looks_like_symptom_input(text):
        return jsonify({"type": "out_of_scope", "message": OUT_OF_SCOPE_RESPONSE})

    label, confidence   = predict_label(text)
    top_k_raw           = predict_top_k(text, k=3)
    top_k               = normalize_top_k(top_k_raw)
    guidance            = get_guidance_for_top_disease(top_k)
    disease_description = get_description(label)

    if confidence >= HIGH_CONFIDENCE_THRESHOLD:
        tier, response_msg = "high", format_primary_response(label, confidence)
    elif confidence >= LOW_CONFIDENCE_THRESHOLD:
        tier, response_msg = "moderate", format_uncertain_response(top_k_raw)
    else:
        tier, response_msg = "low", format_uncertain_response(top_k_raw)

    result = {
        "type": "result", "label": label,
        "confidence": round(float(confidence) * 100, 1),
        "tier": tier, "message": response_msg,
        "top_k": top_k, "triage": None,
        "guidance": guidance, "disease_description": disease_description,
    }

    if HAS_TRIAGE and is_hospital_query(text):
        try:
            hosp = get_hospital_recommendation(text, top_k_raw)
            result["triage"] = hosp if isinstance(hosp, dict) else {"level": "monitor", "message": str(hosp)}
        except Exception:
            result["triage"] = {"level": "monitor", "message": "Please consult a qualified healthcare professional."}

    return jsonify(result)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model": "BiomedBERT", "app": "VitaCheck"})


if __name__ == "__main__":
    print(f"\n  [OK]  VitaCheck -> http://localhost:5000\n", flush=True)
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False, threaded=False)
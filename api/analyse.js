// Vercel Serverless Function: /api/analyse
// Handles POST /api/analyse and proxies to BACKEND_URL if configured,
// or provides built-in clinical triage and symptom analysis engine.

const EMERGENCY_KEYWORDS = [
  "chest pain", "shortness of breath", "can't breathe", "cannot breathe",
  "difficulty breathing", "trouble breathing", "severe bleeding", "heavy bleeding",
  "unconscious", "fainted", "seizure", "tight chest", "heart attack", "stroke"
];

const GREETINGS = {
  "hi": "Hello!", "hello": "Hi there!", "hey": "Hello!",
  "good morning": "Good morning!", "good afternoon": "Good afternoon!",
  "good evening": "Good evening!", "good night": "Good night!",
  "namaste": "Namaste 🙏", "namaskar": "Namaste 🙏",
  "hola": "Hola 👋", "bonjour": "Bonjour 👋", "hallo": "Hallo 👋",
  "ciao": "Ciao 👋", "ola": "Olá 👋", "salam": "Salam 👋"
};

const DISEASE_PROFILES = [
  {
    name: "Common Cold",
    keywords: ["runny nose", "sneezing", "congestion", "sore throat", "mild fever", "cough", "phlegm", "cold", "chills"],
    category: "respiratory",
    description: "Common cold is a mild viral illness commonly associated with sneezing, runny nose, sore throat, congestion, and mild cough.",
    guidance: {
      next_steps: "Rest, stay well hydrated, and monitor congestion, sneezing, sore throat, cough, and fever.",
      seek_help: "Please seek medical advice if symptoms persist for over 10 days, worsen, or are associated with breathing difficulty or high fever."
    }
  },
  {
    name: "Bronchial Asthma",
    keywords: ["wheezing", "chest tightness", "coughing", "breathing difficulty", "short of breath", "breathless", "asthma"],
    category: "respiratory",
    description: "Bronchial asthma is a condition commonly associated with wheezing, chest tightness, coughing, and episodes of breathing difficulty.",
    guidance: {
      next_steps: "Monitor breathing difficulty, wheezing, chest tightness, and coughing episodes closely, especially at night or with physical activity.",
      seek_help: "Please seek medical attention if breathing becomes difficult, chest tightness worsens, or symptoms do not respond to usual relief."
    }
  },
  {
    name: "Pneumonia",
    keywords: ["phlegm", "mucus", "high fever", "chest discomfort", "deep cough", "shaking chills", "lung pain", "rapid breathing"],
    category: "respiratory",
    description: "Pneumonia is a lung infection commonly associated with fever, cough, mucus production, chest discomfort, weakness, and difficulty breathing.",
    guidance: {
      next_steps: "Monitor cough, mucus production, chest discomfort, breathing difficulty, and fever closely.",
      seek_help: "Please seek medical attention promptly, especially if breathing difficulty, high fever, or weakness is worsening."
    }
  },
  {
    name: "Migraine",
    keywords: ["throbbing headache", "one side of head", "nausea", "light sensitivity", "sound sensitivity", "pulsing", "migraine", "vision blur"],
    category: "neurological",
    description: "Migraine is commonly associated with severe headache, nausea, vomiting, dizziness, and sensitivity to light or sound.",
    guidance: {
      next_steps: "Rest in a quiet, dark environment, stay hydrated, and note any food or environmental triggers.",
      seek_help: "Please seek medical advice if headaches are unusually severe, frequent, worsening, or associated with vision or neurological changes."
    }
  },
  {
    name: "Dengue",
    keywords: ["high fever", "pain behind eyes", "joint pain", "severe body ache", "breakbone", "platelet", "red spots rash", "dengue"],
    category: "general_infection",
    description: "Dengue is a mosquito-borne viral illness commonly associated with high fever, severe headache, pain behind the eyes, joint pain, muscle pain, and weakness.",
    guidance: {
      next_steps: "Rest, maintain vigorous hydration with fluids/electrolytes, and monitor platelet count and fever.",
      seek_help: "Please seek medical attention promptly if you notice bleeding gums, persistent vomiting, severe abdominal pain, or extreme lethargy."
    }
  },
  {
    name: "Malaria",
    keywords: ["recurring fever", "shivering chills", "sweating", "headache", "fatigue", "body aches", "malaria"],
    category: "general_infection",
    description: "Malaria is a mosquito-borne infectious disease commonly associated with recurring fever, chills, sweating, weakness, headache, and body aches.",
    guidance: {
      next_steps: "Monitor recurring fever, chills, sweating, and weakness carefully; rest as much as possible.",
      seek_help: "Please arrange medical evaluation promptly for blood testing, especially if fever persists and weakness becomes significant."
    }
  },
  {
    name: "Typhoid",
    keywords: ["prolonged fever", "stomach pain", "headache", "loss of appetite", "weakness", "typhoid", "constipation or diarrhea"],
    category: "general_infection",
    description: "Typhoid is a bacterial infection commonly associated with persistent fever, weakness, stomach pain, headache, and loss of appetite.",
    guidance: {
      next_steps: "Rest, eat clean well-cooked food, maintain hydration, and track daily temperature patterns.",
      seek_help: "Please consult a healthcare professional for diagnostic blood tests and appropriate antimicrobial treatment."
    }
  },
  {
    name: "Psoriasis",
    keywords: ["silvery scales", "red patches", "peeling skin", "itchy rash", "dents in nails", "pitted nails", "psoriasis", "dry flaky"],
    category: "skin_related",
    description: "Psoriasis is a chronic inflammatory skin condition commonly associated with red, scaly, itchy patches and skin irritation.",
    guidance: {
      next_steps: "Keep skin well moisturized, avoid harsh chemicals or excessive scratching, and avoid known stress triggers.",
      seek_help: "Please consult a dermatologist for personalized topical therapy and management."
    }
  },
  {
    name: "Fungal infection",
    keywords: ["ring like rash", "itching groin", "athletes foot", "red circular", "itchy toes", "scaling patches", "fungal"],
    category: "skin_related",
    description: "Fungal infection commonly affects the skin and may be associated with itching, redness, scaling, irritation, and spreading rash-like patches.",
    guidance: {
      next_steps: "Keep the affected area clean and dry, avoid sharing towels or footwear, and monitor for spreading.",
      seek_help: "Please seek medical advice if the rash persists, spreads, or becomes increasingly uncomfortable."
    }
  },
  {
    name: "Acne",
    keywords: ["pimples", "blackheads", "whiteheads", "breakouts", "oily skin", "inflamed bumps", "face rash", "acne"],
    category: "skin_related",
    description: "Acne is a skin condition commonly associated with pimples, inflamed bumps, oily skin, and breakouts, especially on the face, chest, shoulders, or back.",
    guidance: {
      next_steps: "Cleanse skin gently twice daily, avoid picking or squeezing lesions, and use non-comedogenic skincare products.",
      seek_help: "Please seek medical advice if the condition becomes severe, painful, persistent, or leaves deep scars."
    }
  },
  {
    name: "Arthritis",
    keywords: ["joint pain", "stiffness in morning", "swollen joints", "knee pain", "finger joint", "reduced movement", "arthritis"],
    category: "musculoskeletal",
    description: "Arthritis is commonly associated with joint pain, stiffness, swelling, and reduced movement, often affecting daily activities.",
    guidance: {
      next_steps: "Apply gentle warm or cool compresses, perform low-impact joint movements, and note daily mobility.",
      seek_help: "Please arrange a medical consultation if joint pain, redness, or stiffness persists or significantly limits walking and movement."
    }
  },
  {
    name: "Cervical spondylosis",
    keywords: ["neck pain", "neck stiffness", "shoulder ache", "numbness fingers", "neck posture", "cervical"],
    category: "musculoskeletal",
    description: "Cervical spondylosis is commonly associated with neck pain, stiffness, headaches, and discomfort that may worsen with posture or movement.",
    guidance: {
      next_steps: "Practice ergonomic sitting posture, gentle neck stretches, and avoid prolonged head-down screen use.",
      seek_help: "Please seek medical advice if pain radiates down your arm, or causes tingling, numbness, or weakness in your hands."
    }
  },
  {
    name: "GERD",
    keywords: ["heartburn", "acid reflux", "burning chest", "sour taste", "regurgitation", "stomach burning after eating", "gerd"],
    category: "digestive",
    description: "Gastroesophageal reflux disease is commonly associated with heartburn, acid reflux, burning chest discomfort, and symptoms that worsen after meals or when lying down.",
    guidance: {
      next_steps: "Avoid lying down for 2-3 hours after meals, reduce spicy and acidic foods, and eat smaller frequent meals.",
      seek_help: "Please consult a healthcare professional if reflux occurs more than twice weekly or causes painful swallowing."
    }
  },
  {
    name: "Peptic ulcer diseae",
    keywords: ["burning stomach", "upper abdomen pain", "empty stomach pain", "indigestion", "nausea", "bloating", "ulcer"],
    category: "digestive",
    description: "Peptic ulcer disease is commonly associated with burning upper stomach pain, bloating, nausea, and discomfort that may worsen when the stomach is empty.",
    guidance: {
      next_steps: "Avoid NSAID pain relievers, avoid excessive alcohol or spicy foods, and eat regularly.",
      seek_help: "Please seek medical evaluation promptly, and seek emergency care if you notice dark tarry stools or vomit containing dark particles."
    }
  },
  {
    name: "Urinary tract infection",
    keywords: ["burning urination", "frequent urination", "cloudy urine", "pelvic pain", "urge to pee", "uti", "stinging urine"],
    category: "urinary",
    description: "Urinary tract infection is commonly associated with burning during urination, frequent urge to urinate, lower abdominal discomfort, and sometimes fever.",
    guidance: {
      next_steps: "Drink plenty of water to flush the urinary tract, avoid holding urine, and maintain proper hygiene.",
      seek_help: "Please consult a doctor promptly for urine analysis and targeted antibiotic prescription."
    }
  },
  {
    name: "Jaundice",
    keywords: ["yellow eyes", "yellow skin", "dark urine", "pale stool", "loss of appetite", "jaundice", "liver pain"],
    category: "digestive",
    description: "Jaundice is commonly associated with yellowing of the eyes and skin, dark urine, fatigue, appetite loss, and possible abdominal discomfort.",
    guidance: {
      next_steps: "Rest, avoid any alcohol consumption, eat light nutritious food, and keep hydrated.",
      seek_help: "Please seek medical assessment promptly, as jaundice requires professional clinical and laboratory evaluation."
    }
  },
  {
    name: "Hypertension",
    keywords: ["high blood pressure", "pounding in ears", "dizziness", "morning headache", "hypertension", "flushing"],
    category: "general_infection",
    description: "Hypertension, or high blood pressure, may sometimes be associated with headaches, dizziness, fatigue, or no obvious symptoms at all.",
    guidance: {
      next_steps: "Measure and record blood pressure readings, limit dietary sodium, stay active, and manage stress.",
      seek_help: "Please arrange a medical checkup, and seek urgent care if high blood pressure is accompanied by chest pain, shortness of breath, or blurred vision."
    }
  }
];

export default async function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET,OPTIONS,PATCH,DELETE,POST,PUT');
  res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method === 'GET') {
    return res.status(200).json({ status: 'ok', model: 'VitaCheck Edge Engine', app: 'VitaCheck' });
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { text } = req.body || {};
  const query = (text || '').trim();

  if (!query) {
    return res.status(400).json({ error: 'Input text is required' });
  }

  // 1. Check if external backend URL is configured via environment variable
  const backendUrl = process.env.BACKEND_URL;
  if (backendUrl) {
    try {
      const externalRes = await fetch(`${backendUrl.replace(/\/+$/, '')}/analyse`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: query })
      });
      if (externalRes.ok) {
        const data = await externalRes.json();
        return res.status(200).json(data);
      }
    } catch (err) {
      console.warn('Backend proxy failed, falling back to local engine:', err.message);
    }
  }

  const lowerQuery = query.toLowerCase();

  // 2. Emergency triage check
  const isEmergency = EMERGENCY_KEYWORDS.some(kw => lowerQuery.includes(kw));
  if (isEmergency) {
    return res.status(200).json({
      type: 'emergency',
      title: '🚨 Immediate Medical Attention Advised',
      message: 'Your symptoms suggest a potentially urgent medical condition. Please seek emergency medical care immediately or call your local emergency services (such as 911 / 112).',
      query: query,
      triage: {
        level: 'emergency',
        message: 'Proceed to the nearest emergency department or call emergency dispatch immediately.'
      }
    });
  }

  // 3. Greeting check
  for (const [kw, resp] of Object.entries(GREETINGS)) {
    const reg = new RegExp(`\\b${kw}\\b`, 'i');
    if (reg.test(lowerQuery)) {
      return res.status(200).json({
        type: 'chat',
        message: `${resp} I am VitaCheck, an AI-powered health assistant. Describe your symptoms (e.g. "I have a sore throat, runny nose and mild fever") to get an assessment.`,
        query: query
      });
    }
  }

  // 4. Capability / Bot inquiries
  if (/(\bwhat can you do\b|\bhow do you work\b|\bwho are you\b|\bcan you help\b|\bwhat do you do\b)/i.test(lowerQuery)) {
    return res.status(200).json({
      type: 'chat',
      message: 'I am VitaCheck. I analyze descriptions of your symptoms, identify potential matching conditions, assess urgency levels, and provide educational guidance.',
      query: query
    });
  }

  // 5. Symptom matching & scoring
  const scores = [];
  const words = lowerQuery.split(/\W+/).filter(w => w.length > 2);

  for (const prof of DISEASE_PROFILES) {
    let matchScore = 0;
    for (const kw of prof.keywords) {
      if (lowerQuery.includes(kw)) {
        matchScore += 3.5;
      } else {
        const kwWords = kw.split(' ');
        for (const kwWord of kwWords) {
          if (words.includes(kwWord)) matchScore += 1.0;
        }
      }
    }
    if (matchScore > 0) {
      scores.push({
        label: prof.name,
        score: matchScore,
        profile: prof
      });
    }
  }

  if (scores.length === 0) {
    return res.status(200).json({
      type: 'out_of_scope',
      message: 'I could not match your input to specific clinical symptoms with sufficient confidence. Please describe specific physical symptoms (such as pain location, fever, rash, duration) and consult a healthcare professional.',
      query: query
    });
  }

  scores.sort((a, b) => b.score - a.score);
  const topMatches = scores.slice(0, 3);
  const totalScore = topMatches.reduce((acc, curr) => acc + curr.score, 0);

  const top_k = topMatches.map(m => ({
    label: m.label,
    confidence: Number(((m.score / totalScore) * 100).toFixed(1))
  }));

  const primary = topMatches[0].profile;

  return res.status(200).json({
    type: 'result',
    query: query,
    top_k: top_k,
    category: primary.category,
    guidance: primary.guidance,
    disease_description: primary.description,
    triage: {
      level: top_k[0].confidence > 60 ? 'routine' : 'monitor',
      message: 'Please consult a certified medical practitioner for definitive clinical evaluation.'
    }
  });
}


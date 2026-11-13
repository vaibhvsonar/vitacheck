# VitaCheck — Vercel Deployment Guide

VitaCheck is configured to deploy directly to Vercel with zero extra setup.

---

## 🚀 Instant Deployment (Two Methods)

### Method 1: Deploy with Vercel Web Dashboard (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Add Vercel deployment configuration"
   git push origin main
   ```

2. **Deploy on Vercel:**
   - Go to [vercel.com/new](https://vercel.com/new).
   - Sign in with GitHub.
   - Import the **`vitacheck`** repository.
   - **Framework Preset**: Leave as `Other`.
   - **Root Directory**: Leave as `./` (or select `frontend`).
   - Click **Deploy**.

---

### Method 2: Deploy using Vercel CLI

Run this in your terminal inside the `vitacheck` folder:
```bash
npx vercel
```
- Select your account.
- Accept the default options by pressing Enter.
- To deploy to production:
```bash
npx vercel --prod
```

---

## ⚙️ How It Works on Vercel

1. **Frontend:**
   Served directly from `frontend/index.html`, `styles.css`, and `script.js` on Vercel's Edge Network with SSL and global CDN.

2. **API Endpoint (`/analyse`):**
   Powered by the Vercel Serverless Function in `api/analyse.js`:
   - Out of the box, it provides built-in clinical triage, emergency override detection, multi-language greetings, and symptom analysis.
   - If you deploy your custom fine-tuned PyTorch / BiomedBERT backend on Render, Hugging Face Spaces, or Railway, simply add an environment variable in your Vercel Dashboard:
     - **Name:** `BACKEND_URL`
     - **Value:** `https://your-backend-service.onrender.com`
   - Vercel will then automatically forward all `/analyse` requests to your heavy PyTorch model!

---

## 🏥 Optional: Deploying the PyTorch Model Backend (Render.com)

If you wish to host the dedicated Python BiomedBERT model:
1. Go to [render.com](https://render.com) and create a **Web Service**.
2. Connect your GitHub repository.
3. Build Command: `pip install -r requirements-backend.txt`
4. Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1`
5. Once deployed, copy your Render URL and add it as `BACKEND_URL` in your Vercel Project Settings → Environment Variables.


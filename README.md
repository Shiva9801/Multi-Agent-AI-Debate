<div align="center">

# 🗣️ Multi-Agent AI Debate

**Ask a question. Watch multiple AI models debate it out, then get one synthesized best answer.**

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://multi-agent-ai-debate.vercel.app)
![Python](https://img.shields.io/badge/backend-FastAPI-009688?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/frontend-React%2019-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/bundler-Vite-646CFF?logo=vite&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/style-TailwindCSS-38B2AC?logo=tailwindcss&logoColor=white)
![Groq](https://img.shields.io/badge/LLMs-Groq%20%2B%20Gemini-orange)

[**Try it live →**](https://multi-agent-ai-debate.vercel.app)

</div>

---

## What is this?

Instead of asking one model and trusting its first answer, this app runs a **3-round debate** between multiple LLMs — they answer independently, critique each other, and a judge model synthesizes the best final answer with a confidence score.

## How it works

```
Your question
      │
      ▼
┌─────────────────────────────┐
│  Round 1 — Initial Answers   │   LLaMA, Mixtral, and Gemini each
│                              │   answer independently, blind to
│                              │   each other's responses
└──────────────┬───────────────┘
               ▼
┌─────────────────────────────┐
│  Round 2 — Cross-Examination │   Each agent reads the others'
│                              │   answers, critiques them, and
│                              │   writes an improved answer
└──────────────┬───────────────┘
               ▼
┌─────────────────────────────┐
│  Round 3 — Judge's Verdict    │   A judge model synthesizes the
│                              │   strongest points into one final
│                              │   answer + a confidence rating
└──────────────┬───────────────┘
               ▼
      Final answer + HIGH / MEDIUM / LOW confidence
```

The frontend shows all three rounds side by side, so you can watch the reasoning evolve instead of just seeing a final answer appear.

## Tech stack

| Layer | Tech |
|---|---|
| Backend | FastAPI, Python, `asyncio` for concurrent model calls |
| Agents | Groq (LLaMA 3.3 70B, Llama 3.1 8B) + Google Generative AI (Gemini 2.5 Flash) |
| Frontend | React 19, Vite, Tailwind CSS |
| Hosting | Vercel (frontend) |

## Project structure

```
Multi-Agent-AI-Debate/
├── backend/
│   ├── main.py           # FastAPI app — exposes POST /debate
│   ├── debate_logic.py   # 3-round debate orchestration (active)
│   ├── debate.py         # earlier debate implementation
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx        # main UI
    │   ├── App.css
    │   └── main.jsx
    ├── package.json
    └── vercel.json
```

## Getting started

### Prerequisites
- Python 3.10+
- Node.js 18+
- API keys: [Groq](https://console.groq.com/) and [Google AI Studio](https://aistudio.google.com/) (Gemini)

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend/.env`:

```env
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
```

Run it:

```bash
uvicorn main:app --reload
```

API docs available at `http://localhost:8000/docs`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Point the frontend's API base URL at your backend (`http://localhost:8000` by default — update in `App.jsx` if deployed elsewhere).

## API

### `POST /debate`

**Request**
```json
{ "question": "Your question here" }
```

**Response**
```json
{
  "round1": { "llama": "...", "mixtral": "...", "gemini": "..." },
  "round2": { "llama": "...", "mixtral": "...", "gemini": "..." },
  "final": "..."
}
```

## Deployment

- **Frontend** → Vercel (`vercel.json` already configured: `npm install` / `npm run build` / `dist`)
- **Backend** → any Python host (Render, Railway, Fly.io, etc.). Update CORS `origins` in `main.py` and the frontend's API URL to match.

## Roadmap / cleanup ideas

- [ ] Add more model providers — `anthropic`, `openai` are already in `requirements.txt` but unused
- [ ] Remove or merge `debate.py` with `debate_logic.py` (near-duplicates)
- [ ] Add persistence for past debates (`supabase` is already a dependency)
- [ ] Add a `.env.example` for easier onboarding

## License

No license file yet — add one (MIT is a common default) if you want others to reuse this freely.

---

<div align="center">
Made with 🤖 x 🤖 x 🤖

</div>

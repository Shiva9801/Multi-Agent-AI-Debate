# Multi-Agent AI Debate System

A web app where multiple AI models (Claude, GPT-4o, Gemini, Gorq) debate your questions, cross-critique each other, and deliver one synthesized final answer with a confidence score.

Built with Python FastAPI backend and React frontend for a smooth production experience.

## Features

- **Multi-Agent Debate**: Three agents answer independently, then refine through cross-examination.
- **Judge Synthesis**: Combines the best insights from all agents into a single final answer (HIGH/MEDIUM/LOW confidence).

## Future additions

- **Live Progress**: Real-time updates via WebSockets as the debate happens.
- **User Auth & History**: Supabase handles secure logins and saved debates.
- **Payments Ready**: Stripe integration for Pro tiers with premium models.
- **Free Tier**: Uses open-source models via Groq and Gemini Flash to start at zero cost.

## Tech Stack

| Layer       | Technology              | Why? |
|-------------|-------------------------|------|
| Backend     | FastAPI, Python        | Simple async APIs – perfect if you know basic Python. |
| AI Models   | Gorq, GPT-4o, Gemini   | Diverse perspectives catch each other's blind spots. |
| Frontend    | React + Tailwind       | Fast UI, no CSS headaches. |
| Database    | Supabase (PostgreSQL)  | Auth, storage, and DB in one free package. |             (Will be used in future)
| Payments    | Stripe                 | Industry standard with great docs. |                     (Will be used in future)
| Deploy      |  

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js LTS
- Free API keys: [Groq](https://console.groq.com), [Gemini AI Studio](https://aistudio.google.com)

### Setup
1. Clone the repo:
   ```
   git clone https://github.com/yourusername/debate-saas.git
   cd debate-saas
   ```

2. Backend setup:
   ```
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env  # Add your API keys here
   uvicorn main:app --reload
   ```

3. Frontend setup:
   ```
   cd ../frontend
   npm install
   npm run dev
   ```

4. Visit `http://localhost:5173` – ask anything and watch the agents debate live!


## Contributing

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

Focus on clean code, helpful comments, and docs. Bug reports welcome!

***

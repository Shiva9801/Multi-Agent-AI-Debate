from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://multi-agent-ai-debate.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Debate API", "docs": "/docs", "debate": "POST /debate"}


@app.post("/debate")
async def debate(data: dict):
    from debate_logic import run_debate
    question = data["question"]
    result = await run_debate(question)
    return result
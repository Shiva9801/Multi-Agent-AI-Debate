from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/debate")
async def debate(data: dict):
    from debate_logic import run_debate
    question = data["question"]
    result = await run_debate(question)
    return result
import asyncio
import os
import warnings
from dotenv import load_dotenv
from groq import Groq
warnings.filterwarnings("ignore", message=".*google.generativeai.*deprecated.*", category=FutureWarning)
import google.generativeai as genai

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def eval_prompt(name, own, others, question):
    return f"""
You are {name}. The question was: '{question}'
Your answer was: {own}
Other agents answered: {others}
Find flaws in their answers, learn from them, and write an IMPROVED answer.
Format your response as:
CRITIQUE: your critique here
IMPROVED ANSWER: your better answer here
"""

async def ask_llama(prompt):
    try:
        res = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except Exception as e:
        print("LLaMA error:", e)
        return "LLaMA unavailable."

async def ask_mixtral(prompt):
    try:
        res = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except Exception as e:
        print("Mixtral error:", e)
        return "Mixtral unavailable."

async def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        res = model.generate_content(prompt)
        return res.text
    except Exception as e:
        print("Gemini error:", e)
        return "Gemini unavailable."

async def run_debate(question):
    # Round 1: All agents answer independently
    llama, mixtral, gemini = await asyncio.gather(
        ask_llama(question),
        ask_mixtral(question),
        ask_gemini(question),
        return_exceptions=True
    )

    # Round 2: Cross evaluation
    llama2, mixtral2, gemini2 = await asyncio.gather(
        ask_llama(eval_prompt("LLaMA", llama, f"Mixtral: {mixtral} Gemini: {gemini}", question)),
        ask_mixtral(eval_prompt("Mixtral", mixtral, f"LLaMA: {llama} Gemini: {gemini}", question)),
        ask_gemini(eval_prompt("Gemini", gemini, f"LLaMA: {llama} Mixtral: {mixtral}", question)),
        return_exceptions=True
    )

    # Round 3: Judge synthesizes
    judge_prompt = f"""
You are an expert judge. The question was: '{question}'
Three AI agents debated and produced these refined answers:
LLaMA: {llama2}
Mixtral: {mixtral2}
Gemini: {gemini2}
Synthesize the single best final answer combining the strongest points.
End with CONFIDENCE: HIGH, MEDIUM, or LOW based on how much the agents agreed.
"""
    
    final = await ask_llama(judge_prompt)

    return {
        "round1": {"llama": str(llama), "mixtral": str(mixtral), "gemini": str(gemini)},
        "round2": {"llama": str(llama2), "mixtral": str(mixtral2), "gemini": str(gemini2)},
        "final": str(final)
    }

import asyncio
import os
from dotenv import load_dotenv
from groq import Groq
import google.generativeai as genai

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


# ---------------- SAFE MODEL CALLS ---------------- #

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
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": prompt}]
        )
        return res.choices[0].message.content
    except Exception as e:
        print("Mixtral error:", e)
        return "Mixtral unavailable."


async def ask_gemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        res = model.generate_content(prompt)
        return res.text
    except Exception as e:
        print("Gemini error:", e)
        return "Gemini unavailable (quota exceeded or error)."


# ---------------- MAIN DEBATE ---------------- #

async def run_debate(question):

    # Round 1
    llama, mixtral, gemini = await asyncio.gather(
        ask_llama(question),
        ask_mixtral(question),
        ask_gemini(question),
    )

    # Round 2
    def eval_prompt(name, own, others):
        return f"""
        You are {name}. The question was: '{question}'
        Your answer was: {own}
        Other agents answered: {others}
        Find flaws in their answers, learn from them, and write an IMPROVED answer.
        Format your response as:
        CRITIQUE: your critique here
        IMPROVED ANSWER: your better answer here
        """

    llama2, mixtral2, gemini2 = await asyncio.gather(
        ask_llama(eval_prompt("LLaMA", llama, f"Mixtral: {mixtral} Gemini: {gemini}")),
        ask_mixtral(eval_prompt("Mixtral", mixtral, f"LLaMA: {llama} Gemini: {gemini}")),
        ask_gemini(eval_prompt("Gemini", gemini, f"LLaMA: {llama} Mixtral: {mixtral}")),
    )

    # Judge
    judge_prompt = f"""
    You are an expert judge. The question was: '{question}'
    Three AI agents debated and produced these refined answers:
    LLaMA: {llama2}
    Mixtral: {mixtral2}
    Gemini: {gemini2}
    Synthesize the single best final answer combining the strongest points.
    End with CONFIDENCE: HIGH, MEDIUM, or LOW.
    """

    final = await ask_llama(judge_prompt)

    return {
        "round1": {"llama": llama, "mixtral": mixtral, "gemini": gemini},
        "round2": {"llama": llama2, "mixtral": mixtral2, "gemini": gemini2},
        "final": final
    }
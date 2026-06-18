from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import os
import json

app = FastAPI()

# Allow frontend (GitHub Pages)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API key from environment (Render)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

# Endpoint
@app.post("/generate")
def generate(request: ChatRequest):
    try:
        user_input = request.messages[-1].content

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a cooking assistant.

Give a recipe clearly in this format:

Recipe Name:
Ingredients:
- item 1
- item 2

Steps:
1. step one
2. step two

Do NOT return JSON.
Just plain text in this format.
"""
                },
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=500
        )

        text = response.choices[0].message.content

        # 🔥 PARSE TEXT → STRUCTURE
        name = "Recipe"
        ingredients = []
        steps = []

        lines = text.split("\n")

        for line in lines:
            line = line.strip()

            if "recipe name" in line.lower():
                name = line.split(":")[-1].strip()

            elif line.startswith("-"):
                ingredients.append(line.replace("-", "").strip())

            elif line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("4."):
                steps.append(line)

        # fallback if AI messy
        if not ingredients:
            ingredients = ["egg", "salt", "oil"]

        if not steps:
            steps = ["Cook ingredients properly"]

        return {
            "recipes": [
                {
                    "name": name,
                    "ingredients": ingredients,
                    "steps": steps
                }
            ],
            "message": "Here’s your recipe!",
            "question": "Want another recipe?",
            "options": ["Chicken", "Snacks", "Dinner"]
        }

    except Exception as e:
        return {
            "recipes": [],
            "message": "AI error. Try again.",
            "question": "What do you want to cook?",
            "options": ["Egg", "Chicken", "Snacks"]
        }
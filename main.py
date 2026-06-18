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
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """
You are Recipe Maker AI.

STRICT RULES:
- Only talk about food and recipes
- ONLY return JSON
- NO explanations
- NO text outside JSON
- Output must be valid JSON

FORMAT:
{
  "recipes": [
    {
      "name": "string",
      "ingredients": ["item1", "item2"],
      "steps": ["step1", "step2"]
    }
  ],
  "message": "string",
  "question": "string",
  "options": ["opt1", "opt2", "opt3"]
}

IMPORTANT:
- If user gives ingredients → ALWAYS return at least 1 recipe
- If unsure → still return a simple recipe
"""
                },
                *[m.dict() for m in request.messages]
            ],
            temperature=0.6,
            max_tokens=700
        )

        content = response.choices[0].message.content

        # 🔥 FORCE CLEAN JSON (VERY IMPORTANT)
        try:
            # Remove possible junk before/after JSON
            start = content.find("{")
            end = content.rfind("}") + 1
            cleaned = content[start:end]

            parsed = json.loads(cleaned)
        except:
            parsed = {
                "recipes": [
                    {
                        "name": "Simple Egg Fry",
                        "ingredients": ["egg", "salt", "oil"],
                        "steps": [
                            "Heat oil in pan",
                            "Crack egg",
                            "Add salt",
                            "Cook until done"
                        ]
                    }
                ],
                "message": "Here is a simple recipe.",
                "question": "Want another recipe?",
                "options": ["Chicken recipes", "Quick meals", "Breakfast ideas"]
            }

        return parsed

    except Exception as e:
        return {
            "recipes": [
                {
                    "name": "Basic Toast",
                    "ingredients": ["bread", "butter"],
                    "steps": [
                        "Toast the bread",
                        "Apply butter"
                    ]
                }
            ],
            "message": "Fallback recipe due to error.",
            "question": "Try another ingredient?",
            "options": ["Egg", "Rice", "Snacks"]
        }
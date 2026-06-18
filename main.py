from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware
import json

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

@app.post("/generate")
def generate(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": """
You are Recipe Maker AI — a strict cooking assistant.

RULES:
- ONLY talk about food, cooking, recipes
- If user asks unrelated things → redirect to food
- ALWAYS return JSON

FORMAT:
{
  "recipes": [
    {
      "name": "",
      "ingredients": [],
      "steps": []
    }
  ],
  "message": "",
  "question": "",
  "options": ["", "", ""]
}

LOGIC:
- If user gives ingredients → generate recipes
- If user unclear → ask food-related question
- If user says random stuff → redirect:
  "I focus on cooking. Tell me ingredients or dish."

NO OTHER BEHAVIOR.
"""
                },
                *[m.dict() for m in request.messages]
            ],
            temperature=0.6,
            max_tokens=700
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except:
            return {
                "recipes": [],
                "message": "I focus on cooking. Tell me ingredients or a dish.",
                "question": "What do you want to cook?",
                "options": ["Egg recipes", "Chicken recipes", "Quick meals"]
            }

    except:
        return {
            "recipes": [],
            "message": "Error occurred. Try again.",
            "question": "What do you want to cook?",
            "options": ["Simple recipes", "Snacks", "Dinner ideas"]
        }
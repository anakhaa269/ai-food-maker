from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
import os
import json

app = FastAPI()

# Allow frontend (GitHub) to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY not set")

# Get API key from environment (Render)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

# API endpoint
@app.post("/generate")
def generate(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are a recipe AI. Always respond in JSON format with recipes."
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
                "message": "Tell me ingredients or a dish.",
                "question": "What do you want to cook?",
                "options": ["Egg recipes", "Chicken recipes", "Quick meals"]
            }

    except Exception as e:
        return {
            "recipes": [],
            "message": "Server error. Try again.",
            "question": "What do you want to cook?",
            "options": ["Simple recipes", "Snacks", "Dinner ideas"]
        }
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from fastapi.middleware.cors import CORSMiddleware
import os
import json

app = FastAPI()

# ✅ CORS (important for GitHub Pages)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ API KEY from Railway environment
api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=api_key)

# ✅ Models
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
You are Recipe Maker AI.

STRICT RULES:
- Only respond about food, recipes, cooking
- Understand simple English inputs
- If user greets → greet back
- If user gives ingredients → generate recipes
- If unclear → ask a question

OUTPUT MUST BE VALID JSON ONLY

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
- Max 5 recipes
- If only 1 ingredient → still generate simple recipes
- If unrelated → say: "I focus on cooking. Tell me ingredients or a dish."
"""
                },
                *[m.dict() for m in request.messages]
            ],
            temperature=0.7,
            max_tokens=800
        )

        content = response.choices[0].message.content

        try:
            data = json.loads(content)

            # ✅ Limit recipes to 5
            if "recipes" in data:
                data["recipes"] = data["recipes"][:5]

            return data

        except:
            return {
                "recipes": [],
                "message": "I focus on cooking. Tell me ingredients like egg, chicken, rice.",
                "question": "What ingredients do you have?",
                "options": ["Egg", "Chicken", "Vegetarian"]
            }

    except Exception as e:
        return {
            "recipes": [],
            "message": "Server error. Try again.",
            "question": "What do you want to cook?",
            "options": ["Quick meals", "Snacks", "Dinner"]
        }


# ✅ Railway PORT FIX
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
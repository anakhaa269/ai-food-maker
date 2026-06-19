# 🍳 AI Recipe Maker

An intelligent AI-powered recipe assistant that generates recipes based on user-provided ingredients.

---

## 🚀 Overview

AI Recipe Maker is a full-stack web application that allows users to enter ingredients or food preferences and receive structured recipes instantly. It uses a Large Language Model (LLM) to understand natural language input and generate meaningful cooking suggestions.

---

## ✨ Features

* 🧠 Understands natural language (e.g., "I have egg and rice")
* 🍽 Generates multiple recipes (up to 5)
* 📋 Structured output (ingredients + step-by-step instructions)
* 🎥 Provides YouTube tutorial links for recipes
* ⚡ Fast response using Groq API
* 💬 Chat-based user interface
* 🔁 Follow-up questions and suggestions

---

## 🛠 Tech Stack

### Frontend

* HTML
* CSS
* JavaScript

### Backend

* FastAPI (Python)
* Groq API (LLM - LLaMA 3)

### Deployment

* Frontend: GitHub Pages
* Backend: Railway

---

## 🧠 How It Works

1. User enters ingredients or a query
2. Frontend sends request to FastAPI backend
3. Backend calls Groq LLM model
4. LLM generates structured recipe data
5. Response is displayed in UI with:

   * Recipe cards
   * Ingredients
   * Steps
   * YouTube links

---

## ⚙️ Installation (Local Setup)

### 1. Clone the repository

```
git clone https://github.com/your-username/ai-food-maker.git
cd ai-food-maker
```

---

### 2. Install dependencies

```
pip install fastapi uvicorn groq python-dotenv
```

---

### 3. Add API Key

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

### 4. Run backend

```
uvicorn main:app --reload
```

---

### 5. Run frontend

```
python -m http.server 5500
```

Open:

```
http://127.0.0.1:5500
```

---

## 🌐 Live Demo

Frontend:
https://anakhaa269.github.io/ai-food-maker/

Backend:
https://ai-food-maker-production.up.railway.app

---

## ⚠️ Limitations

* Depends on LLM response quality
* Requires internet connection
* API key required for backend

---

## 📌 Future Improvements

* Save favorite recipes
* User authentication
* Image generation for recipes
* Voice input support
* Personalized recommendations

---

## 👩‍💻 Author

Anakha
B.Tech Computer Science Engineering

---

## ⭐ Conclusion

This project demonstrates how modern AI (LLMs) can be integrated into real-world applications to solve everyday problems like cooking assistance.

import os
import cohere
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import traceback

from fastapi.middleware.cors import CORSMiddleware



# Load API Key from .env file
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    raise ValueError("Cohere API Key not found. Please check your .env file.")

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Cohere Client
co = cohere.Client(COHERE_API_KEY)

# Request Model
class ChatRequest(BaseModel):
    message: str

# Root Endpoint
@app.get("/")
async def root():
    return {"message": "Chatbot API is running"}

# Chat Endpoint
@app.post("/chat/")
async def chat(request: ChatRequest):
    try:
        # 🎯 Personalized prompt including "Ajwan"
        personalized_prompt = f"""
        Your name is **Azwan**, and you are an AI assistant designed by Yousuf Sinha.
        You should provide clear, precise and insightful responses. 
        If Yousuf asks about AI, chatbot development, business, or software engineering, give expert advice. 
        Keep your tone friendly yet professional.

        User: {request.message}
        Azwan:
        """

        # Send request to Cohere API
        response = co.generate(
            model="command",
            prompt=personalized_prompt,  # 👈 Injecting our custom prompt
            max_tokens=150  # Adjust for longer responses
        )

        # Extract response text
        if response and response.generations:
            bot_reply = response.generations[0].text.strip()
            return {"response": bot_reply}

        raise HTTPException(status_code=500, detail="Invalid response from Cohere")

    except Exception as e:
        print(traceback.format_exc())  # Logs the full error
        raise HTTPException(status_code=500, detail=str(e))

import os
import cohere
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import traceback
from fastapi.middleware.cors import CORSMiddleware  # Keep only this import




# Load API Key from .env file
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    raise ValueError("Cohere API Key not found. Please check your .env file.")

# Initialize FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allowed frontend domains
origins = [
    "http://localhost:5173",  # Local frontend
    "https://azwanfrontend-8rf2pb5da-yousuf-sinhas-projects.vercel.app",  # Deployed frontend
    "https://azwan-frontend.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow only these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
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
        Your name is **Azwan**, and you are an AI assistant developed by Yousuf Sinha.
        You should provide clear, precise and insightful responses. 
        If anyone asks about anything, give precised answer. 
        Keep your tone friendly yet professional. Do not make answers long.

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
        if response and hasattr(response, "generations") and response.generations:
            bot_reply = response.generations[0].text.strip()
            return {"response": bot_reply}
        else:
            return {"response": "I'm sorry, but I couldn't generate a response."}

  
    except cohere.error.CohereAPIError as e:
        raise HTTPException(status_code=500, detail=f"Cohere API Error: {str(e)}")
    except Exception as e:
        print(traceback.format_exc())  # Logs error in backend
        raise HTTPException(status_code=500, detail="Something went wrong. Please try again.")
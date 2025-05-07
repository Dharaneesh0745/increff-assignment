from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from chatbot import chatbot

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],  # allow all methods
    allow_headers=["*"],
)

MONGO_URI = "mongodb+srv://dharaneesh5577:Dhoni_007@cluster0.rgafzk3.mongodb.net/products"
client = MongoClient(MONGO_URI)
db = client["products"]

def serialize_objectid(item):
    if isinstance(item, dict):
        for key, value in item.items():
            if isinstance(value, ObjectId):
                item[key] = str(value)
            elif isinstance(value, dict):
                item[key] = serialize_objectid(value)
    return item

@app.get("/")
async def index():
    return {"message": "Hello from FastAPI"}

# define pydantic model for POST body
class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(request: ChatRequest):
    response = chatbot(request.message)
    return {"reply": response}

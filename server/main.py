from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
from chatbot import chatbot

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
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

@app.get("/chat")
async def chat(query: str = Query(..., description="User query")):
    response = chatbot(query)
    return {"response": response}

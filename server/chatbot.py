import google.generativeai as genai
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from pymongo import MongoClient
from typing import List, Dict

load_dotenv()

genai.configure(api_key="AIzaSyCilfMz7c33yA4TBhaLrKO4OpLwrAauiDs")
model = genai.GenerativeModel("gemini-1.5-flash")

sentence_model = SentenceTransformer('all-MiniLM-L6-v2')

client = MongoClient("mongodb+srv://dharaneesh5577:Dhoni_007@cluster0.rgafzk3.mongodb.net/products")
db = client["products"]
collection = db["product_data"]

def fetch_product_data() -> List[Dict[str, str]]:
    product_data = []
    for product in collection.find():
        product_text = f"Product Name: {product['name']}. Category: {product['category']}. " \
                       f"Description: {product['description']}. Specifications: {', '.join([f'{key}: {value}' for key, value in product['specifications'].items()])}. " \
                       f"Price: {product['price']}. Ratings: Average {product['ratings']['average']}, Count {product['ratings']['count']}."
        product_data.append({"id": product["_id"], "text": product_text})
    return product_data

# FAISS index
def embed_documents(docs: List[Dict[str, str]]) -> faiss.Index:
    embeddings = sentence_model.encode([doc["text"] for doc in docs])
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    return index

# retrieve relevant product chunks
def retrieve_relevant_chunks(query: str, index: faiss.Index, k: int = 2) -> List[Dict[str, str]]:
    query_embedding = sentence_model.encode([query])
    _, I = index.search(np.array(query_embedding), k)
    return [docs[i] for i in I[0]]

#gen res
def generate_response(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text

docs = fetch_product_data()
index = embed_documents(docs)

def chatbot(query: str) -> str:
    relevant_chunks = retrieve_relevant_chunks(query, index)

    if not relevant_chunks:
        return "Irrelevant content. You can ask me about electronic gadgets like smartphones, laptops, or accessories."

    context = " ".join([chunk["text"] for chunk in relevant_chunks])
    prompt = f"User query: {query}\nContext: {context}\nProvide a detailed answer based on the context."
    return generate_response(prompt)

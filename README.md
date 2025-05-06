# Increff Assignment: Electronic Gadget Chatbot

This is a AI Custom Chatbot that provides a chatbot to answer user queries about electronic gadgets (smartphones, laptops, accessories) using a Retrieval-Augmented Generation (RAG) pipeline with FAISS and Gemini 1.5 Flash.

---

## 📦 Tech Stack

- **🧠 Large Language Model:** Gemini 1.5 Flash API
- **🗃️ Vector Database:** MongoDB Atlas
- **⚙️ Vector Search:** FAISS
- **🐍 Backend Framework:** FastAPI (Python)
- **⚛️ Frontend Framework:** React (Vite)

---

## 🚀 Getting Started

Follow these steps to set up and run the application locally.

### 🖥️ Backend Setup (FastAPI)

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/increff-assignment.git](https://github.com/Dharaneesh0745/increff-assignment.git)
   cd increff-assignment/server
   ```

2. **Create a virtual environment**
   ```
   python -m venv chatbot-env
   ```
   
3. **Activate the environment**
   # for windows
   ```
   chatbot-env\Scripts\activate
   ```

   # for linux\macOS
   ```
   source chatbot-env/bin/activate
   ```

5. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

6. **Run the FastAPI server on port 5000**
   ```
   uvicorn main:app --host 0.0.0.0 --port 5000 --reload
   ```

7. **Frontend**
   ```
   cd ../client
   ```

8. **Install dependencies**
   ```
   npm install
   ```

9. **Run the development server**
   ```
   npm run dev
   ```

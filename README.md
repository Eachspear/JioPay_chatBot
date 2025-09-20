This project is a fully functional, production-grade Retrieval-Augmented Generation (RAG) chatbot designed to automate customer support for JioPay. It uses a knowledge base created from the official JioPay website to provide accurate and contextually relevant answers to user queries.

The application features a modern backend built with FastAPI and LangChain, and a responsive frontend developed with React and Vite.

✨ Features
Interactive Chat Interface: A clean and intuitive UI for seamless user interaction.

Retrieval-Augmented Generation: Provides answers grounded in a curated knowledge base, minimizing hallucinations.

Automated Data Pipeline: Scripts to scrape public data and build a searchable vector index.

Modern Tech Stack: Utilizes powerful open-source models and libraries for state-of-the-art performance.

📸 Screenshots
Here's a look at the chatbot in action:

The main chat interface where users can ask questions.

An example conversation showing the chatbot's ability to answer follow-up questions.

🛠️ Tech Stack
Backend
Framework: FastAPI

RAG Orchestration: LangChain (using LCEL)

Vector Database: FAISS (Facebook AI Similarity Search)

Embedding Model: BAAI/bge-small-en-v1.5 (via Sentence-Transformers)

LLM: mistralai/Mistral-7B-Instruct-v0.2 (via HuggingFace Hub)

Web Scraping: BeautifulSoup4 & Requests

Data Validation: Pydantic

Frontend
Framework: React

Build Tool: Vite

Styling: Tailwind CSS

API Client: Axios

🚀 Getting Started
Follow these instructions to set up and run the project on your local machine.

Prerequisites
Git

Python 3.9+

Node.js and npm (or yarn)

1. Clone the Repository
Bash

git clone https://github.com/Eachspear/JioPay_chatBot.git
cd JioPay_chatBot
2. Set Up Environment Variables
You'll need a Hugging Face API token to access the Mistral-7B model.

Navigate to the backend directory.

Create a .env file by copying the example file:

Bash

cp .env.example .env
Open the .env file and add your Hugging Face API token:

HUGGINGFACEHUB_API_TOKEN="hf_YourTokenHere"
3. Backend Setup
Navigate to the backend directory:

Bash

cd backend
Create and activate a virtual environment:

Bash

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
Install dependencies:

Bash

pip install -r requirements.txt
4. Build the Knowledge Base
Before running the backend server, you must first create the vector index.

Run the scraper script to collect data from the JioPay website:

Bash

python scrapper.py
This will create a jiopay_data.txt file.

Run the ingestion script to build the FAISS index:

Bash

python ingest.py
This will create a faiss_index folder containing the vector store.

5. Run the Backend Server
Now that the index is built, you can start the FastAPI server.

Bash

uvicorn main:app --reload
The backend will be running at http://localhost:8000.

6. Frontend Setup
Open a new terminal and navigate to the frontend directory:

Bash

cd frontend
Install dependencies:

Bash

npm install
Run the frontend development server:

Bash

npm run dev
The frontend will be accessible at http://localhost:5173.

Usage
Once both the backend and frontend servers are running, open your web browser and navigate to http://localhost:5173. You can now start asking the JioPay Assistant questions!

📂 Project Structure
.
├── backend/
│   ├── faiss_index/      # Stores the generated FAISS vector index
│   ├── ingest.py         # Script to build the vector index from scraped data
│   ├── main.py           # FastAPI application and RAG chain logic
│   ├── scrapper.py       # Scrapes data from JioPay website
│   ├── requirements.txt  # Backend dependencies
│   └── .env.example      # Environment variable template
└── frontend/
    ├── src/
    │   └── App.jsx       # Main React component for the UI
    └── package.json      # Frontend dependencies
☁️ Deployment
Frontend: The React application is deployed on Vercel.

Backend: The FastAPI backend is fully functional but could not be deployed on Render's free tier. This is due to the high memory requirements of the BAAI/bge-small-en-v1.5 embedding model, which exceeded the RAM limitations of the free service plan. The application runs successfully in a local environment or on a cloud service with sufficient memory.

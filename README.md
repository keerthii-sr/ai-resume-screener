📄 AI Resume Screening Agent

An AI-powered Streamlit application that analyzes multiple resumes, compares them with a Job Description (JD), and ranks candidates based on match percentage using Google Gemini.

✨ Features

Upload multiple PDFs

Extract text using PyPDF2

Analyze resumes using Gemini API

Match percentage + HIRE/AVERAGE/REJECT verdict

Rank candidates by match score

Clean, simple UI layout

🛠️ Setup & Installation

1️⃣ Prerequisites

Python 3.8+

Google Gemini API Key

2️⃣ Add Your Gemini API Key

Create a .env file:

GEMINI_API_KEY="YOUR_API_KEY_HERE"

3️⃣ Install Dependencies

Create a requirements.txt:

streamlit==1.32.0
PyPDF2
python-dotenv==1.0.1
google-genai


Then install:

pip install -r requirements.txt

4️⃣ Run the Application
streamlit run app.py


App will open at:

http://localhost:8501

⚙️ How to Use

Paste Job Description in the text area

Upload one or more PDF resumes

Click Analyze
View:
Ranking
Match %
Gemini-generated summary
Skill gaps
Verdict
Suggestions

🧩 Tech Stack
Component	Used
Framework	Streamlit
Language	Python
AI Model	Google Gemini
PDF Parsing	PyPDF2
Config	dotenv

📁 Project Structure
├── app.py
├── README.md
├── requirements.txt
├── .env

📌 Notes

Do NOT upload your .env to GitHub.

Only PDF resumes supported.

Works best with text-based PDFs (not scans).
📄 AI Resume Screening Agent

An intelligent resume-screening system built with Streamlit and powered by Google Gemini.
It analyzes multiple candidate resumes, compares them against a Job Description (JD), generates insights, ranks candidates by relevance, and produces hiring recommendations.

✨ Features

Upload multiple PDF resumes at once

Extract resume text using PyPDF2

Intelligent comparison with JD using Google Gemini

Generates:
Match percentage
Summary of candidate
Strengths & weaknesses
Skill gaps
Verdict (HIRE / AVERAGE / REJECT)
Ranks candidates from best to worst
Clean UI built with Streamlit

⚙️ Limitations

Only supports PDF files

Works best with text-based PDFs (non-scanned)

Relies on API stability and internet connectivity

Output quality depends on JD clarity

🧩 Tech Stack
Component	Used
Frontend	Streamlit
Backend	Python
AI Model	Google Gemini
PDF Parsing	PyPDF2
Hosting	GitHub + Streamlit Cloud
Config	python-dotenv

APIs Used

Google Gemini API — Used for analyzing resumes, comparing them with the Job Description, generating summaries, skill gaps, match percentages, and hiring recommendations.


🚀 Setup & Installation
1️⃣ Clone the Repository
git clone https://github.com/keerthii-sr/ai-resume-screener
cd ai-resume-screener

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Add Your Google Gemini API Key

Create a .env file:

GEMINI_API_KEY="YOUR_API_KEY_HERE"

4️⃣ Run the application
streamlit run app.py


App opens at:
http://localhost:8501

🎯 How to Use

Paste Job Description

Upload one or more PDF resumes

Click Analyze Resumes
View:
Ranking
Match %
AI-generated summary
Skill gaps
Hiring recommendation

🚧 Potential Improvements

Support for scanned PDFs (OCR using Tesseract)

Support for multiple file formats (DOCX, TXT)

Advanced analytics dashboard

Downloadable report for each candidate

ATS keyword extraction

Cloud database for storing history


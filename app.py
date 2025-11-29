import streamlit as st
from google import genai
from google.genai.types import Part
import PyPDF2
import io
import re

# ==================================
# 💡 WIDE LAYOUT CHANGE: Set page config to 'wide' to expand content area
st.set_page_config(layout="wide")
# ==================================

# ====== CUSTOM THEME & STYLING ======
st.markdown("""
    <style>
        /* Global clean theme and Times New Roman font for everything */
        body, .stApp, .stApp * {
            /* 🎨 BACKGROUND: SOFT GRAY APP BACKGROUND */
            background-color: #F5F5F5 !important; 
            color: black !important;
            font-family: 'Times New Roman', serif !important;
            /* FONT SIZE BASE for body text (20px) */
            font-size: 20px !important; 
        }
        
        /* 💡 ADJUSTED FIX: Custom class for the Main Header (60px) */
        .main-title {
            font-size: 60px !important; /* REDUCED SIZE */
            font-weight: bold;
            color: black !important;
            margin-bottom: 5px;
        }

        /* 💡 ADJUSTED FIX: Custom class for the Sub Header (40px) */
        .sub-title {
            font-size: 40px !important; /* REDUCED SIZE */
            color: #333333 !important;
            margin-top: 0px;
            margin-bottom: 30px;
        }
        
        /* Ensure specific elements inherit text color/font */
        p, label, input, textarea, div.st-emotion-cache-1ft07to {
            color: black !important;
            font-family: 'Times New Roman', serif !important;
            font-size: 20px !important; /* Force body text to 20px */
        }

        /* Other headers remain large but smaller than the top two lines */
        h2 { font-size: 2.0em !important; } 
        h3 { font-size: 1.5em !important; } 
        h4 { font-size: 1.2em !important; color: black !important; }

        /* 1. FILE UPLOADER FIX: Outer Container Style (Solid Border) */
        .stFileUploader {
            /* FIX: Match JD Text Area Border/Background */
            background-color: white !important; /* Ensure main box is white */
            border: 1px solid #c4c4c4; /* Solid border to match JD box */
            border-radius: 6px;
            padding: 0px; 
            height: 190px; 
            overflow: hidden; 
        }

        /* 2. FILE UPLOADER FIX: Inner Element Style (Remove Dashed Line) */
        .stFileUploader > div:first-child > div:first-child { 
            /* Remove dashed border to make it look like a seamless box */
            border: none !important; 
            background-color: white !important; /* Force inner background white */
            border-radius: 6px;
            padding: 20px;
            text-align: center;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
        
        /* 3. Text areas (JD Box) - Targeting the container around the textarea */
        div[data-testid="stTextarea"] > div:first-child {
             /* Ensure the JD container visually matches the File Uploader outer box */
             background-color: white !important;
             border: 1px solid #c4c4c4 !important; 
             border-radius: 6px;
        }
        
        /* Text area content (Text Box) */
        .stTextArea textarea {
            background-color: white !important; /* Keep text box pure white */
            color: black !important;
            border-radius: 6px !important;
            border: none !important; /* Border is now on the container above */
            font-family: 'Times New Roman', serif !important;
            padding: 10px; /* Add padding for better spacing */
            resize: none !important; /* Prevent user resize */
            font-size: 20px !important; /* Ensure text inside text area is large */
        }
        
        /* Result area */
        .result-box {
            background-color: #f9f9f9 !important; 
            padding: 20px 30px;
            margin-top: 20px;
            border-radius: 12px;
            border: 1px solid #cfcfcf;
            font-size: 20px; /* Result text size matched to base */
            font-family: 'Times New Roman', serif !important;
        }

        /* Buttons (Soft Black/Deep Charcoal) */
        .stButton>button {
            background-color: #333333 !important; /* Deep Charcoal/Soft Black */
            color: white !important;
            border-radius: 6px !important;
            border: none !important;
            padding: 8px 20px;
            font-family: 'Times New Roman', serif !important;
            margin-top: 20px;
            transition: background-color 0.2s;
            font-size: 1em !important; /* Keep button text proportional */
        }
        .stButton>button:hover {
            background-color: #555555 !important; /* Slightly lighter Charcoal on hover */
        }
    </style>
""", unsafe_allow_html=True)

# ----------------------------
# GOOGLE GEMINI CONFIG
# ----------------------------
# !! IMPORTANT: Replace "AIzaSyAizA6rTV6tKr6uBT_-hFHb-8vSVdS8888" with your actual Gemini API key. 
client = genai.Client(api_key="AIzaSyAizA6rTV6tKr6uBT_-hFHb-8vSVdS8888")

# ----------------------------
# FIXED FUNCTION: Extract text from MULTIPLE PDFs
# ----------------------------
def extract_text_from_pdf(uploaded_files):
    all_text = ""

    for uploaded_file in uploaded_files:
        pdf_bytes = uploaded_file.read()
        pdf_stream = io.BytesIO(pdf_bytes)

        pdf_reader = PyPDF2.PdfReader(pdf_stream)

        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                all_text += content + "\n"

    return all_text


# -----------------------------------------------------
# AI FUNCTION: Analyze Resume (JD ALIGNMENT FOCUS)
# -----------------------------------------------------
def analyze_resume(resume_text, jd_text):
    prompt = f"""
    You are a Resume Screener focused on immediate Job Description (JD) matching.
    Analyze the resume strictly based on the provided JD context.
    
    Give:
    - **Skills Overview**: Primary technical skills present.
    - **Project Relevance**: How the candidate's existing projects demonstrate value or transferrable skills for this JD.
    - **JD Alignment Actions**: Specific, immediate actions the candidate could take (e.g., specific courses, certifications, project tweaks, better resume wording) to close the observed skill gaps and increase their match percentage for THIS specific JD. Frame this as a pathway to 'somehow match' the role.
    
    Provide output in a clear, professional format.

    Job Description Context:
    {jd_text}
    
    Resume Content:
    {resume_text}
    """

    result = client.models.generate_content(
        model="models/gemini-2.0-flash",
        contents=[{"parts": [{"text": prompt}]}]
    )

    return result.text


# -----------------------------------------------------
# AI FUNCTION: Match Resume to Job Description
# -----------------------------------------------------
def match_resume_to_jd(resume_text, jd_text):
    prompt = f"""
    Compare the following resume with the given Job Description (JD).

    JD:
    {jd_text}

    Resume:
    {resume_text}

    Give:
    - Match Percentage (0 to 100)
    - Key Matching Skills
    - Missing Skills
    - Short verdict (HIRE / AVERAGE / REJECT)

    Return in clean bullet points.
    """

    result = client.models.generate_content(
        model="models/gemini-2.0-flash",
        contents=[{"parts": [{"text": prompt}]}]
    )

    return result.text

# -----------------------------------------------------
# AI FUNCTION 3: Concise Summary Generator 
# -----------------------------------------------------
def generate_concise_summary(match_result, detailed_analysis, filename):
    # Condense the key points from the two analyses into one block
    combined_prompt = f"""
    Combine the following Match Result and JD-Focused Analysis into ONE concise, clear, and professional summary suitable for a quick review by a Hiring Manager. 
    
    Focus only on: 
    1. Match Percentage and Verdict.
    2. The 3 strongest matching skills (from Match Result).
    3. The 2 most critical missing skills/gaps (from Match Result).
    4. **JD ALIGNMENT ACTIONS**: Rephrase the actions as **objective notes for the hiring team**, explaining that if the candidate pursues these specific actions, their profile will be a better fit for this role. Do NOT address the candidate directly.

    Candidate File: {filename}
    
    Match Result (Skills, %):
    {match_result}

    JD-Focused Analysis (Alignment Actions):
    {detailed_analysis}
    
    Format the output using clear headings like: **VERDICT**, **KEY MATCHES**, **CRITICAL GAPS**, **JD ALIGNMENT ACTIONS**.
    """
    
    result = client.models.generate_content(
        model="models/gemini-2.0-flash",
        contents=[{"parts": [{"text": combined_prompt}]}]
    )
    return result.text

# -----------------------------------------------------
# STREAMLIT UI (MATCHING IMAGE LAYOUT)
# -----------------------------------------------------

# Main Title and Subtitle 
# 🚀 FINAL FIX: Using custom classes with reduced font sizing
st.markdown("<div class='main-title'>AI Resume Screening Agent</div>", unsafe_allow_html=True) 
st.markdown("<div class='sub-title'>Rank resumes based on job descriptions</div>", unsafe_allow_html=True) 

# Container for the side-by-side JD and Upload sections
col1, col2 = st.columns(2)

# -------- LEFT SIDE: MULTIPLE RESUME UPLOAD ----------
with col1:
    st.markdown("<h4>Upload your resume (PDF)</h4>", unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Drag and drop file here\nLimit 200MB per file • PDF", 
        type=["pdf"], 
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

# -------- RIGHT SIDE: JOB DESCRIPTION ----------
with col2:
    st.markdown("<h4>Enter Job Description:</h4>", unsafe_allow_html=True)
    
    jd_text = st.text_area(
        "Paste the job description here...", 
        height=190, 
        key="jd", 
        label_visibility="collapsed",
        placeholder="Paste the job description here..."
    )
    
st.markdown("---") # Separator

# -----------------------------------------------------
# PROCESSING AND RESULT DISPLAY (CONCISE ANALYSIS)
# -----------------------------------------------------
if st.button("Analyze Match"):
    if jd_text and uploaded_files:
        results = []
        
        # --- Helper function to extract percentage ---
        def extract_percentage(text):
            match = re.search(r'(\d+)%', text)
            if match:
                return int(match.group(1))
            return 0
        
        # ---------- Step 1: Process and Analyze All Resumes ----------
        for uploaded_file in uploaded_files:
            with st.spinner(f"Analyzing {uploaded_file.name}..."):
                resume_text = extract_text_from_pdf([uploaded_file])
                
                # Pass JD to the analysis function
                analysis = analyze_resume(resume_text, jd_text) 
                
                match_result = match_resume_to_jd(resume_text, jd_text)

                results.append({
                    "filename": uploaded_file.name,
                    "resume_text": resume_text,
                    "analysis": analysis,
                    "match": match_result
                })

        # ---------- Step 2: SORT BY MATCH % ----------
        results = sorted(results, key=lambda x: extract_percentage(x["match"]), reverse=True)

        # -----------------------------------------------------------------
        # ---------- Part 1: DISPLAY TOPPERS LIST (Concise Summary) ----------
        # -----------------------------------------------------------------
        st.subheader("🏆 Resume Shortlist: Top Matches")
        
        toppers_list_markdown = ""
        rank = 1
        
        for res in results:
            percentage = extract_percentage(res["match"])
            toppers_list_markdown += f"**🥇 Rank {rank}:** {res['filename']} — **{percentage}%** Match\n\n"
            rank += 1
        
        st.markdown(toppers_list_markdown)
        st.markdown("---") 

        # -----------------------------------------------------------------
        # ---------- Part 2: DISPLAY CONCISE DETAILED ANALYSIS (Ranked) ----------
        # -----------------------------------------------------------------
        st.subheader("📄 Detailed Candidate Review")
        
        rank = 1
        for res in results:
            # Generate the new, concise summary block
            concise_summary = generate_concise_summary(res["match"], res["analysis"], res["filename"])
            
            # Display Rank and File Name
            st.markdown(f"### 🥇 Rank {rank}: **{res['filename']}**")
            
            # Display the combined, concise summary (No surrounding custom box)
            st.write(concise_summary.strip())
            
            rank += 1
            st.markdown("---") # Separator between ranked candidates

    else:
        st.warning("Please upload resumes AND paste the job description.")
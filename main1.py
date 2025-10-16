import streamlit as st
import google.generativeai
import os
import PyPDF2
from dotenv import load_dotenv
import json
import io  # <-- added

load_dotenv(override=True)

google.generativeai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
st.title("Applicant Tracking System")
st.markdown("Enhance your resume for interview calls; assess its strengths and weaknesses against the job description and receive tailored recommendations for improvement.")
st.sidebar.title("Profile of the Developer") 

st.sidebar.subheader("Name: Lawrence Owusu")
st.sidebar.subheader("Email: lawrenceowusu0541@gmail.com")
st.sidebar.subheader("GenAI engineer, Data Scientist, Machine Learning Engineer, Data Analyst")
st.sidebar.subheader("Credentials: BSc, M.S., M.S., PhD candidate, 6X AWS certified, Certified ScrumMaster, SQL Developer.")
st.sidebar.subheader("Technical Skills: Python programming, Pytorch, Keras and Tensorflow, FastAPI, Spark, SQL, AWS, Airflow, Github Actions, Kubernetes, Docker, Git, AWS, Streamlit, Jenkins.")


def LLM_repsonse(input):
    model = google.generativeai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(input)
    return response.text

def Resume_text(uploaded_file):
    if uploaded_file is None:
        return ""
    data = uploaded_file.read()
    buffer = io.BytesIO(data)
    buffer.seek(0)

    reader = PyPDF2.PdfReader(buffer)
    text = ""
    for page in range(len(reader.pages)):
        page_obj = reader.pages[page]
        text += str(page_obj.extract_text())
    return text

job_description = st.text_area("Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="PDF format *")

# Move text extraction to after button click and file check
submit = st.button("Submit your uploaded resume")

if submit:
    if uploaded_file is None:
        st.error("Please upload a PDF resume.")
    else:
        text1 = Resume_text(uploaded_file)

        
        input_prompt = f"""
Act like an experienced ATS across IT/engineering roles. Evaluate the uploaded resume against the job description.
Return a concise evaluation including Job Description match %, missing keywords, strengths, weaknesses, profile summary, Chance of interview call %, and recommendations.

resume:{text1}
description:{job_description}

Return JSON with keys:
{{"Job Description Match":"%","MissingKeywords":[],"Strength of Resume":[],"Weakness of Resume":[],"Profile Summary":"","Chance of interview call":"%","Recommendations":""}}
"""

        response = LLM_repsonse(input_prompt)
        st.subheader("ATS Evaluation")
        st.write(response)

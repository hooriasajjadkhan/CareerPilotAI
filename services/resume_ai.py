import fitz
from groq import Groq
from config import Config

client = Groq(api_key=Config.GROQ_API_KEY)


def extract_text(pdf_path):

    text = ""

    document = fitz.open(pdf_path)

    for page in document:
        text += page.get_text()

    document.close()

    return text


def analyze_resume(pdf_path):

    resume_text = extract_text(pdf_path)

    prompt = f"""
You are an expert ATS Resume Reviewer.

Analyze this resume professionally.

Return your answer in the following format:

Overall ATS Score (out of 100)

Summary

Strengths

Weaknesses

Missing Skills

Suggestions for Improvement

Resume:

{resume_text}
"""

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],

        temperature=0.4

    )

    return response.choices[0].message.content
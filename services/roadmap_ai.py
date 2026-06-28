from groq import Groq
from config import Config

client = Groq(api_key=Config.GROQ_API_KEY)


def generate_roadmap(career, skills, level):

    prompt = f"""
You are an expert career mentor.

Create a personalized roadmap.

Career Goal:
{career}

Current Skills:
{skills}

Experience:
{level}

Return your answer using these headings:

1. Career Summary

2. Skills to Learn

3. Projects to Build

4. Certifications

5. Interview Preparation

6. Estimated Timeline

Make the roadmap practical and beginner-friendly.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.5
    )

    return response.choices[0].message.content
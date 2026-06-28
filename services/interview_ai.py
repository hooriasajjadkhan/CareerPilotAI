import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are CareerPilot AI.

You are a professional HR interviewer.

Rules:

• Ask only ONE interview question at a time.
• Keep answers under 80 words.
• Be encouraging.
• Wait for the candidate's response.
• Ask realistic technical and HR interview questions.
• After 8 questions, end the interview and provide:
  - Overall Score (/100)
  - Strengths
  - Weaknesses
  - Suggestions
"""

conversation = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

def ask_ai(user_message):
    try:
        conversation.append({
            "role": "user",
            "content": user_message
        })

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation,
            temperature=0.7,
            max_tokens=500
        )

        reply = response.choices[0].message.content

        conversation.append({
            "role": "assistant",
            "content": reply
        })

        return reply

    except Exception as e:
        print("GROQ ERROR:", e)
        return f"Error: {e}"
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# class BasicAgent:

#     def ask(self, text):

#         res = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[{"role": "user", "content": text}]
#         )

#         return res.choices[0].message.content

class BasicAgent:
    def ask(self, text):
        return "AI is the simulation of human intelligence in machines."

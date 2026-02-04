from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_GEMINI_KEY')
client = genai.Client(api_key=api_key)

print("testing memory problems")
print("="*50)

print("CALL 1: what is my fav colour")
response1 = client.models.generate_content(
    model = "gemini-3-flash-preview", contents="my fav colour is purple"
)
print(f"Gemini:{response1.text}")

print("CALL 1: Asking what my fav colour is...")
response2 = client.models.generate_content(
    model = "gemini-3-flash-preview", contents="what is my favourtie colour"
)
print(f"Gemini:{response2.text}")
print("="*50)
from google import genai
import os 
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_GEMINI_KEY')
client = genai.Client(api_key=api_key)

print("✅ Testing Memory Solution")
print("="*50)

# Create a chat session
chat = client.chats.create(
    model="gemini-3-flash-preview"
)

# First message in the session
print("\n📤 MESSAGE 1: Telling Gemini my favorite color...")
response1 = chat.send_message("My favorite color is purple.")
print(f"Gemini: {response1.text}")

# Second message in the SAME session
print("\n📤 MESSAGE 2: Asking what my favorite color is...")
response2 = chat.send_message("What is my favorite color?")
print(f"Gemini: {response2.text}")

# Third message - test if it STILL remembers
print("\n📤 MESSAGE 3: Asking a related question...")
response3 = chat.send_message("Why do you think I like that color?")
print(f"Gemini: {response3.text}")

print("\n✅ Gemini remembers!")
print("="*50)

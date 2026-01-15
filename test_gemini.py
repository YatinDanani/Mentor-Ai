from google import genai 
import os 
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_GEMINI_KEY')
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model = "gemini-3-flash-preview", contents="what is my fav colour"
)
print("\n" + "="*100)
print("GEMINI'S RESPONSE:")
print("="*100)
print(response.text)
print("="*100)
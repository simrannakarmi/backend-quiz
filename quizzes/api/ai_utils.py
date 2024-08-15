import google.generativeai as genai
from django.conf import settings

# Configure the Gemini AI with the API key
genai.configure(api_key=settings.GEMINI_API_KEY)

# Initialize the Gemini AI model
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_quiz(description):
    # Use the model to generate a quiz based on the description
    response = model.generate(
        prompt=description,
        max_tokens=150  # Adjust the token limit as needed
    )
    
    # Extract the generated quiz content
    quiz_data = response['choices'][0]['text']
    
    return quiz_data


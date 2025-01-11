import google.generativeai as genai
from django.conf import settings
from google.api_core.exceptions import  InvalidArgument
import json
from quizzes.api.utils import save_quiz
genai.configure(api_key=settings.API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

def generate_quiz(description):
    """
    Generates a quiz based on the given description.

    Args:
    description (str): The description of the topic or concept to be quizified.
    """
    try:
        response = model.generate_content(
            f"Generate a quiz in Json format. Include a title and description for the quiz and the output should include fields like 'questions', 'options', and 'correct_answer' for the topic: {description}."
        )
        print(f"AI Response: {response.text}")
        
        # clean the response text
        response_text = response.text.strip()
        response_text = response_text.replace('\n', '').replace('\r', '')
        
        # removing the code block indicators
        if response_text.startswith('```') and response_text.endswith('```'):
            response_text = response_text[3:-3].strip()
            
        # if the response text starts with 'json', removing it
        if response_text.lower().startswith('json'):
            response_text = response_text[4:].strip()
            
        response_text = response_text.strip()
        
        try:    
            # parse the clean text as JSON
            quiz_data = json.loads(response_text)
            print(f"Quiz_Data: {quiz_data}")
        except json.JSONDecodeError as e:
            print("Failed to parse JSON. Falling back to  plain text handling.")
            quiz_data = {
                "error": "The AI response was not in the expected JSON format.",
                "response": response_text
            }               
        return quiz_data
    
    except InvalidArgument as e:
        print(f"API error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise
    
def handle_quiz(description):
    quiz_data = generate_quiz(description)
    
    if 'error' in quiz_data:
        print("Error in AI response:", quiz_data['response'])
        return None
    
    # save quiz data
    quiz_id = save_quiz(quiz_data)
    
    if quiz_id:
        print(f"Quiz saved successfully with ID: {quiz_id}")
        return quiz_id
    else:
        print("Failed to save quiz.")
        return None
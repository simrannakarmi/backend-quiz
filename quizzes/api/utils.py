from quizzes.models import Quiz, Question, Choice

def save_quiz(quiz_data):
    try:
        # quiz_info = quiz_data.get('quiz')
        title = quiz_data.get('title')
        description = quiz_data.get('description')
        print(f"Quiz_Info right now: {quiz_data}")
        
        quiz = Quiz.objects.create(title=title, description=description)
        
        for index, question_data in enumerate(quiz_data.get('questions', []), start=1):
            print(question_data)
            question_text = question_data.get('question')
            
            question = Question.objects.create(quiz=quiz, text=question_text, order=index)
            # options iteration
            for option_text in question_data.get('options', []):
                is_correct = option_text == question_data.get('correct_answer')
                
                Choice.objects.create(question=question, text=option_text, is_correct=is_correct)
                
        return quiz.id
    except Exception as e:
        print(f"Error saving quiz to the database: {e}")
        return None 
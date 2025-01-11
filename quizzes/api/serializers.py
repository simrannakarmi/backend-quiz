from rest_framework import serializers
from quizzes.models import Quiz, Question, Choice, UserResponse, QuizResult

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'question', 'text', 'is_correct']
        
        
class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text', 'order', 'choices']
        

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Quiz
        fields = "__all__"
        
    
class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserResponse
        fields = "__all__"
        
        

class QuizResultSerializer(serializers.ModelSerializer):
    quiz_title = serializers.CharField(source='quiz.title')
    questions = serializers.SerializerMethodField()
    class Meta:
        model = QuizResult
        fields = ['quiz_title', 'score', 'total', 'questions']
        
    def get_questions(self, obj):
        responses = UserResponse.objects.filter(user=obj.user, quiz=obj.quiz)
        question_data = []
        for response in responses:
            correct_choice = response.question.choices.filter(is_correct=True).first()
            question_data.append({
                'question_id': response.question.id,
                'question_text': response.question.text,
                'user_choice_text': response.choice.text,
                'correct_choice_text': correct_choice.text if correct_choice else None,
                'is_correct': response.choice == correct_choice
            })
        return question_data

# class QuizResultSerializer(serializers.ModelSerializer):
#     quiz_title = serializers.CharField(source='quiz.title')
#     questions = serializers.SerializerMethodField()

#     class Meta:
#         model = QuizResult
#         fields = ['quiz_title', 'score', 'total', 'questions']

    # def get_questions(self, obj):
    #     responses = UserResponse.objects.filter(user=obj.user, quiz=obj.quiz)
    #     return [
    #         {
    #             'id': response.question.id,
    #             'text': response.question.text,
    #             'user_choice_text': response.choice.text,
    #             'correct_choice_text': response.question.choices.filter(is_correct=True).first().text
    #         }
    #         for response in responses
    #     ]
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from .ai_utils import generate_quiz, handle_quiz
from quizzes.models import Quiz, Question, Choice, UserResponse, QuizResult
from .serializers import QuizSerializer, QuestionSerializer, ChoiceSerializer, UserResponseSerializer, QuizResultSerializer
from quizzes.api.permissions import IsAdminOrReadOnly

from django.views import View
from django.http import JsonResponse
# import json

class QuizResultView(generics.RetrieveAPIView):
    serializer_class = QuizResultSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'quiz_id'

    def get_queryset(self):
        user = self.request.user
        quiz_id = self.kwargs.get('quiz_id')
        return QuizResult.objects.filter(user=user, quiz_id=quiz_id)

    def get_object(self):
        queryset = self.get_queryset()
        return queryset.first()


class GenerateQuizView(APIView):
    def post(self, request):
        # data = json.loads(request.body)
            
        # description = data.get('description')
        description = request.data.get('description')
        title = request.data.get('title') 

        if not description:
            return Response({"error": "Description is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            quiz_id = handle_quiz(description)
            
            if quiz_id:
                return JsonResponse({'status': 'success', 'quiz_id': quiz_id})
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to generate or save the quiz.'})
            

            return JsonResponse({"quiz_id": quiz.id, "quiz_data": quiz_data}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    
class QuizDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]
    
    
class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]
    
    
class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]
    
    
class ChoiceListCreateView(generics.ListCreateAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]
    
    
class ChoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]
    
    
class UserResponseListCreateView(generics.ListCreateAPIView):
    queryset = UserResponse.objects.all()
    serializer_class = UserResponseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def create(self, request, *args, **kwargs):
        user = request.user
        responses = request.data.get('responses', [])
        
        for response in responses:
            question = Question.objects.get(id=response['question'])
            choice = Choice.objects.get(id=response['choice'])
            
            UserResponse.objects.create(user=user, question=question, choice=choice)
            
        return Response({"status": {"success", status.HTTP_201_CREATED}, "message": "Responses saved successfully"})
    
    
class UserResponseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserResponse.objects.all()
    serializer_class = UserResponseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    
    
class SubmitQuizView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        quiz_id = request.data.get('quiz_id')
        responses = request.data.get('responses')
        
        quiz = Quiz.objects.get(id=quiz_id)
        total_questions = quiz.questions.count()
        correct_answers = 0

        for response in responses:
            question = Question.objects.get(id=response['question'])
            choice = Choice.objects.get(id=response['choice'])
            is_correct = choice.is_correct
            
            UserResponse.objects.create(
                user=user,
                quiz=quiz,
                question=question,
                choice=choice
            )
            
            if is_correct:
                correct_answers += 1

        score = correct_answers
        result = QuizResult.objects.create(
            user=user,
            quiz=quiz,
            score=score,
            total=total_questions
        )

        return Response({'score': score, 'total': total_questions, 'result_id': result.id}, status=status.HTTP_201_CREATED)

# class QuizResultView(generics.RetrieveAPIView):
#     queryset = QuizResult.objects.all()
#     serializer_class = QuizResultSerializer
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [TokenAuthentication]
#     lookup_field = 'id'

#     def get(self, request, *args, **kwargs):
#         try:
#             result = self.get_object()
#             responses = UserResponse.objects.filter(user=result.user, quiz=result.quiz)
#             result_data = {
#                 'quiz_title': result.quiz.title,
#                 'score': result.score,
#                 'total': result.total,
#                 'questions': self.get_question_details(responses)
#             }
#             return Response(result_data)
#         except QuizResult.DoesNotExist:
#             return Response({'error': 'Result not found'}, status=status.HTTP_404_NOT_FOUND)

#     def get_question_details(self, responses):
#         question_details = []
#         for response in responses:
#             question = response.question
#             question_details.append({
#                 'question_id': question.id,
#                 'question_text': question.text,
#                 'user_choice': response.choice.text,
#                 'correct_choice': question.choices.filter(is_correct=True).first().text
#             })
#         return question_details
    
# class QuizResultView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, quiz_id, *args, **kwargs):
#         try:
#             quiz = get_object_or_404(Quiz, id=)
#             user = request.user
        
#             user_responses = UserResponse.objects.filter(user=user, question__quiz=quiz)
        

#             score, total_questions = self.calculate_score(user_responses, quiz)


#             result_data = {
#                 'quiz_id': quiz.id,
#                 'title': quiz.title,
#                 'score': score,
#                 'total_questions': total_questions,
#             }
#             return Response(result_data)
#         except Exception as e:
#             print(f"Error fetching quiz result: {str(e)}")
#             return Response({'error': 'An error occurred while fetching the quiz result.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def calculate_score(self, user_responses, quiz):
#         correct_answers = 0
#         total_questions = quiz.questions.count()

#         for response in user_responses:
#             question = response.question
#             if question.correct_choice == response.choice:
#                 correct_answers += 1

#         return correct_answers, total_questions

# class QuizResultView(generics.RetrieveAPIView):
#     permission_classes = [IsAuthenticated]
    
#     queryset = QuizResult.objects.all()
#     serializer_class = QuizResultSerializer
#     lookup_field = 'pk'
    
#     # def get(self, request, id):
#     #     try:
#     #         quiz = Quiz.objects.get(id=id)
#     #         questions = Question.objects.filter(quiz=quiz)
#     #         result = {
#     #             'score': quiz.score,  # Example method, implement according to your logic
#     #             'totalQuestions': questions.count(),
#     #             'questions': [
#     #                 {
#     #                     'id': question.id,
#     #                     'text': question.text,
#     #                     'choices': [
#     #                         {
#     #                             'id': choice.id,
#     #                             'text': choice.text,
#     #                             'is_correct': choice.is_correct
#     #                         }
#     #                         for choice in Choice.objects.filter(question=question)
#     #                     ]
#     #                 }
#     #                 for question in questions
#     #             ]
#     #         }
#     #         return JsonResponse(result)
#     #     except Quiz.DoesNotExist:
#     #         return JsonResponse({'error': 'Quiz not found'}, status=404)
        
#     def get_queryset(self):
#         user = self.request.user
#         return QuizResult.objects.filter(user=user)
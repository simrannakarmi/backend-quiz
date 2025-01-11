from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (QuizListCreateView, QuizDetailView,
                    QuestionListCreateView, QuestionDetailView,
                    ChoiceListCreateView, ChoiceDetailView,
                    UserResponseListCreateView, UserResponseDetailView,
                    GenerateQuizView, SubmitQuizView, QuizResultView)


urlpatterns = [
    path('quizzes/', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('quiz/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('choices/', ChoiceListCreateView.as_view(), name='choices-list-create'),
    path('choices/<int:pk>/', ChoiceDetailView.as_view(), name='choices-detail'),
    path('responses/', UserResponseListCreateView.as_view(), name='userresponses-list-create'),
    path('responses/<int:pk>/', UserResponseDetailView.as_view(), name='userresponses-detail'),
    
    # ai generate quiz path
    path('generate-quiz/', GenerateQuizView.as_view(), name='generate-quiz'),
    path('quiz-submit/<int:pk>/', SubmitQuizView.as_view(), name='submit-quiz'),
    path('quiz-result/<int:quiz_id>/', QuizResultView.as_view(), name='quiz-result'),
    
]
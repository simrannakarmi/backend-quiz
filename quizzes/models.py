from django.db import models
from django.contrib.auth.models import User

class Quiz(models.Model):
    title = models.CharField(max_length=255, verbose_name="Quiz Title")
    description = models.TextField(verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
        ordering = ["-created_at"]
    

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE, verbose_name="Related Quiz")
    text = models.CharField(max_length=1000, verbose_name="Question Text")
    order = models.IntegerField(verbose_name="Order")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    
    def  __str__(self):
        return f"{self.quiz.title} - Q{self.order}: {self.text[:50]}..."
    
    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ['quiz', 'order']
        constraints = [
            models.UniqueConstraint(fields=['quiz', 'order'], name='unique_question_order')
        ]
        
        
class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE, verbose_name="Related Question")
    text = models.CharField(max_length=600, verbose_name="Choice Text")
    is_correct = models.BooleanField(default=False, verbose_name="Is Correct")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated")
    
    def __str__(self):
        return f"Q{self.question.order}: {self.question.text[:50]}... - {self.text[:50]}"
    
    class Meta:
        verbose_name = "Choice"
        verbose_name_plural = "Choices"
        ordering = ['question', 'text']
        
    
class UserResponse(models.Model):
    user = models.ForeignKey(User, related_name="responses", on_delete=models.CASCADE, verbose_name="User")
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name="Quiz")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Question")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, verbose_name="Chosen Answer")
    play_count = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Response Time")
    
    def __str__(self):
        return f"{self.user.username}'s response to '{self.question.text[:50]}...'"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.play_count = 1  # Initialize the play count for a new response
        else:
            self.play_count += 1  # Increment the play count for an existing response
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "User Response"
        verbose_name_plural = "User Responses"
        ordering = ['-timestamp']
        # unique_together = ('user', 'question')
        # constraints = [
        #     models.UniqueConstraint(fields=['user', 'question'], name='unique_user_response')
        # ]
        
class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
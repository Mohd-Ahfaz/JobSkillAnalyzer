from django.db import models
from django.contrib.auth.models import User


class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

# User Profile Model (Auth & Onboarding data)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    target_role = models.CharField(max_length=100, default="Full Stack Developer")
    experience_level = models.CharField(max_length=50, default="Student / Fresher")
    primary_skills = models.CharField(max_length=255, default="Python, Django, MySQL")
    skills = models.TextField(blank=True, null=True, help_text="Detailed skills for matching")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Technical Test Quiz Question Model (Members 3 & 4)
class QuizQuestion(models.Model):
    target_role = models.CharField(max_length=100, default="Software Engineer")
    question_text = models.CharField(max_length=255)
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100)
    option_d = models.CharField(max_length=100)
    correct_option = models.CharField(max_length=1)

    def __str__(self):
        return f"[{self.target_role}] {self.question_text}"

# Quiz Result Model (Members 3 & 4)
class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField(default=4)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Score: {self.score}/{self.total_questions}"
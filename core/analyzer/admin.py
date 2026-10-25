from django.contrib import admin
from .models import UserProfile, QuizQuestion, QuizResult

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'target_role', 'experience_level', 'updated_at')
    search_fields = ('user__username', 'target_role')

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ('target_role', 'question_text', 'correct_option')
    list_filter = ('target_role',)

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'total_questions', 'submitted_at')
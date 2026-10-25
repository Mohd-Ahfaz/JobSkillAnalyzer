from django.urls import path
from . import views

urlpatterns = [
    # Auth & Onboarding Routes (Member 1)
    path('', views.login_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('onboarding/', views.onboarding_view, name='onboarding'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Core Analyzer & Quiz Routes (Members 3 & 4)
    path('update-skills/', views.update_skills, name='update_skills'),
    path('quiz/', views.take_quiz, name='take_quiz'),
    path('report/', views.report_view, name='report'),
]
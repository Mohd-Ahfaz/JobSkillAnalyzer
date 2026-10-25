from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_job, name='upload_job'),
    path('so/', views.job_list, name='job_list'),
]
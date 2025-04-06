from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/keywords/', views.get_keywords_by_category, name='get_keywords'),
    path('api/trending/', views.get_trending_topics, name='trending_topics'),
    path('api/generate-prompts/', views.generate_prompts, name='generate_prompts'),
    path('api/generate-question-prompts/', views.generate_question_prompts, name='generate_question_prompts'),
] 
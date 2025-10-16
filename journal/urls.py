from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),  # Home page
    path('add/', views.add_mood, name = 'add-mood'), # Add Mood page
    path('list/', views.mood_list, name='mood-list'),  # View all moods

]

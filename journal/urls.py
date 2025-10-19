from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

# for api 
from rest_framework import routers
from .views import home, add_mood, mood_list
from .views_api import MoodEntryViewSet

router = routers.DefaultRouter()
router.register(r'moods', MoodEntryViewSet)

urlpatterns = [
    path('', views.home, name = 'home'),  # Home page
    path('add/', views.add_mood, name = 'add-mood'), # Add Mood page
    path('list/', views.mood_list, name='mood-list'),  # View all moods
    
    path('signup/', views.signup, name='signup'), # Signup 
    
    # Login and Logout
    
    path('login/', auth_views.LoginView.as_view(template_name='journal/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # API URLS
    path('api/', include(router.urls)),

    

]

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class MoodEntry(models.Model):
    MOOD_CHOICES = [
        ('Happy', 'Happy'),
        ('Sad', 'Sad'),
        ('Tired', 'Tired'),
        ('Excited', 'Excited'),
        ('Calm', 'Calm'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES)
    note = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.mood} on {self.date.strftime('%Y-%m-%d')}"



# For recording the Mood
class Mood(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

# For recording the own quotes

class Quote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE )
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE)
    text = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.mood} : {self.text[:50]}"
    
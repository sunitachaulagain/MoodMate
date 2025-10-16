from django.shortcuts import render,redirect
from .forms import MoodEntryForm
from .models import MoodEntry
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, 'journal/home.html')


@login_required
def add_mood(request):
    if request.method == 'POST':
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit = False)
            entry.user = request.user
            entry.save()
            print("Saved:", entry)

            return redirect('mood-list')
    
    else:
        form = MoodEntryForm()
    return render(request, 'journal/add_mood.html', {'form' : form})        


@login_required
def mood_list(request):
    
    # Get all mood entries for the logged-in user
    
    entries = MoodEntry.objects.filter(user = request.user).order_by('-date')
    return render(request, 'journal/mood_list.html', {'entries' : entries})
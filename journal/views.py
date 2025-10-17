from django.shortcuts import render,redirect
from .forms import MoodEntryForm
from .models import MoodEntry
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages


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


def signup(request):
    # Signup if you are not logged in
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save() # create the new user
            login(request, user) # Log the user in immediately after signup
            return redirect('home') # Redirect to home
    else:
        form = SignUpForm()
            

    # render form (for both GET and invalid POST)
    return render(request, 'journal/signup.html', {'form': form})





def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')  # redirect to home by default
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'journal/login.html')    

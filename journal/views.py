from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.cache import cache
from django.conf import settings
from .forms import MoodEntryForm, SignUpForm, QuoteForm
from .models import MoodEntry, Quote, Mood
import requests
import logging

logger = logging.getLogger(__name__)


# for adding and showing quote
from .models import Quote



# --- Default Quote ---
DEFAULT_QUOTE = "Every mood has meaning — and every feeling deserves to be heard."
DEFAULT_AUTHOR = "MoodMate"

# --- Mood to ZenQuotes Keyword Mapping ---
MOOD_QUOTE_MAPPING = {
    'Happy': 'happiness',
    'Sad': 'life',
    'Excited': 'inspirational',
    'Angry': 'motivational',
    'Calm': 'peace'
}

# --- ZenQuotes API Config ---
ZEN_QUOTES_URL = "https://zenquotes.io/api/"
ZEN_QUOTES_KEY = getattr(settings, "ZEN_QUOTES_KEY", None)  # optional


def fetch_zenquote(endpoint="today", keyword=None):
    """
    Fetch a quote from ZenQuotes API. Always returns a dict:
    {"text": ..., "author": ...}.
    Endpoint: 'today', 'random', or 'quotes'.
    Optional keyword filters quotes by mood.
    """
    url = f"{ZEN_QUOTES_URL}{endpoint}/"
    
    # Append API key if exists
    if ZEN_QUOTES_KEY:
        url += ZEN_QUOTES_KEY
    
    # ZenQuotes doesn't officially support 'keyword' filtering in free API
    # But you can still pass it if your plan allows
    if keyword:
        url += f"?keyword={keyword}"
    
    try:
        resp = requests.get(url, timeout=6)
        resp.raise_for_status()
        data = resp.json()

        # ZenQuotes returns a list of quotes
        if isinstance(data, list) and len(data) > 0:
            item = data[0]
            text = item.get("q") or DEFAULT_QUOTE
            author = item.get("a") or DEFAULT_AUTHOR
            return {"text": text, "author": author}

        # Sometimes API might return a single dict
        if isinstance(data, dict):
            text = data.get("q") or DEFAULT_QUOTE
            author = data.get("a") or DEFAULT_AUTHOR
            return {"text": text, "author": author}

    except Exception as e:
        logger.warning("ZenQuotes API fetch failed: %s", e)

    # Fallback if API fails completely
    return {"text": DEFAULT_QUOTE, "author": DEFAULT_AUTHOR}


# # --- Home Page View ---
# def home(request):
#     """
#     Show daily inspirational quote, cached for 24 hours.
#     """
#     cache_key = "zenquote_home"
#     quote = cache.get(cache_key)
#     if not quote:
#         quote = fetch_zenquote(endpoint="today")
#         cache.set(cache_key, quote, 60 * 60 * 24)  # 24-hour cache
#     return render(request, "journal/home.html", {"quote": quote})


# generate random quotes every time

def home(request):
    quote = fetch_zenquote(endpoint="random")
    return render(request, "journal/home.html", {"quote": quote})



# --- Add Mood View ---
@login_required
def add_mood(request):
    if request.method == 'POST':
        form = MoodEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('show-quotes')
    else:
        form = MoodEntryForm()
    return render(request, "journal/add_mood.html", {"form": form})


## --- Show Mood-Based Quotes ---
@login_required
def show_quotes(request):
    last_entry = MoodEntry.objects.filter(user=request.user).order_by('-date').first()

    if last_entry:
        mood = last_entry.mood
        keyword = MOOD_QUOTE_MAPPING.get(mood, None)
        cache_key = f"zenquote_{mood}"
        quote = cache.get(cache_key)

        if not quote:
            result = fetch_zenquote(endpoint="quotes", keyword=keyword)
            # Always make it a dict with keys 'text' and 'author'
            if isinstance(result, dict):
                quote = {"text": result.get("text", DEFAULT_QUOTE),
                         "author": result.get("author", DEFAULT_AUTHOR)}
            else:
                quote = {"text": DEFAULT_QUOTE, "author": DEFAULT_AUTHOR}
            cache.set(cache_key, quote, 60*60)
    else:
        mood = None
        quote = {"text": DEFAULT_QUOTE, "author": DEFAULT_AUTHOR}
        
    if not isinstance(quote, dict):
        quote = {"text": str(quote), "author": DEFAULT_AUTHOR}


    print(f"🌟 Mood: {mood}, Quote: {quote['text']} — {quote['author']}")  # debug
    return render(request, "journal/show_quotes.html", {"quote": quote, "mood": mood})


# --- Mood List View ---
@login_required
def mood_list(request):
    entries = MoodEntry.objects.filter(user=request.user).order_by('-date')
    return render(request, "journal/mood_list.html", {"entries": entries})


# --- Signup View ---
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, "journal/signup.html", {"form": form})


# --- Login View ---
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "journal/login.html")


@login_required
def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            # Get new mood input safely
            new_mood_name = form.cleaned_data.get('new_mood')
            mood = form.cleaned_data.get('mood')  # existing mood from dropdown

            if new_mood_name:  # user entered a new mood
                new_mood_name = new_mood_name.strip()
                if new_mood_name:  # only create if not empty
                    mood, created = Mood.objects.get_or_create(name=new_mood_name)
            elif mood:
                pass  # existing mood selected, use it
            else:
                # neither new mood nor existing selected
                form.add_error('mood', 'Please select or add a mood.')
                return render(request, "journal/add_quote.html", {"form": form})

            # Save the quote
            quote = form.save(commit=False)
            quote.user = request.user
            quote.mood = mood
            quote.save()

            # Redirect after save (change to 'quote-list' if you have that page)
            return redirect('home')
    else:
        form = QuoteForm()

    return render(request, "journal/add_quote.html", {"form": form})

# Quotelist view
@login_required
def quote_list(request):
    quotes = Quote.objects.all().order_by('-created_at')
    return render(request, 'journal/quote_list.html', {'quotes': quotes})

from django.shortcuts import render, redirect, get_object_or_404
import requests
from .models import URLShortener
from django.http import JsonResponse
import pyshorteners

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def about(request):
    return render(request, 'about.html')

def feedback(request):
    return render(request, 'feedback.html')

def verify(request):
    return render(request, 'linkverify.html')

def cyber(request):
    api_url = 'https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=ffbf00a3d838482bb9bc980e0f5b61a7'
    news_articles = []

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        news_articles = data.get('articles', [])
    except requests.exceptions.RequestException as e:
        print('Error fetching news:', e)
        # You can handle the error as needed, e.g., log it or set a message for the template

    return render(request, 'cyber.html', {'news_articles': news_articles})

def short(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        s = pyshorteners.Shortener()
        short_url = s.tinyurl.short(original_url)
        url_shortener, created = URLShortener.objects.get_or_create(
            original_url=original_url, short_url=short_url
        )
        return JsonResponse({'short_url': short_url})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

 

















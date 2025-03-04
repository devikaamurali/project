from django.shortcuts import render, redirect, get_object_or_404
import requests
import urllib.request
from .models import URLShortener
from django.contrib import messages
from django.http import JsonResponse
import pyshorteners
import socket
import qrcode
from io import BytesIO
import base64

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
    if request.method == 'POST':
        link = request.POST.get('link')
        try:
            # Attempt to open the URL
            response = urllib.request.urlopen(link)
            status_code = response.getcode()
            if status_code == 200:
                return JsonResponse({'status': 'valid', 'message': 'The link is valid!'})
            else:
                return JsonResponse({'status': 'invalid', 'message': 'The link returned a status code: {}'.format(status_code)})
        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.gaierror):
                return JsonResponse({'status': 'invalid', 'message': 'Could not resolve the domain name. Please check the URL.'})
            return JsonResponse({'status': 'invalid', 'message': str(e)})
        except Exception as e:
            return JsonResponse({'status': 'invalid', 'message': str(e)})
    
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
        if not is_valid_url(original_url):
            messages.error(request, 'Please enter a valid URL.')
            return JsonResponse({'error': 'Invalid URL'}, status=400)

        try:
            s = pyshorteners.Shortener()
            short_url = s.tinyurl.short(original_url)
            url_shortener, created = URLShortener.objects.get_or_create(
                original_url=original_url, short_url=short_url
            )
            if created:
                messages.success(request, 'URL shortened successfully!')
            else:
                messages.info(request, 'This URL has already been shortened.')
            return JsonResponse({'short_url': short_url})
        except Exception as e:
            messages.error(request, 'An error occurred while shortening the URL.')
            return JsonResponse({'error': 'An error occurred'}, status=500)
    return render(request, 'short.html')

def is_valid_url(url):
    # Implement URL validation logic here
    return True
 

















from django.shortcuts import render
import requests
import validators
from django.http import JsonResponse

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



# Blacklisted domains (expand as needed)
BLACKLISTED_DOMAINS = ["example-spam.com", "malicious-site.net", "phishing-site.org"]

# Google Safe Browsing API Key (Get yours from Google)
GOOGLE_SAFE_BROWSING_API_KEY = "YOUR_API_KEY"

def check_google_safe_browsing(url):
    """Check if URL is malicious using Google Safe Browsing API."""
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_SAFE_BROWSING_API_KEY}"
    payload = {
        "client": {"clientId": "yourcompany", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}],
        },
    }

    try:
        response = requests.post(api_url, json=payload)
        data = response.json()
        if "matches" in data:
            return True  # URL is unsafe
    except Exception as e:
        print(f"Error checking Google Safe Browsing: {e}")
    
    return False  # URL is safe

def check_url_validity(request):
    """Checks if the given URL is valid, spam, or contains phishing/malware."""
    url = request.GET.get("url", None)

    if not url:
        return JsonResponse({"status": "error", "message": "No URL provided"}, status=400)

    # Validate URL format
    if not validators.url(url):
        return JsonResponse({"status": "invalid", "message": "Invalid URL format"})

    # Extract domain from URL
    domain = url.split("/")[2]

    # Check against blacklisted domains
    if domain in BLACKLISTED_DOMAINS:
        return JsonResponse({"status": "spam", "message": "URL is blacklisted as spam"})

    # Check Google Safe Browsing API
    if check_google_safe_browsing(url):
        return JsonResponse({"status": "phishing", "message": "URL detected as phishing/malware"})

    return JsonResponse({"status": "safe", "message": "URL is valid and safe"})

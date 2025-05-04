from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.db import models
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from datetime import timedelta
import random
import json
import requests
# Create your views here.
# Route for Groovepad
def groovepad(request):
    if not request.session.get('username'):
        # Show groovepad interface with login/signup options
        return render(request, 'login.html')  # Redirect to login if not authenticated
    return render(request, 'groovepad.html')

def play_beat(request):
    if not request.session.get('username'):
        return redirect('login')
    # Handle beat playing logic for authenticated users
    return JsonResponse({'status': 'success'})

def home_view(request):
    if not request.session.get('username'):
        return redirect('login')  # Redirect to login if not authenticated
    return render(request, "groovepad.html")

# Route to serve audio files
def serve_audio(request, filename):
    return JsonResponse({'audio_file': f'audio/{filename}'})

# User Login
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('pswd')
        user = User.objects.filter(email=email).first()

        if user and check_password(user.password, password):
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            return redirect('groovepad')
        else:
            return JsonResponse({"error": "Invalid Credentials"}, status=401)

# User Signup
class SignupView(View):
    def post(self, request):
        username = request.POST.get('txt')
        email = request.POST.get('email')
        password = request.POST.get('pswd')

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already taken"}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already registered"}, status=400)

        hashed_password = make_password(password)
        new_user = User(username=username, email=email, password=hashed_password)
        new_user.save()

        request.session['user_id'] = new_user.id
        request.session['username'] = new_user.username

        return redirect('groovepad')

# User Logout
def logout(request):
    request.session.flush()
    return redirect('login')

def get_flask_data(request):
    response = requests.get('http://127.0.0.1:5001/api/hello')
    data = response.json()
    return JsonResponse(data)


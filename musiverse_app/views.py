from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from google.oauth2 import id_token
from google.auth.transport import requests
from django.views.decorators.csrf import csrf_exempt
import os
from .chatgpt import generate_lyric,generate_song,generate_image,generate_lyric
from .models import Song

# Home page - Accessible only if logged in, otherwise redirect to sign-in page
def home(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            prompt = request.POST.get('message', '')
            print(prompt)
            image_url=generate_image(prompt)
            song_title,song_lyrics=generate_lyric(prompt)
            song_url=generate_song(song_lyrics)
            Song.objects.create(user=request.user, song_url=song_url,song_name=song_title, image_url=image_url,song_lyrics=song_lyrics)
        
        songs = Song.objects.filter(user=request.user)

        return render(request, 'dashboard.html',{'user_name':request.user.username,'songs':songs})
    return redirect('signin')

# Sign-in page - Redirect to home if already logged in
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email')  # Get email from form
        password = request.POST.get('password')

        try:
            print(email)
            user = User.objects.get(email=email)
            print(user)
            user = authenticate(request, username=user.username, password=password)

             # Authenticate using username
            print(user)
        except User.DoesNotExist:
            user = None
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'signin.html')


# Sign-up page - Redirect to sign-in after successful registration
def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('signup')

        # Use create_user to ensure password hashing
        user = User.objects.create_user(username=username, email=email, password=password, first_name=name)
        user.save()

        messages.success(request, 'Registration successful! Please log in.')
        return redirect('signin')

    return render(request, 'signup.html')


# Sign out - Redirect to sign-in page
def signout(request):
    logout(request)
    return redirect('signin')

def get_user_details(request):
    # Fetch the first user in the database (for example purposes)
    user = request.user  # Modify this as needed

    if user:
        user_data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
        }
        return JsonResponse(user_data)
    
    return JsonResponse({"error": "No user found"}, status=404)


def innovation_page(request):
    base_url = request.build_absolute_uri('/')
    return render(request, 'innovation.html', {'base_url': base_url})

def player_page(request):
    song_id = request.GET.get('songId')
    title = request.GET.get('title')
    lyrics = request.GET.get('lyrics')
    audio = request.GET.get('audio')
    cover = request.GET.get('cover')

    # Ensure audio is not undefined
    if audio == 'undefined':
        audio = '/static/default_audio.mp3'  # Set a default audio if not provided
    if not song_id:  # If no song ID is provided
        context = {
            'song_id': None,
            'title': 'Press any Song',
            'lyrics': 'lyrics will appear here.',
            'cover': '/static/home-icon.svg',
        }
    else:
        context = {
            'song_id': song_id,
            'title': title,
            'lyrics': lyrics,
            'audio': audio,
            'cover': cover,
        }

    return render(request, 'player.html', context)

def compose_page(request):
    base_url = request.build_absolute_uri('/')  # Dynamically gets the root URL
    prompt=request.GET.get("message")
    print(prompt)
    lyric=generate_lyric(prompt)
    context={
        'base_url':base_url,
        'prompt':prompt
    }
    import json

    def append_to_json(file_path, new_data):
        try:
            with open(file_path, 'w') as file:
                json.dump([new_data], file, indent=4)
        except json.JSONDecodeError:
            with open(file_path, 'w') as file:
                json.dump([new_data], file, indent=4)

    # Example usage
    file_path = 'music_data.json'
    new_data = {
        "id": 1,
        "lyrics": lyric,
    }

    append_to_json(file_path, new_data)

    return render(request, 'compose.html', context)

def lyric_page(request):
    base_url = request.build_absolute_uri('/')  # Dynamically gets the root URL
    import json

    if request.GET.get("regenerate") is None:
        def load_lyrics_from_json(file_path):
            try:
                with open(file_path, 'r') as file:
                    data = json.load(file)
                    return data
            except FileNotFoundError:
                print("File not found.")
                return []
            except json.JSONDecodeError:
                print("Invalid JSON.")
                return []

        def get_lyrics_by_id(data, id):
            for song in data:
                if song['id'] == id:
                    return song.get('lyrics', '')
            return None
        file_path = 'music_data.json'
        data = load_lyrics_from_json(file_path)

        # Access lyrics by ID
        lyric = get_lyrics_by_id(data, 1)
        print(lyric)
    else:
        prompt=request.GET.get("regenerate")
        lyric=generate_lyric(prompt)
    return render(request, 'lyric.html', {'base_url': base_url,'lyric':lyric})

def generate_page(request):
    base_url = request.build_absolute_uri('/')  # Dynamically gets the root URL
    return render(request, 'generate.html', {'base_url': base_url})

def account_page(request):
    base_url = request.build_absolute_uri('/')  # Dynamically gets the root URL
    return render(request, 'account.html', {'base_url': base_url})
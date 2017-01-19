from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth import authenticate, login # authenticate user


def index(request):
    return render(request, 'login_app/login.html')

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
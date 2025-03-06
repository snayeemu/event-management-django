from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def sign_up(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        
        user = User.objects.filter(username=username)
        user2 = User.objects.filter(email=email)
        if user.exists():
            messages.error(request, "Username already taken!")
            return redirect('sign-up')
        if user2.exists():
            messages.error(request, "Email already taken!")
            return redirect('sign-up')
        if len(password) < 8:
            messages.error(request, "Password length must be above 8 chars!")
            return redirect('sign-up')
        if confirm_password != password:
            messages.error(request, "Confirm Password didn't matched!")
            return redirect('sign-up')
        
        
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
        )
        
        user.set_password(password)
        user.save()
        
        messages.success(request, "Account created Successfully!")
        return redirect('sign-up')

    return render(request, "registrations/sign-up.html")

def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.filter(username=username)
        if not user.exists():
            messages.error(request, "Incorrect Username!")
            return redirect("sign-in")
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "Incorrect Password!")
            return redirect("sign-in")
        else:
            login(request, user)
            return redirect("event-list")
    return render(request, "registrations/sign-in.html")
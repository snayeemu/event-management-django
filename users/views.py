from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Permission, Group
from users import forms
from django.contrib.auth.tokens import default_token_generator 
from django.http import HttpResponse

def is_admin(user):
    return user.groups.filter(name="Admin").exists()


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
            email=email,
            password=password
        )
        
        user_group, isCreated = Group.objects.get_or_create(name="Participant")
        user.groups.add(user_group)
        user.is_active = False
        user.save()
        
        messages.success(request, "An Confirmation Email has Sent!")
        return redirect('sign-in')

    return render(request, "registrations/sign-up.html")

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "Account Activated Successfully!")
            return redirect("sign-in")
        else:
            return HttpResponse("Invalid URL")
    except Exception as e:
        print(str(e))
        return HttpResponse("User Does not Exist")
    
    

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

def sign_out(request):
    logout(request)
    return redirect("sign-in")

@login_required
@user_passes_test(is_admin, login_url="no-permission")
def create_group(request):
    exist = Group.objects.filter(name=request.POST.get("name")).exists()
    if exist:
        messages.error(request, f"Group {request.POST.get('name')} already exists!")
        return redirect("create-group")
    if request.method == "POST":
        form = forms.CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has created successfully!")
            return redirect("create-group")
    permissions = Permission.objects.all()
    return render(request, "admin/create-group.html", {"permissions": permissions})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .forms import RegistrationForm, LoginForm, ProfileEditForm
from .models import Profile
from rooms.models import Room, Message


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # Profile is created via signal
            login(request, user)
            messages.success(request, f"Welcome to Learnova, {user.username}! 🎉")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below.")

    context = {'form': form, 'page': 'register'}
    return render(request, 'accounts/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}! 👋")
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")

    context = {'form': form, 'page': 'login'}
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out. See you again!")
    return redirect('home')


def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile, created = Profile.objects.get_or_create(user=profile_user)

    hosted_rooms = Room.objects.filter(host=profile_user).order_by('-created_at')
    joined_rooms = Room.objects.filter(members=profile_user).exclude(host=profile_user).order_by('-created_at')
    recent_messages = Message.objects.filter(user=profile_user).select_related('room').order_by('-created_at')[:10]

    context = {
        'profile_user': profile_user,
        'profile': profile,
        'hosted_rooms': hosted_rooms,
        'joined_rooms': joined_rooms,
        'recent_messages': recent_messages,
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='/accounts/login/')
def edit_profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully! ✨")
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileEditForm(instance=profile, user=request.user)

    context = {'form': form}
    return render(request, 'accounts/edit_profile.html', context)

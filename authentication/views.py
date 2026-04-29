from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    # If already logged in, redirect them based on their status
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('custom_admin:dashboard')
        return redirect('home')  # Assuming your main student page is named 'home'

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")

                # Check where to route them
                if user.is_staff or user.is_superuser:
                    return redirect('custom_admin:dashboard')
                else:
                    return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been safely logged out.")
    # Change 'home' to 'authentication:login'
    return redirect('authentication:login')

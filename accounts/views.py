from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import SignUpForm, LoginForm
from .models import User


# ✅ Sign-up view
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after sign-up
        else:
            # Form errors displayed on the page
            return render(request, 'accounts/signup.html', {'form': form, 'error': 'Invalid details. Please try again.'})
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


# ✅ Login view with role-based redirection and previous-page handling
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Redirect to the previous page or dashboard
            next_url = request.GET.get('next', '/')

            # Role-based redirection
            if user.role == 'faculty':
                return redirect(next_url or '/faculty/dashboard/')
            elif user.role == 'student':
                return redirect(next_url or '/student/dashboard/')
            else:
                return HttpResponse("Invalid role", status=403)  # Handle unexpected roles
        else:
            return render(request, 'accounts/login.html', {'form': form, 'error': 'Invalid username or password'})

    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


# ✅ Logout view with redirect to login
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# ✅ Profile view (optional)
@login_required
def profile_view(request):
    """Displays user profile information."""
    return render(request, 'accounts/profile.html', {'user': request.user})

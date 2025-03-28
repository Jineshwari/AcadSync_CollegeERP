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


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from .models import User


# ✅ Improved Login View with Proper Redirection
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # 🔥 Redirect based on role
                if user.role == 'faculty':
                    return redirect('/faculty/dashboard/')   # Redirect faculty
                elif user.role == 'student':
                    return redirect('/student/dashboard/')   # Redirect student
                else:
                    return HttpResponse("Invalid role", status=403)
            
            else:
                messages.error(request, "Invalid username or password")
        
        else:
            messages.error(request, "Invalid form submission")
    
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

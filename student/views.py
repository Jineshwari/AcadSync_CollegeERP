from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def student_dashboard(request):
    return render(request, 'student/dashboard.html', {'user': request.user})

@login_required
def student_profile(request):
    """Render the student profile with their details"""
    
    user = request.user  # Get the current logged-in student

    # Pass the user data to the template
    context = {
        'user': user
    }
    return render(request, 'student/profile.html', context)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def faculty_dashboard(request):
    return render(request, 'faculty/dashboard.html', {'user': request.user})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import User
from .forms import EditFacultyProfileForm

# ✅ Faculty profile view
@login_required
def faculty_profile(request):
    """Displays the faculty's profile information."""
    faculty = request.user  # Current faculty user
    return render(request, 'faculty/profile.html', {'faculty': faculty})


# ✅ Edit faculty profile view
@login_required
def edit_faculty_profile(request):
    """Allows faculty to edit their profile."""
    faculty = request.user

    if request.method == 'POST':
        form = EditFacultyProfileForm(request.POST, request.FILES, instance=faculty)

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully! ✅")
            return redirect('faculty_profile')  # Redirect back to profile
        else:
            messages.error(request, "Error updating profile. Please try again.")
    else:
        form = EditFacultyProfileForm(instance=faculty)

    return render(request, 'faculty/edit_profile.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from .models import Classroom
from .forms import ClassroomForm

# ✅ Faculty - Create Classroom View
@login_required
def create_classroom(request):
    """ Faculty creates a new classroom """
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.faculty = request.user  # Assign faculty
            # Generate a unique join code
            classroom.join_code = get_random_string(6).upper()
            classroom.save()
            
            return redirect('/faculty/dashboard/')  # Redirect to faculty dashboard
    else:
        form = ClassroomForm()

    return render(request, 'faculty/create_classroom.html', {'form': form})

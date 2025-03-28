# student/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.utils.dateparse import parse_datetime
from faculty.models import Classroom, Assignment, Submission
from .models import StudentClassroom, GitHubSubmission
import requests

# student/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from faculty.models import Classroom, Assignment, Submission, Resource  # Import Resource model
from .models import StudentClassroom


# ✅ Student Dashboard → Display classrooms only
@login_required
def student_dashboard(request):
    student = request.user

    # Get classrooms the student has joined
    student_classrooms = StudentClassroom.objects.filter(student=student)
    classrooms = [sc.classroom for sc in student_classrooms]

    context = {
        'classrooms': classrooms,
    }
    return render(request, 'student/dashboard.html', context)


# ✅ Load classroom details dynamically in the popup
@login_required
def classroom_detail(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)

    # Assignments for the classroom
    assignments = Assignment.objects.filter(classroom=classroom)

    # Submissions for the current student
    student_submissions = Submission.objects.filter(
        student=request.user,
        assignment__in=assignments
    )

    # Resources for the classroom
    resources = Resource.objects.filter(classroom=classroom)

    context = {
        'classroom': classroom,
        'assignments': assignments,
        'submissions': student_submissions,
        'resources': resources,
    }
    return render(request, 'student/classroom_popup.html', context)

# ✅ Join Classroom
@login_required
def join_classroom(request):
    if request.method == 'POST':
        join_code = request.POST.get('join_code')

        classroom = Classroom.objects.filter(join_code=join_code).first()
        if classroom:
            if StudentClassroom.objects.filter(student=request.user, classroom=classroom).exists():
                messages.warning(request, "You're already in this classroom.")
            else:
                StudentClassroom.objects.create(student=request.user, classroom=classroom)
                messages.success(request, f"Joined {classroom.name} successfully!")
        else:
            messages.error(request, "Invalid join code. Try again!")

    return redirect('student_dashboard')


# ✅ Upload Submission
@login_required
def upload_submission(request):
    if request.method == 'POST' and request.FILES.get('file'):
        assignment = get_object_or_404(Assignment, id=request.POST.get('assignment_id'))

        # File upload handling
        file = request.FILES['file']
        fs = FileSystemStorage()
        file_path = fs.save(f'submissions/{file.name}', file)

        Submission.objects.create(
            assignment=assignment,
            student=request.user,
            file=file_path
        )

        messages.success(request, "Assignment submitted successfully!")

    return redirect('student_dashboard')


# ✅ View Classroom Details (With Assignments)
@login_required
def view_classroom(request, classroom_id):
    classroom = get_object_or_404(Classroom, id=classroom_id)
    assignments = Assignment.objects.filter(classroom=classroom)

    student_submissions = Submission.objects.filter(
        student=request.user,
        assignment__in=assignments
    )

    submitted_assignment_ids = student_submissions.values_list('assignment_id', flat=True)

    context = {
        'classroom': classroom,
        'assignments': assignments,
        'submitted_assignment_ids': submitted_assignment_ids
    }

    return render(request, 'student/classroom_detail.html', context)


# ✅ View Assignment Details with Submission Form
@login_required
def view_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    submission = Submission.objects.filter(
        assignment=assignment,
        student=request.user
    ).first()

    context = {
        'assignment': assignment,
        'submission': submission
    }

    return render(request, 'student/assignment_detail.html', context)


# ✅ Fetch GitHub Repo Details
def fetch_github_details(repo_url):
    try:
        parts = repo_url.strip('/').split('/')
        if len(parts) < 2:
            return None

        username, repo_name = parts[-2], parts[-1]
        api_url = f"https://api.github.com/repos/{username}/{repo_name}"

        response = requests.get(api_url)
        if response.status_code != 200:
            return None

        data = response.json()

        return {
            'repo_name': data.get('full_name', ''),
            'description': data.get('description', ''),
            'stars': data.get('stargazers_count', 0),
            'forks': data.get('forks_count', 0),
            'last_updated': parse_datetime(data.get('updated_at'))
        }

    except Exception as e:
        print(f"Error fetching GitHub details: {e}")
        return None

# student/views.py
import requests
from django.utils.dateparse import parse_datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import GitHubSubmission

# ✅ Extract GitHub Username from URL
def extract_github_username(repo_url):
    try:
        parts = repo_url.strip('/').split('/')
        if len(parts) < 2:
            return None
        return parts[-2]  # Extract the username from the URL
    except Exception as e:
        print(f"Error extracting username: {e}")
        return None

import os
import git  # GitPython
from django.conf import settings

# ✅ Clone GitHub repo to local storage
def clone_github_repo(repo_url, username):
    """
    Clones the GitHub repo to a local directory.
    """
    try:
        repo_name = repo_url.strip('/').split('/')[-1]  # Extract repo name
        local_path = os.path.join(settings.BASE_DIR, 'repos', username, repo_name)

        # Check if repo already exists
        if os.path.exists(local_path):
            print(f"Repo already cloned: {local_path}")
        else:
            # Clone the repo
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            git.Repo.clone_from(repo_url, local_path)
            print(f"Cloned {repo_url} to {local_path}")

        return local_path

    except Exception as e:
        print(f"Error cloning repo: {e}")
        return None


# ✅ Modify the GitHub submission view
@login_required
def submit_github_repo(request):
    if request.method == 'POST':
        repo_url = request.POST.get('repo_url')

        if 'github.com' not in repo_url:
            messages.error(request, "Invalid GitHub URL. Please enter a valid GitHub repository link.")
            return redirect('dashboard')

        # Extract username from the URL
        username = extract_github_username(repo_url)

        # Clone the repo and get local path
        local_path = clone_github_repo(repo_url, username)

        # Fetch GitHub repo details
        github_data = fetch_github_details(repo_url)

        # Save submission with local path
        submission = GitHubSubmission(
            student=request.user,
            repo_url=repo_url,
            repo_name=github_data['repo_name'] if github_data else '',
            description=github_data['description'] if github_data else '',
            stars=github_data['stars'] if github_data else 0,
            forks=github_data['forks'] if github_data else 0,
            last_updated=github_data['last_updated'] if github_data else None,
            local_path=local_path  # Save local path
        )
        submission.save()

        messages.success(request, "GitHub repository submitted and cloned successfully!")

    return redirect('dashboard')

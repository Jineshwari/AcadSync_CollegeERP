# faculty/views.py

from django.shortcuts import (
    render, redirect, get_object_or_404
)
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now

from .models import (
    Classroom, Assignment, Submission, StudentClassroom
)
from student.models import GitHubSubmission


# faculty/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from faculty.models import Classroom, Assignment, Submission
from student.models import GitHubSubmission

# ✅ Faculty Dashboard → Display GitHub Submissions with extracted username
@login_required
def faculty_dashboard(request):
    faculty_classrooms = Classroom.objects.filter(faculty=request.user)
    assignments = Assignment.objects.filter(classroom__in=faculty_classrooms)

    submissions = Submission.objects.filter(assignment__in=assignments)
    github_submissions = GitHubSubmission.objects.filter(student__in=submissions.values('student'))

    # ✅ Extract GitHub username from the repo_url
    for submission in github_submissions:
        if submission.repo_url:
            submission.github_username = submission.repo_url.strip('/').split('/')[-2]

    context = {
        'classrooms': faculty_classrooms,
        'assignments': assignments,
        'submissions': submissions,
        'github_submissions': github_submissions,
    }

    return render(request, 'faculty/dashboard.html', context)

# ✅ AJAX: Create Classroom
@login_required
def create_classroom_ajax(request):
    """Create classroom via AJAX request."""
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")

        if name and description:
            classroom = Classroom.objects.create(
                name=name,
                description=description,
                faculty=request.user
            )

            return JsonResponse({
                "success": True,
                "name": classroom.name,
                "join_code": classroom.join_code
            })

    return JsonResponse({"success": False})


# ✅ AJAX: Join Classroom
@login_required
def join_classroom_ajax(request):
    """Join a classroom using AJAX and join code."""
    if request.method == "POST":
        join_code = request.POST.get("join_code")
        classroom = Classroom.objects.filter(join_code=join_code).first()

        if classroom:
            if StudentClassroom.objects.filter(
                student=request.user, classroom=classroom
            ).exists():
                return JsonResponse({
                    "success": False, 
                    "message": "You are already in this classroom!"
                })

            # Enroll the student
            StudentClassroom.objects.create(
                student=request.user, classroom=classroom
            )

            return JsonResponse({
                "success": True,
                "name": classroom.name
            })

        return JsonResponse({
            "success": False, 
            "message": "Invalid join code!"
        })

    return JsonResponse({"success": False})


# ✅ AJAX: Get Classrooms
@login_required
def get_classrooms_ajax(request):
    """Return classrooms with ID, name, join_code, and description."""
    classrooms = Classroom.objects.filter(
        faculty=request.user
    ).values('id', 'name', 'description', 'join_code')

    return JsonResponse(list(classrooms), safe=False)


# ✅ Display Classroom with Assignments & Submissions
@login_required
def classroom_detail(request, classroom_id):
    """Display classroom details with students, assignments, and submissions."""
    classroom = get_object_or_404(Classroom, id=classroom_id)

    # Get students and assignments
    student_classrooms = StudentClassroom.objects.filter(classroom=classroom)
    students = [sc.student for sc in student_classrooms]
    assignments = Assignment.objects.filter(classroom=classroom)

    is_faculty = request.user == classroom.faculty
    submissions = Submission.objects.filter(assignment__classroom=classroom) if is_faculty else None

    if request.method == 'POST':
        # ✅ Student Submission Logic
        if 'submit_assignment' in request.POST:
            assignment_id = request.POST.get('assignment_id')
            file = request.FILES.get('file')

            if assignment_id and file:
                assignment = get_object_or_404(Assignment, id=assignment_id)
                
                # Check for existing submission
                existing_submission = Submission.objects.filter(
                    assignment=assignment, student=request.user
                ).first()

                if existing_submission:
                    existing_submission.file = file
                    existing_submission.submitted_at = now()
                    existing_submission.save()
                    messages.success(request, 'Assignment re-submitted successfully!')
                else:
                    Submission.objects.create(
                        assignment=assignment,
                        student=request.user,
                        file=file
                    )
                    messages.success(request, 'Assignment submitted successfully!')

                return redirect('classroom_detail', classroom_id=classroom_id)

        # ✅ Faculty Grading Logic
        elif 'grade_submission' in request.POST:
            submission_id = request.POST.get('submission_id')
            marks = request.POST.get('marks')
            feedback = request.POST.get('feedback')

            submission = get_object_or_404(Submission, id=submission_id)
            submission.marks = float(marks) if marks else None
            submission.feedback = feedback
            submission.save()

            messages.success(request, 'Submission graded successfully!')
            return redirect('classroom_detail', classroom_id=classroom_id)

    context = {
        'classroom': classroom,
        'students': students,
        'assignments': assignments,
        'is_faculty': is_faculty,
        'submissions': submissions
    }

    return render(request, 'faculty/classroom_detail.html', context)


# ✅ Upload Assignment
@login_required
def upload_assignment(request, classroom_id):
    """Upload an assignment to a specific classroom."""
    classroom = get_object_or_404(Classroom, id=classroom_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')

        if not title or not description or not due_date:
            return JsonResponse({'success': False, 'message': 'All fields are required!'})

        # Create the assignment
        Assignment.objects.create(
            classroom=classroom,
            title=title,
            description=description,
            due_date=due_date
        )

        return redirect('classroom_detail', classroom_id=classroom_id)

    return render(request, 'faculty/upload_assignment.html', {'classroom': classroom})
import os

# ✅ View repo file structure
@login_required
def view_repo(request, submission_id):
    submission = get_object_or_404(GitHubSubmission, id=submission_id)

    repo_path = submission.local_path
    file_structure = []

    if os.path.exists(repo_path):
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                relative_path = os.path.relpath(os.path.join(root, file), repo_path)
                file_structure.append(relative_path)

    context = {
        'submission': submission,
        'file_structure': file_structure
    }
    return render(request, 'faculty/view_repo.html', context)

import shutil
from django.http import HttpResponse

# ✅ Download repo as ZIP
@login_required
def download_repo(request, submission_id):
    submission = get_object_or_404(GitHubSubmission, id=submission_id)

    zip_path = f"{submission.local_path}.zip"
    shutil.make_archive(submission.local_path, 'zip', submission.local_path)

    with open(zip_path, 'rb') as zip_file:
        response = HttpResponse(zip_file.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{submission.repo_name}.zip"'
        return response

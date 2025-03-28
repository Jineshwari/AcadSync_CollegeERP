# student/models.py

from django.db import models
from django.conf import settings
from faculty.models import Classroom, Assignment


# ✅ Student-Classroom Relationship
class StudentClassroom(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_classrooms'
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name='classroom_students'
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'classroom')

    def __str__(self):
        return f"{self.student.username} → {self.classroom.name}"


# ✅ Submission Model (Student)
class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='student_submissions'  # 👈 Unique related_name
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_submissions'  # 👈 Unique related_name
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/')
    feedback = models.TextField(blank=True, null=True)
    marks = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"


# ✅ Student Profile
class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    github_username = models.CharField(
        max_length=100, 
        blank=True, 
        null=True
    )

    def __str__(self):
        return self.user.username

# student/models.py
from django.db import models
from django.conf import settings

class GitHubSubmission(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    repo_url = models.URLField()

    # GitHub repo details
    repo_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    stars = models.IntegerField(default=0)
    forks = models.IntegerField(default=0)
    last_updated = models.DateTimeField(blank=True, null=True)

    # Store cloned repo path
    local_path = models.CharField(max_length=500, blank=True, null=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} → {self.repo_url}"

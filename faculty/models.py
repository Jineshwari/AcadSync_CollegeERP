# faculty/models.py

from django.db import models
from django.conf import settings  # Reference custom User model
import random
import string


# ✅ Classroom Model
class Classroom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    join_code = models.CharField(max_length=8, unique=True, blank=True)
    faculty = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Generate a unique join code when creating the classroom."""
        if not self.join_code:
            self.join_code = ''.join(random.choices(
                string.ascii_uppercase + string.digits, k=8
            ))
        super(Classroom, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.join_code})"


# ✅ Student-Classroom Relationship
class StudentClassroom(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='faculty_student_classrooms'
    )
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name='faculty_classroom_students'
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'classroom')

    def __str__(self):
        return f"{self.student.username} → {self.classroom.name}"


# ✅ Assignment Model
class Assignment(models.Model):
    classroom = models.ForeignKey(
        Classroom, 
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    marks = models.IntegerField(default=100)  # Marks field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ✅ Submission Model (Faculty)
class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment, 
        on_delete=models.CASCADE, 
        related_name='faculty_submissions'  # Unique related_name
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='faculty_submissions'  # Unique related_name
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/')
    feedback = models.TextField(blank=True, null=True)
    marks = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"

# ✅ Resource Model
class Resource(models.Model):
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name='resources'
    )
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='resources/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

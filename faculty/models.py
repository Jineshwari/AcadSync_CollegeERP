from django.db import models
from accounts.models import User  # Import User model for relations

# ✅ Classroom model
class Classroom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    join_code = models.CharField(max_length=10, unique=True)  # Unique join code
    faculty = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classrooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.faculty.username})"


# ✅ Student-Classroom Relationship
class StudentClassroom(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='students')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'classroom')  # Prevent duplicate enrollments

    def __str__(self):
        return f"{self.student.username} → {self.classroom.name}"


# ✅ Assignment model
class Assignment(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=150)
    description = models.TextField()
    due_date = models.DateTimeField()
    max_marks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.classroom.name})"


# ✅ Submission model
class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='assignments/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    marks = models.IntegerField(blank=True, null=True)  # Marks (optional until graded)
    feedback = models.TextField(blank=True, null=True)  # Feedback from faculty
    late_submission = models.BooleanField(default=False)  # Late flag

    def __str__(self):
        return f"{self.student.username} → {self.assignment.title}"

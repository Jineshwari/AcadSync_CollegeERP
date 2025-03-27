from django.contrib import admin
from .models import Classroom, StudentClassroom, Assignment, Submission

# ✅ Register models
@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty', 'join_code', 'created_at')

@admin.register(StudentClassroom)
class StudentClassroomAdmin(admin.ModelAdmin):
    list_display = ('student', 'classroom', 'joined_at')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'classroom', 'due_date', 'max_marks', 'created_at')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'submitted_at', 'marks', 'late_submission')

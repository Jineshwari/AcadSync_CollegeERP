from django.contrib import admin
from .models import StudentClassroom, Submission

@admin.register(StudentClassroom)
class StudentClassroomAdmin(admin.ModelAdmin):
    list_display = ('student', 'classroom', 'joined_at')
    search_fields = ('student__username', 'classroom__name')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'submitted_at', 'marks')
    search_fields = ('student__username', 'assignment__title')

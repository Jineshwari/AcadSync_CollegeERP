from django.contrib import admin
from .models import Classroom, Assignment, Submission

admin.site.register(Classroom)
admin.site.register(Assignment)
admin.site.register(Submission)
